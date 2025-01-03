import enrich from "../../assets/icons/buttons/enrichButton.svg";
import adjustment from "../../assets/icons/buttons/spotAdjustmentButton.svg";
import exportText from "../../assets/icons/buttons/setTextButton.svg";
import closeButton from "../../assets/icons/buttons/closeButton.svg";
import arrowLeft from "../../assets/icons/buttons/arrowLeftButton.svg";
import arrowRight from "../../assets/icons/buttons/arrowRightButton.svg";
import useIaInputHook from "../../hook/useIaInputHook";
import * as S from "../styleComponents";
import styled from "styled-components";
import React, { useEffect, useState } from "react";
import { Button } from "../../components/button";
import { Modal } from "../modal";
const TextArea = styled.textarea`
  border: 1px solid #b1b1b1;
  width: 100%;
  resize: none;
  background-color: transparent;
  outline: 0;
  height: 224px;
  border-radius: var(--br-9xs);
  box-sizing: border-box;
  overflow-y: auto;
  flex-shrink: 0;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  padding: var(--padding-base);
  font-family: var(--font-lexend);
  font-size: var(--font-size-xs);
  color: #686868;
  min-width: 250px;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: #adadad;
  }

  &::-webkit-scrollbar-thumb {
    background: #808080;
    border-radius: 10px;
  }
`;

const IAfield = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1em;
  margin: 1em 0;
`;

export const ButtonsDiv = styled.div`
  position: relative; /* Necessário para o posicionamento absoluto dos botões */
  display: flex;
  gap: 10px;

  &.iaButtons {
    width: 100%;
    justify-content: flex-end;
    gap: 15px;
  }
`;

const Title = styled(S.Text)`
  font-size: 1.3em;
  margin: 0.5em 0;
  font-weight: 400;
`;

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #00000020;
  color: black;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background: white;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 1em;
  border-radius: 12px;
  width: 100%;
  max-width: 80%;
`;

interface IATextAreaProps {
  inputName: string;
  label: string;
  placeholder?: string;
}

export const IATextArea: React.FC<IATextAreaProps> = ({
  inputName,
  label,
  placeholder = "Digite algo e experimente enriquecer o conteúdo...",
}) => {
  const [text, setText] = useState("");
  const [modalText, setModalText] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [exportTextModal, setExportTextModal] = useState(false);

  useEffect(() => {
    const storedText = localStorage.getItem(inputName);
    if (storedText) {
      setText(storedText);
      setModalText(storedText);
      console.log(exportTextModal);
    } else {
      setText("");
      setModalText("");
    }
  }, [inputName]);

  const onChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    localStorage.setItem(inputName, e.target.value);
    setText(e.target.value);
    setModalText(e.target.value);
  };

  const onModalChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setModalText(e.target.value);
  };

  const sendModalData = () => {
    const data = {
      inputName,
      content: modalText,
    };

    console.log(data); // Simula envio para um servidor
    closeModal();
  };

  const {
    enrichFunction,
    handleExport,
    arrowBackFunction,
    arrowForwardFunction,
  } = useIaInputHook(text);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <IAfield>
      <S.Container>
        <Title>{label}</Title>
        <ButtonsDiv>
          <S.Button onClick={arrowBackFunction} className="tooltip">
            <S.Image src={arrowLeft} />
            <span className="tooltiptext">Voltar</span>
          </S.Button>
          <S.Button onClick={arrowForwardFunction} className="tooltip">
            <S.Image src={arrowRight} />
            <span className="tooltiptext">Avançar</span>
          </S.Button>
        </ButtonsDiv>
      </S.Container>
      <TextArea value={text} onChange={onChange} placeholder={placeholder} />

      {/* DIVS DE BOTÕES */}
      <ButtonsDiv className="iaButtons">
        <S.Button onClick={enrichFunction} className="tooltip">
          <S.Image src={enrich} />
          <span className="tooltiptext">Enriquecer o texto</span>
        </S.Button>
        <S.Button onClick={openModal} className="tooltip">
          <S.Image src={adjustment} />
          <span className="tooltiptext">Fazer ajuste pontual</span>
        </S.Button>
        <S.Button
          onClick={() => handleExport(setExportTextModal)}
          className="tooltip"
        >
          <S.Image src={exportText} />
          <span className="tooltiptext">Copiar texto</span>
        </S.Button>
      </ButtonsDiv>

      {isModalOpen && (
        <ModalOverlay>
          <ModalContent>
            <S.Container>
              <S.Container style={{ width: "auto", gap: "10px" }}>
                <S.Image src={adjustment} />
                <h2>Ajustes pontuais</h2>
              </S.Container>
              <S.Button onClick={closeModal}>
                <S.Image src={closeButton} />
              </S.Button>
            </S.Container>
            <TextArea
              value={modalText}
              onChange={onModalChange}
              placeholder={placeholder}
            />
            <Button label="Enviar solicitação" onClick={sendModalData} />
          </ModalContent>
        </ModalOverlay>
      )}
      {exportTextModal && (
        <Modal closeModal={() => setExportTextModal(false)} text={text} />
      )}
    </IAfield>
  );
};

export default IATextArea;
