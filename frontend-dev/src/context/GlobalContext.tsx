import React, { createContext, useState, ReactNode } from "react";
import { SideBarOptionT } from "../types/SideBarOptions";

interface GlobalContextProps {
  sideBarOption: SideBarOptionT;
  setSideBarOption: React.Dispatch<
    React.SetStateAction<{ title: string; sideBarOption: string }>
  >;
  logged: boolean;
  setLogged: React.Dispatch<React.SetStateAction<boolean>>;
  currentPage: string;
  setCurrentPage: React.Dispatch<React.SetStateAction<string>>;
  SeiCount: number;
  setSeiCount: React.Dispatch<React.SetStateAction<number>>;
}

const defaultState = {
  sideBarOption: {
    title: "Estudo técnico preliminar (DFD)",
    sideBarOption: "DFD",
  },
  setSideBarOption: () => {},
  logged: false,
  setLogged: () => {},
  currentPage: "main",
  setCurrentPage: () => {},
  SeiCount: 0,
  setSeiCount: () => {},
};

export const GlobalContext = createContext<GlobalContextProps>(defaultState);

export const GlobalProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [sideBarOption, setSideBarOption] = useState(
    defaultState.sideBarOption
  );

  const [logged, setLogged] = useState(defaultState.logged);

  const [currentPage, setCurrentPage] = useState(defaultState.currentPage);

  const [SeiCount, setSeiCount] = useState(defaultState.SeiCount);

  return (
    <GlobalContext.Provider
      value={{
        sideBarOption,
        setSideBarOption,
        logged,
        setLogged,
        currentPage,
        setCurrentPage,
        SeiCount,
        setSeiCount,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};
