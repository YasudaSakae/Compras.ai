import styled from "styled-components";

export const Container = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-between;

  &.header {
    display: flex;
    width: auto;
    padding: 0.5em 1.5em;
    gap: 2em;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
    background-color: var(--color-whitesmoke-100);
  }
  &.logo {
    flex-direction: row;
    gap: var(--gap-8xs);
    width: 200px;
    display: flex;
    justify-content: center;
  }
`;

export const Text = styled.p`
  font-size: 0.7em;
  font-weight: lighter;
  margin: 0;
  color: black;

  &.subtitle {
    font-size: 0.8em;
    margin: 0;
    font-weight: lighter;
  }
  &.title {
    font-size: 1em;
    font-weight: bold;
    margin: 0.5em 0;
  }
`;

export const Button = styled.button<{ disabled?: boolean }>`
  cursor: pointer;
  border: 0;
  padding: 0;
  border: none;
  outline: none;
  background-color: transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: ${(props) => (props.disabled ? 0.5 : 1)};
  pointer-events: ${(props) => (props.disabled ? "none" : "auto")};
  position: relative; /* Necessário para o posicionamento absoluto do tooltip */
  margin: 10px; /* Adiciona espaçamento entre os botões */
  &:focus {
    outline: none;
  }

  &.tooltip .tooltiptext {
    visibility: hidden;
    width: auto;
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 5px;
    font-size: 12px;
    padding: 6px;
    position: absolute;
    z-index: 1;
    bottom: 125%; /* Posiciona o tooltip acima do botão */
    left: 50%;
    transform: translateX(-50%);
    opacity: 0;
    transition: opacity 0.3s;
  }

  &.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
  }
`;

export interface ImageProps {
  src: string;
}

export const Image = styled.img<ImageProps>`
  src: ${(props) => props.src};
  cursor: pointer;
  &.logo {
    width: 160px;
  }
`;

export const Input = styled.input`
  cursor: pointer;
  margin: 0;
  padding: var(--padding-11xs);
`;

export const CheckboxContainer = styled.div`
  display: flex;
  align-items: center;
`;

export const CheckboxLabel = styled.label`
  margin-left: 8px;
  font-size: var(--font-size-sm);
  color: black;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
`;

export const CheckboxInput = styled.input.attrs({ type: "checkbox" })`
  width: 16px;
  height: 16px;
  cursor: pointer;
  border-radius: 50%;
  appearance: none;
  background-color: white;
  border: 1px solid #0000005e;
  display: flex;
  align-items: center;
  justify-content: center;

  &:checked {
    background-color: #1795a6;
  }

  &:before {
    content: "";
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: white;
    display: block;
    transition: background-color 0.2s;
  }

  &:checked:before {
    background-color: #1795a6;
  }
`;

export const RadioContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

export const RadioLabel = styled.label`
  margin-left: 8px;
  font-size: var(--font-size-sm);
  color: black;
  display: flex;
  align-items: center;
  gap: 8px;
`;

export const RadioInput = styled.input.attrs({ type: "radio" })`
  width: 16px;
  height: 16px;
  cursor: pointer;
  border-radius: 50%;
  appearance: none;
  background-color: white;
  border: 1px solid #00000057;
  display: flex;
  align-items: center;
  justify-content: center;

  &:checked {
    background-color: #1795a6;
  }

  &:before {
    content: "";
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: white;
  }

  &:checked:before {
    background-color: #1795a6;
  }
`;
