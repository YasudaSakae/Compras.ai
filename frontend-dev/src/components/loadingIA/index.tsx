import React from "react";
import styled, { keyframes } from "styled-components";
import loadingIcon from "../../assets/icons/logo-compras-ia.svg"; // Altere o caminho conforme necessário

// Animação de fade-in/out
// const blink = keyframes`
//   0% { opacity: 1; }
//   50% { opacity: 0.5; }
//   100% { opacity: 1; }
// `;

const gradientAnimation = keyframes`
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 100% 50%;
  }
`;

const LoadingContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-family: Arial, sans-serif;
  font-size: 1.2em;
  color: #000;
`;

const LoadingText = styled.span`
  background-image: linear-gradient(90deg, #1ccce3, #000000);
  background-size: 200% 100%; // Faz o gradiente ser maior que o texto para criar o efeito de movimento
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  animation: ${gradientAnimation} 1s infinite alternate;
  font-size: 14px;
`;

const Icon = styled.img`
  width: 30px;
  height: 30px;
`;

interface LoadingProps {
  message?: string;
  iconSrc?: string;
}

export const Loading: React.FC<LoadingProps> = ({
  message = "Buscando na base de conhecimento...",
  iconSrc = loadingIcon,
}) => {
  return (
    <LoadingContainer>
      <Icon src={iconSrc} alt="Loading Icon" />
      <LoadingText>{message}</LoadingText>
    </LoadingContainer>
  );
};
