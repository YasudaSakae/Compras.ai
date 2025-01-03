import { FunctionComponent, ReactElement, useContext } from "react";
import styled from "styled-components";
import * as S from "../components/styleComponents";

import { InfoCard } from "../components/infoCard";
import { Header } from "../components/header";
import { SideBar } from "../components/sideBar";
import { DFD } from "./mainContent/DFD";
import { GlobalContext } from "../context/GlobalContext";
import { ETP } from "./mainContent/ETP";
import { ConfigPage } from "./mainContent/Config";
import { AssistPage } from "./mainContent/Assist";
import { SEIPage } from "./mainContent/SEI";

const Container = styled.div`
  width: 100%;
  height: auto;
  box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.3);
  overflow-x: hidden;
`;
const ContentContainer = styled(S.Container)`
  height: 100%;
  width: auto;
  display: flex;
`;

const Main: FunctionComponent = () => {
  const { sideBarOption } = useContext(GlobalContext);

  function view(): ReactElement {
    switch (sideBarOption.sideBarOption) {
      case "DFD":
        return <DFD sideBarOption={sideBarOption} />;
      case "ETP":
        return <ETP sideBarOption={sideBarOption} />;
      case "config":
        return <ConfigPage />;
      case "assist":
        return <AssistPage />;
      case "SEI":
        return <SEIPage />;
      default:
        return <DFD sideBarOption={sideBarOption} />;
    }
  }

  return (
    <Container>
      <Header />
      <InfoCard />
      <ContentContainer>
        {view()}
        <SideBar />
      </ContentContainer>
    </Container>
  );
};

export default Main;
