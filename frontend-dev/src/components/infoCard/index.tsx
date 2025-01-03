import comprasNetLogo from "../../assets/icons/comprasNetLogo.svg";
import uploadFile from "../../assets/icons/buttons/uploadFileButton.svg";
import downloadFile from "../../assets/icons/buttons/downloadFileButton.svg";
import newFile from "../../assets/icons/buttons/newFileButton.svg";
import * as S from "../styleComponents";
import styled from "styled-components";
import { useContext } from "react";
import { GlobalContext } from "../../context/GlobalContext";
import configIcon from "../../assets/icons/ajustes.svg";
import assistentIcon from "../../assets/icons/assistente.svg";
import backButton from "../../assets/icons/buttons/backButton.svg";
import useSideBarHook from "../../hook/useSideBarHook";

const Container = styled(S.Container)`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  &.info-card-text {
    gap: 8px;
  }
  &.buttons {
    flex-direction: row;
    justify-content: flex-start;
    gap: 30px;
    margin: 0.5em 0;
  }
`;

const Badge = styled.span`
  position: absolute;
  transform: translateY(-10px);
  left: 20px;
  background-color: white;
  color: #1a6873;
  border-radius: 50%;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.295);
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;

  &.empty {
    position: absolute;
    transform: translateY(-10px);
    left: 20px;
    background-color: #FF6A56;
    color: white;
    border-radius: 50%;
    border: 1px solid white;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.295);
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
  }
`;

const Section = styled(S.Container)`
  background-color: var(--color-darkcyan-100);
  display: flex;
  width: auto;
  align-items: center;
  padding: 5px 20px;
  gap: var(--gap-xl);
  font-size: var(--font-size-xl);
  color: var(--color-white);
`;

const Title = styled(S.Text)`
  color: white;
  font-size: 0.9em;
  font-weight: bold;
  margin: 0.5em 0;
`;

const Subtitle = styled(S.Text)`
  color: white;
  font-size: 0.7em;
  margin: 0;
  font-weight: lighter;
`;

export function InfoCard() {
  const { sideBarOption, SeiCount } = useContext(GlobalContext);
  const { dfdFunction, seiFunction } = useSideBarHook();

  function currentInfo() {
    switch (sideBarOption.sideBarOption) {
      case "config":
        return (
          <Section>
            <Container>
              <Container>
                <Title
                  style={{ display: "flex", alignItems: "center", gap: "10px" }}
                >
                  <S.Image src={backButton} onClick={dfdFunction} />
                  Configurações
                  <S.Image src={configIcon} />
                </Title>
              </Container>
            </Container>
          </Section>
        );
      case "assist":
        return (
          <Section>
            <Container>
              <Container>
                <Title
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "10px",
                  }}
                >
                  <S.Image src={backButton} onClick={dfdFunction} />
                  Assistente
                  <S.Image src={assistentIcon} />
                </Title>
              </Container>
            </Container>
          </Section>
        );
      default:
        return (
          <Section>
            {sideBarOption.sideBarOption !== "SEI" ? (
              <S.Image src={comprasNetLogo} />
            ) : (
              <S.Image src={backButton} onClick={dfdFunction} />
            )}
            <Container>
              <Container>
                <Title>Aquisição de equipamentos de informática</Title>
                <Container>
                  <Subtitle>
                    Processo administrativo: 03001.004484/2024-81
                  </Subtitle>
                  <Subtitle>
                    Iniciado por Antonio Machado em 12/11/2024 às 12:43
                  </Subtitle>
                </Container>
              </Container>
              <Container className="buttons">
                <S.Button onClick={seiFunction}>
                  <S.Image src={uploadFile} />
                  <Badge className={SeiCount !== 0 ? "" : "empty"}>
                    {SeiCount > 0 ? SeiCount : "!"}
                  </Badge>
                </S.Button>
                <S.Button disabled>
                  <S.Image src={downloadFile} />
                </S.Button>
                <S.Button disabled>
                  <S.Image src={newFile} />
                </S.Button>
              </Container>
            </Container>
          </Section>
        );
    }
  }

  return currentInfo();
}
