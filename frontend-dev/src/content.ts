console.log("Content script injected successfully!");

if (!document.getElementById("compras-ia-container")) {
  const container = document.createElement("div");
  container.id = "compras-ia-container";
  container.style.position = "fixed";
  container.style.top = "0px";
  container.style.right = "0px";
  container.style.height = "95vh";
  container.style.boxShadow = "0px 0px 5px 0px rgba(0, 0, 0, 0.12)";
  container.style.width = "650px";
  container.style.zIndex = "99999";
  container.style.margin = "20px";
  container.style.borderRadius = "12px";
  container.style.transition =
    "width 0.3s, height 0.3s, transform 0.3s, opacity 0.3s";
  container.style.transform = "scale(0.1)";
  container.style.opacity = "0";

  const iFrame = document.createElement("iframe");
  iFrame.style.height = "100%";
  iFrame.style.width = "100%";
  iFrame.style.backgroundColor = "white";
  iFrame.style.color = "black";
  iFrame.style.border = "15px";
  iFrame.style.borderRadius = "12px";
  iFrame.style.boxShadow = "0px 0px 5px 0px rgba(0, 0, 0, 0.12)";
  iFrame.setAttribute("src", chrome.runtime.getURL("index.html"));

  const closeButton = document.createElement("button");
  closeButton.className = "close-button-compras-ia";
  closeButton.style.position = "absolute";
  closeButton.style.top = "0";
  closeButton.style.right = "0";
  closeButton.style.backgroundColor = "transparent";
  closeButton.style.padding = "15px";
  closeButton.style.border = "none";
  closeButton.style.cursor = "pointer";
  closeButton.style.color = "black";
  closeButton.style.outline = "none";

  const closeIcon = document.createElement("span");
  closeIcon.className = "material-symbols-outlined";
  closeIcon.textContent = "close";
  closeIcon.style.fontSize = "20px";
  closeButton.appendChild(closeIcon);

  const expandButton = document.createElement("button");
  expandButton.className = "expand-button-compras-ia";
  expandButton.style.position = "absolute";
  expandButton.style.top = "0";
  expandButton.style.left = "0px";
  expandButton.style.backgroundColor = "transparent";
  expandButton.style.padding = "15px";
  expandButton.style.border = "none";
  expandButton.style.cursor = "pointer";
  expandButton.style.color = "black";
  expandButton.style.outline = "none";

  const expandIcon = document.createElement("span");
  expandIcon.className = "material-symbols-outlined";
  expandButton.style.color = "black";
  expandIcon.textContent = "expand_content";
  expandIcon.style.fontSize = "20px";
  expandButton.appendChild(expandIcon);

  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href =
    "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined";
  document.head.appendChild(link);

  let isExpanded = false;

  expandButton.addEventListener("click", () => {
    if (isExpanded) {
      container.style.width = "650px";
      container.style.height = "95vh";
      expandIcon.textContent = "expand_content";
    } else {
      container.style.width = "98%";
      container.style.height = "95vh";
      expandIcon.textContent = "collapse_content";
    }
    isExpanded = !isExpanded;
  });

  closeButton.addEventListener("click", () => {
    container.style.transform = "scale(0.1) translate(50%, -50%)";
    container.style.opacity = "0";

    setTimeout(() => {
      document.body.removeChild(container);
      chrome.runtime.sendMessage({ action: "closeExtension" }, (response) => {
        console.log(response.status);
      });
    }, 300);
  });

  document.body.appendChild(container);

  setTimeout(() => {
    container.style.transform = "scale(1)";
    container.style.opacity = "1";
  }, 10);

  container.appendChild(iFrame);
  container.appendChild(closeButton);
  container.appendChild(expandButton);
}

window.addEventListener("beforeunload", () => {
  chrome.runtime.sendMessage({ action: "closeExtension" }, (response) => {
    console.log(response.status);
  });
});
