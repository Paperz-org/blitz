from pathlib import Path

from blitz.db.errors import NoChangesDetectedError
from blitz.models.base import BaseResourceModel, clear_metadata, create_resource_model
from blitz.models.blitz.field import _BlitzNullValue, AllowedBlitzFieldTypes, BlitzField, BlitzType
from blitz.models.blitz.file import BlitzFile
from blitz.models.blitz.resource import BlitzResource, BlitzResourceConfig
from blitz.parser import find_blitz_file_path
from blitz.db.migrations import generate_migration, run_migrations
import warnings
from sqlalchemy import exc as sa_exc
from semver import Version
from loguru import logger


class BlitzApp:
    def __init__(
        self,
        name: str,
        path: Path,
        file: BlitzFile,
        in_memory: bool = False,
        version: Version | None = None,
    ) -> None:
        self.name = name
        self.path = path
        self.file = file
        self.version = version
        self.logger = logger.bind(blitz_app=self.name)

        # TODO Change to a database connector to make BlitzApp agnostic of the database implementation
        self._in_memory = in_memory
        self.resources: list[BlitzResource] = []
        self._is_loaded = False
        self._base_resource_model: type[BaseResourceModel] = BaseResourceModel
        self._available_version: list[Version] = []

        self._load_versions()

    def _load_versions(self) -> None:
        if not self.path.exists() or not self.path.is_dir():
            return

        for directory in self.path.iterdir():
            if directory.is_dir():
                try:
                    version = Version.parse(directory.name)
                except Exception:
                    continue

                try:
                    find_blitz_file_path(self.path / str(version))
                except Exception:
                    raise ValueError(
                        f"Blitz app {self.name} has a version dir '{version}' without a blitz file inside."
                    )
                self._available_version.append(version)

        self._available_version = sorted(self._available_version)

    def get_version(self, version: Version) -> "BlitzApp":
        if version not in self._available_version:
            raise ValueError(f"Version {version} not found for Blitz app {self.name}")
        return BlitzApp(
            name=self.name,
            path=self.path,
            file=BlitzFile.from_file(find_blitz_file_path(self.path / str(version))),
            in_memory=self._in_memory,
            version=version,
        )

    def load(self) -> None:
        """
        Can be more elegant
        """
        if self._is_loaded:
            return

        models_by_name: dict[str, type[BaseResourceModel]] = {}
        config_by_name: dict[str, BlitzResourceConfig] = {config.name: config for config in self.file.resources_configs}
        for config in self.file.resources_configs:
            relationships: dict[str, list[str]] = {}
            for field in config.fields.values():
                # Change the field type depending of the target table column type
                if field.type == AllowedBlitzFieldTypes.foreign_key:
                    if not isinstance(field.foreign_key, _BlitzNullValue):
                        table, column = field.foreign_key.split(".")
                        if table not in config_by_name:
                            raise ValueError(f"Table `{table}` not found for foreign key `{field.foreign_key}`")

                        if column in self._base_resource_model.__default_columns__:
                            field.type = BlitzType(
                                type=AllowedBlitzFieldTypes.from_class(
                                    self._base_resource_model.__annotations__[column]
                                )
                            )
                        elif column in config_by_name[table].fields:
                            field.type = config_by_name[table].fields[column].type
                        else:
                            raise ValueError(
                                f"Column `{column}` not found in table `{table}` for foreign key `{field.foreign_key}`"
                            )
                    else:
                        raise ValueError(f"Foreign key `{field.foreign_key}` is missing.")

            # We loop through the relationships to create the relationship field in the other table
            for relationship in relationships:
                config.fields[relationship.lower()] = BlitzField(
                    type=AllowedBlitzFieldTypes.relationship,
                    relationship=relationship,
                )
            try:
                model = create_resource_model(config, already_created_models=models_by_name)
                models_by_name[config.name] = model
            except Exception:
                raise
            self.resources.append(BlitzResource(config=config, model=model))

        self._is_loaded = True

    def release(self, level: str, force: bool = False) -> Version:
        clear_metadata()

        latest_version = self._available_version[-1] if self._available_version else None

        # If there is already a released version
        if latest_version is not None:
            # Check if the path (then the app) exists
            latest_version_path = self.path / f"{latest_version}"
            assert latest_version_path.exists()

            # We bump the version regarding the release level
            match level:
                case "major":
                    new_version = latest_version.bump_major()
                case "minor":
                    new_version = latest_version.bump_minor()
                case "patch":
                    new_version = latest_version.bump_patch()

            if self.file.path is None:
                # TODO: handle error
                raise Exception
            # We run the migrations to the latest version
            latest_blitz_app = BlitzApp(
                "", latest_version_path, BlitzFile.from_file(latest_version_path / self.file.path.name), in_memory=True
            )

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=sa_exc.SAWarning)
                latest_blitz_app.load()

            run_migrations(
                blitz_app=self,
                in_memory=True,
                is_release=True,
            )
        # Else, we consider it's the first release
        else:
            try:
                # Use the version in the blitz file as initial version
                new_version = Version.parse(self.file.config.version)
            except Exception:
                logger.warning(
                    (
                        f"Version in blitz file {self.file.path} is not a valid semver version."
                        "Using 0.1.0 as the new version."
                    )
                )
                new_version = Version(major=0, minor=1, patch=0)

        new_version_path = self.path / str(new_version)
        new_blitz_file = self.file.model_copy()
        new_blitz_file.config.version = str(new_version)

        # Now we run generate the migration for this blitz app
        released_blitz_app = BlitzApp(
            name=self.name,
            path=self.path,
            file=self.file,
            in_memory=True,
        )
        clear_metadata()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)
            released_blitz_app.load()

        try:
            generate_migration(
                message="Blitz autogenerated migration",
                blitz_app=released_blitz_app,
                in_memory=True,
                is_release=True,
            )
        except NoChangesDetectedError:
            if force is False:
                raise

        # If everything went well, we create the new version directory
        if not new_version_path.exists():
            new_version_path.mkdir(parents=True)

        if self.file.path is None:
            # TODO: handle error
            raise Exception
        # We copy the current blitz file to the new version directory
        new_version_blitz_file_path = new_version_path / self.file.path.name
        new_version_blitz_file_path.write_text(self.file.path.read_text())

        # Automatically update the blitz file version needs a specific write method
        # new_blitz_file = self.file.model_copy()
        # new_blitz_file.config.version = str(new_version)
        # new_version_blitz_file_path = new_version_path / self.file.path.name
        # with open(new_version_blitz_file_path, "w") as f:
        #     new_blitz_config = new_blitz_file.config.version = str(new_version)

        return new_version
