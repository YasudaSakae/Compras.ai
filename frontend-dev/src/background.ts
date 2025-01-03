chrome.action.onClicked.addListener((tab) => {
  chrome.storage.local.get(["extensionOpened"], (result) => {
    if (result.extensionOpened) {
      console.log("Extension is already opened.");
      return;
    }

    if (
      tab.url &&
      !tab.url.startsWith("chrome://") &&
      !tab.url.startsWith("edge://")
    ) {
      if (tab.id !== undefined) {
        chrome.scripting.executeScript(
          {
            target: { tabId: tab.id },
            files: ["content.js"],
          },
          () => {
            if (chrome.runtime.lastError) {
              console.error(
                "Error injecting script:",
                chrome.runtime.lastError.message
              );
            } else {
              console.log("Script injected into:", tab.url);
              chrome.storage.local.set({ extensionOpened: true });
            }
          }
        );
      } else {
        console.error("Tab ID is undefined.");
      }
    } else {
      console.error("Cannot inject script into this URL:", tab.url);
    }
  });
});

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.action === "closeExtension") {
    chrome.storage.local.set({ extensionOpened: false });
    sendResponse({ status: "Extension closed" });
  }
});
