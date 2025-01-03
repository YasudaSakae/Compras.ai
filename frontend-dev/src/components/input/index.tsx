import { ChangeEvent } from "react";
import styled from "styled-components";

const InputStyle = styled.input`
  width: 100%;
  background-color: white;
  color: black;
  border-radius: 12px;
  border: 1px solid #afafaf;
  font-family: var(--font-lexend);
  box-sizing: border-box;
  height: 60px;
  padding: 0 1.5em;

  &:focus {
    border: 1px solid #198998;
    outline-color: #198998;
  }

  &::placeholder {
    color: #afafaf;
  }

  &.error {
    border: 1px solid #ff6a56;
    outline-color: #ff6a56;
  }
`;

interface InputProps {
  placeholder?: string;
  type?: string;
  value: string;
  onChange: (value: string) => void;
  error?: boolean;
}

export const Input = ({
  placeholder,
  type,
  value,
  onChange,
  error,
}: InputProps) => {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  return (
    <div
      style={{
        display: "flex",
        width: "100%",
        flexDirection: "column",
        gap: "10px",
      }}
    >
      <InputStyle
        className={error ? "error" : ""}
        type={type || "text"}
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
      />
    </div>
  );
};
