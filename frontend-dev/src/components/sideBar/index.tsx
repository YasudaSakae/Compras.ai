import dfd from "../../assets/icons/dfd.svg";
import etp from "../../assets/icons/etp.svg";
import riscos from "../../assets/icons/riscos.svg";
import tr from "../../assets/icons/tr.svg";
import edital from "../../assets/icons/edital.svg";
import assistente from "../../assets/icons/assistente.svg";
import ajustes from "../../assets/icons/ajustes.svg";

import * as S from "../styleComponents";
import styled from "styled-components";
import useSideBarHook from "../../hook/useSideBarHook";
import { useContext, useEffect, useState } from "react";
import { GlobalContext } from "../../context/GlobalContext";

const Button = styled(S.Button) <{ selected?: boolean }>`
  cursor: pointer;
  background-color: ${(props) => (props.selected ? "#1A6873" : "transparent")};
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: none;
  position: relative;
  display: inline-block;
  padding: 0.5em 0;
  margin: 0;
  gap: 5px;
  &:hover {
    background-color: ${(props) =>
    props.selected ? "#1A6873" : "var(--color-darkcyan-100)"};
    border: none;
  }
  &.sei-button {
    color: white;
    font-size: 16px;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    position: relative;
    cursor: pointer;
  }
`;

const ButtonLabel = styled(S.Text)`
  font-size: 0.9em;
  font-weight: bold;
  color: white;
  width: 70px;
`;
const ImageButton = styled.img`
  width: 30px;
`;

const SideBarContainer = styled(S.Container)`
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  width: 110px;
  background-color: #1795a6;
  justify-content: space-between;
  align-items: center;
  padding: 1.6em 0 5em 0;
`;

const Container = styled(S.Container)`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8em;
`;

export function SideBar() {
  const { dfdFunction, etpFunction, configFunction, assistFunction } =
    useSideBarHook();
  const [selectedButton, setSelectedButton] = useState<string | null>("dfd");
  const { sideBarOption } = useContext(GlobalContext);

  const handleButtonClick = (buttonId: string, action: () => void) => {
    setSelectedButton(buttonId);
    action();
  };

  useEffect(() => {
    setSelectedButton(sideBarOption.sideBarOption);
  }, [sideBarOption.sideBarOption]);

  if (
    sideBarOption.sideBarOption === "config" ||
    sideBarOption.sideBarOption === "assist" ||
    sideBarOption.sideBarOption === "SEI"
  ) {
    return null;
  }

  return (
    <SideBarContainer>
      <Container>
        <Button
          selected={selectedButton === "DFD"}
          onClick={() => handleButtonClick("dfd", dfdFunction)}
        >
          <ImageButton src={dfd} />
          <ButtonLabel>DFD</ButtonLabel>
        </Button>
        <Button
          selected={selectedButton === "ETP"}
          onClick={() => handleButtonClick("etp", etpFunction)}
        >
          <ImageButton src={etp} />
          <ButtonLabel>ETP</ButtonLabel>
        </Button>
        <Button disabled>
          <ImageButton src={riscos} />
          <ButtonLabel>Riscos</ButtonLabel>
        </Button>
        <Button disabled>
          <ImageButton src={tr} />
          <ButtonLabel>TR</ButtonLabel>
        </Button>
        <Button disabled>
          <ImageButton src={edital} />
          <ButtonLabel>Edital</ButtonLabel>
        </Button>
      </Container>
      <Container>
        <Button
          selected={selectedButton === "assistente"}
          onClick={() => handleButtonClick("assistente", assistFunction)}
        >
          <ImageButton src={assistente} />
          <ButtonLabel>Assistente</ButtonLabel>
        </Button>
        <Button
          selected={selectedButton === "config"}
          onClick={() => handleButtonClick("config", configFunction)}
        >
          <ImageButton src={ajustes} />
          <ButtonLabel>Ajustes</ButtonLabel>
        </Button>
      </Container>
    </SideBarContainer>
  );
}
