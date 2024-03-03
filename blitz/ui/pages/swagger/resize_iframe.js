const iframe = document.querySelector("iframe");

const resizeIframe = function () {
  iframe.style.height = iframe.contentWindow.document.body.scrollHeight + "px";
};
