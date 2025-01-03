import styled from "styled-components";
import * as S from "../../components/styleComponents";

export const Container = styled.main`
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  height: 76vh;
  display: flex;
  flex-direction: column;
  background-color: var(--color-whitesmoke-100);
  gap: 20px;
  padding: 10px 20px 80px;

  font-size: var(--font-size-sm);

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

export const TitleSection = styled.div`
  width: 100%;
  padding: 1em 0;
  border-bottom: 1px solid #e5e5ea;
`;

export const Title = styled(S.Text)`
  font-size: 1.3em;
  margin: 0.5em 0;
  font-weight: 400;
`;

export const Row = styled.div`
  display: flex;
  gap: 20px;
`;
