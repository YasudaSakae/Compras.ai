import React from "react";
import styled from "styled-components";
import IALogo from "../../assets/icons/logo-compras-ia.svg";

const MessageContainer = styled.div`
  display: flex;
  align-items: flex-start; /* Alinha os itens ao topo */
`;

const TypingIcon = styled.span`
  font-size: 20px;
  color: #1795a6;
  margin-right: 10px;
`;

const MessageTextContainer = styled.div`
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  max-width: 50%;
  color: black;
  background-color: transparent;
  word-wrap: break-word;
  overflow-wrap: break-word;
  background-color: #fff;
`;

const Logo = styled.img`
  width: 30px;
  height: 30px;
`;

interface IaMessageProps {
  message: string;
}

export const IaMessage: React.FC<IaMessageProps> = ({ message }) => {
  return (
    <MessageContainer>
      <TypingIcon>
        <Logo src={IALogo} alt="IA Logo" />
      </TypingIcon>
      <MessageTextContainer>{message}</MessageTextContainer>
    </MessageContainer>
  );
};
