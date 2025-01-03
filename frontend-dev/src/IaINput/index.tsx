import React from "react";
import styled from "styled-components";

const StyledInput = styled.input`
  border: 1px solid #b1b1b1;
  width: 100%;
  resize: none;
  background-color: transparent;
  outline: 0;
  border-radius: var(--br-9xs);
  box-sizing: border-box;
  overflow-y: auto;
  flex-shrink: 0;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 1.4em 0.5em;
  font-family: var(--font-lexend);
  font-size: var(--font-size-xs);
  color: #686868;
  min-width: 250px;
`;

const Label = styled.h2`
  font-size: 1.3em;
  margin: 0.5em 0;
  font-weight: 400;
  color: black;
`;

interface IAInputProps {
  value: string;
  setValue: (value: string) => void;
  label: string;
  inputName: string;
}

const IAInput: React.FC<IAInputProps> = ({
  value,
  setValue,
  label,
  inputName,
}) => {
  function handleOnChange(e: React.ChangeEvent<HTMLInputElement>) {
    localStorage.setItem(inputName, e.target.value);
    setValue(e.target.value);
  }
  return (
    <div>
      <Label>{label}</Label>
      <StyledInput
        id="exampleInput"
        type="text"
        placeholder="Ex: 50 unidades"
        value={value}
        onChange={handleOnChange}
      />
    </div>
  );
};

export default IAInput;
