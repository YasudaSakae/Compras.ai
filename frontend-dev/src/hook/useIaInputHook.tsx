import { useEffect, useState } from "react";

const useIaInputHook = (initialText: string) => {
  const [text, setText] = useState(initialText);
  useEffect(() => {
    setText(initialText);
  }, [initialText]);

  const enrichFunction = () => {
    setText("enriched ");
  };

  const handleExport = async (
    setShowModal: React.Dispatch<React.SetStateAction<boolean>>
  ) => {
    const iframeEmpty = await isIframeEmpty();
    if (iframeEmpty) {
      clipBoard();
    } else {
      setShowModal(true);
    }
  };

  const isIframeEmpty = async () => {
    return new Promise<boolean>((resolve) => {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]?.id) {
          chrome.scripting.executeScript(
            {
              target: { tabId: tabs[0].id },
              func: () => {
                const iframe = document.querySelector("iframe");
                if (iframe && iframe.contentDocument) {
                  const iframeDoc = iframe.contentDocument;
                  // const body = iframeDoc.getElementsByTagName("body");
                  // if (body.length > 0) {
                  //   return body[0].innerText.trim() === "";
                  // }
                  const p = iframeDoc.getElementsByTagName("p");
                  if (p.length > 0) {
                    return p[0].innerText.trim() === "";
                  }
                }
                return false;
              },
            },
            (results) => {
              if (results && results[0]) {
                resolve(results[0].result ?? false);
              } else {
                resolve(false);
              }
            }
          );
        } else {
          resolve(false);
        }
      });
    });
  };

  const clipBoard = () => {
    const textarea = document.createElement("textarea");
    textarea.value = text;

    textarea.style.position = "fixed";
    textarea.style.top = "0";
    textarea.style.left = "0";
    textarea.style.opacity = "0";

    document.body.appendChild(textarea);

    textarea.focus();
    textarea.select();

    document.execCommand("copy");

    document.body.removeChild(textarea);

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.id) {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          func: (message: string) => {
            const iframe = document.querySelector("iframe");
            if (iframe && iframe.contentDocument) {
              const iframeDoc = iframe.contentDocument;
              // const body = iframeDoc.getElementsByTagName("body");
              // if (body.length > 0) {
              //   body[0].innerText = message;
              //   console.log("Texto <body> exportado com sucesso.");
              // } else {
              //   console.error("Tag <body> não encontrada.");
              // }
              const p = iframeDoc.getElementsByTagName("p");
              if (p.length > 0) {
                p[0].innerText = message;
                console.log("Texto <p> exportado com sucesso.");
              } else {
                console.error("Tag <p> não encontrada.");
              }
            } else {
              console.error(
                "Iframe não encontrado ou sem acesso ao conteúdo.",
                iframe?.contentDocument
              );
            }
          },
          args: [text],
        });
      }
    });
  };

  const alternativeFuntion = () => console.log("alternative");
  const adjustmentFunction = () => console.log("adjustment");
  const arrowBackFunction = () => console.log("arrowBack");
  const arrowForwardFunction = () => console.log("arrowForward");

  return {
    enrichFunction,
    alternativeFuntion,
    adjustmentFunction,
    handleExport,
    arrowBackFunction,
    arrowForwardFunction,
    clipBoard,
  };
};

export default useIaInputHook;
