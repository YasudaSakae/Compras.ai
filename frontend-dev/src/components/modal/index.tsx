import useIaInputHook from "../../hook/useIaInputHook";
import styled from "styled-components";
import { Button } from "../button";
import * as S from "../../components/styleComponents";

const ModalBackGround = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  z-index: 999999;
  width: 100%;
  height: 100%;
  background-color: RGBA(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
`;

const ModalContainer = styled.div`
  background-color: white;
  width: 400px;

  border-radius: 12px;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 1em;
`;

const ButtonsContainer = styled.div`
  width: 100%;
  padding: 0 px;
  display: flex;
  gap: 10px;
`;
interface ModalProps {
  closeModal: (value: boolean) => void;
  text: string;
}

export const Modal: React.FC<ModalProps> = ({ closeModal, text }) => {
  const { clipBoard } = useIaInputHook(text);

  return (
    <ModalBackGround>
      <ModalContainer>
        <S.Text className="title">
          Há um texto existente! Tem certeza que deseja substituí-lo?
        </S.Text>
        <div
          style={{
            display: "flex",
          }}
        >
          <ButtonsContainer>
            <Button
              label="Cancelar"
              onClick={() => {
                closeModal(false);
              }}
              classname="secundary"
            />
            <Button
              label="Sim"
              onClick={() => {
                clipBoard();
                closeModal(false);
              }}
            />
          </ButtonsContainer>
        </div>
      </ModalContainer>
    </ModalBackGround>
  );
};
