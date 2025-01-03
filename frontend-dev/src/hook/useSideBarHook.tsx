import { useContext } from "react";
import { GlobalContext } from "../context/GlobalContext";

const useSideBarHook = () => {
  const { setSideBarOption } = useContext(GlobalContext);

  function dfdFunction() {
    setSideBarOption({
      title: "Estudo técnico preliminar (DFD)",
      sideBarOption: "DFD",
    });
  }
  function etpFunction() {
    setSideBarOption({
      title: "Estudo técnico preliminar (ETP)",
      sideBarOption: "ETP",
    });
  }

  function configFunction() {
    setSideBarOption({
      title: "Configurações",
      sideBarOption: "config",
    });
  }
  function seiFunction() {
    setSideBarOption({
      title: "SEI",
      sideBarOption: "SEI",
    });
  }
  function assistFunction() {
    setSideBarOption({
      title: "Assistente",
      sideBarOption: "assist",
    });
  }
  return {
    dfdFunction,
    etpFunction,
    configFunction,
    assistFunction,
    seiFunction,
  };
};

export default useSideBarHook;
