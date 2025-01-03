import React from "react";
import styled from "styled-components";

const MessageContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
  margin-right: 10px;
`;

const MessageTextContainer = styled.div`
  background-color: #1795a6;
  color: white;
  padding: 10px;
  border-radius: 8px;
  max-width: 50%;
  word-wrap: break-word;
  overflow-wrap: break-word;
`;

interface UserMessageProps {
  message: string;
}

export const UserMessage: React.FC<UserMessageProps> = ({ message }) => {
  return (
    <MessageContainer>
      <MessageTextContainer>{message}</MessageTextContainer>
    </MessageContainer>
  );
};
