const iframe = document.querySelector("iframe");

const resizeIframe = function () {
  iframe.style.height = iframe.contentWindow.document.body.scrollHeight + "px";
};

const navList = iframe.getElementById("navList");
if (navList) {
  var lastNavItem = navList.lastElementChild;
  if (lastNavItem) {
    lastNavItem.style.pointerEvents = "none";
    lastNavItem.style.color = "gray";
  }
}
