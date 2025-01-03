import { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import { Container, Row } from "./styles";
import { IaMessage } from "../../components/messages/IaMessage";
import { UserMessage } from "../../components/messages/UserMessage";
import { Loading } from "../../components/loadingIA";
import IaButton from "../../assets/icons/buttons/sendButton.svg";



const MessageContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
  height: 100%;

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

const InputContainer = styled.div`
  display: flex;
  width: 100%;
  padding-top: 10px;
  margin-top: 10px;
`;

const Input = styled.input`
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-right: 10px;
  background-color: white;
  color: black;

  &:focus {
    border-color: #1795a6;
    outline: none;
  }
`;

const SendButton = styled.button`
  padding: 10px;
  background-color: #1795a6;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  &:focus {
    outline: none;
  }
  &:active {
    outline: none;
  }
`;

type Message = {
  text: string;
  isUser: boolean;
  timestamp: string;
};

export const AssistPage = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await fetch("http://localhost:3001/mock-conversation");
        const data = await response.json();
        setMessages(data.messages);
      } catch (error) {
        console.error("Erro ao buscar mensagens:", error);
      }
    };

    fetchMessages();
  }, []);

  useEffect(() => {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === "") return;

    const timestamp = new Date().toISOString();
    const userMessage = { text: inputValue, isUser: true, timestamp };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputValue("");

    const loadingMessage = {
      text: "Carregando...",
      isUser: false,
      timestamp: new Date().toISOString(),
    };
    setMessages((prevMessages) => [...prevMessages, loadingMessage]);

    try {
      const response = await fetch("http://localhost:3001/test", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputValue, timestamp }),
      });

      const data = await response.json();
      const iaMessage = {
        text: data.message,
        isUser: false,
        timestamp: new Date().toISOString(),
      };

      setTimeout(() => {
        setMessages((prevMessages) => {
          const updatedMessages = prevMessages.filter(
            (msg) => msg.text !== "Carregando..."
          );
          return [...updatedMessages, iaMessage];
        });
      }, 2000);
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);
    }
  };

  return (
    <Container
      style={{
        height: "85vh",
        padding: "20px",
      }}
    >

      <MessageContainer>
        {messages.map((message, index) =>
          message.isUser ? (
            <UserMessage key={index} message={message.text} />
          ) : message.text === "Carregando..." ? (
            <Row>
              <Loading key={index} />
            </Row>
          ) : (
            <IaMessage key={index} message={message.text} />
          )
        )}
        <div ref={messagesEndRef} />
      </MessageContainer>
      <InputContainer>
        <Input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Digite sua mensagem..."
        />
        <SendButton onClick={handleSendMessage}>
          <img src={IaButton} alt="Enviar" />
        </SendButton>
      </InputContainer>

    </Container>
  );
};
