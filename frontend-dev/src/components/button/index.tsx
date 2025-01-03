import styled from "styled-components";

const ButtonStyle = styled.button`
  cursor: pointer;
  border: 0;
  height: 48px;
  border-radius: 12px;
  border: none;
  outline-style: none;
  background-color: #198998;
  color: white;
  font-size: 1em;
  font-weight: normal;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;

  &:focus {
    outline: none;
  }

  &:hover {
    background-color: #1faabd;
  }

  &.secundary {
    background-color: transparent;
    border: #198998 1px solid;
    color: #198998;
  }

  &.secundary:hover {
    background-color: #198998;
    color: white;
  }
`;

interface ButtonProps {
  disabled?: boolean;
  classname?: string;
  label: string;
  onClick?: () => void;
}

export const Button = ({ label, classname, onClick }: ButtonProps) => {
  return (
    <ButtonStyle onClick={onClick} className={classname}>
      {label}
    </ButtonStyle>
  );
};
