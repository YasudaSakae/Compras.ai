import styled from "styled-components";
import {} from "../../components/styleComponents";
import logo from "../../assets/icons/logo-compras-ia.svg";
import { Input } from "../../components/input";
import { Button } from "../../components/button";
import { useContext, useState } from "react";
import { GlobalContext } from "../../context/GlobalContext";
// import { Divider } from "../../components/divider";

const Container = styled.div`
  width: 100%;
  color: black;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`;

const ContainerLogin = styled.div`
  width: 100%;
  gap: 5em;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`;

const Image = styled.img`
  width: 100px;
`;
const Title = styled.h1`
  font-size: 2.3em;
  font-weight: 500;
  margin: 0.5em 0;
`;
const Description = styled.p`
  font-size: 1em;
  width: 80%;
  font-weight: 300;
  text-align: center;
  margin: 0.5em 0;
  opacity: 50%;
`;

const ErrorMessage = styled.span`
  color: #ff6a56;
  font-size: 0.8em;
`;

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { setCurrentPage } = useContext(GlobalContext);
  const [isError, setIsError] = useState(false);

  function onHandleLogin() {
    if (email === "admin" && password === "admin") {
      setCurrentPage("main");
    } else {
      setIsError(true);
    }
  }
  return (
    <Container style={{ height: "100vh" }}>
      <ContainerLogin>
        {/* Logo etc */}
        <Container>
          <Image src={logo} />
          <Title>Compras IA</Title>
          <Description>
            Com o Compras IA, agilidade e precisão trabalham juntas para
            potencializar suas licitações.
          </Description>
        </Container>

        {/* Buttons */}
        <Container style={{ gap: "20px", width: "80%" }}>
          <Input
            placeholder="E-mail"
            value={email}
            error={isError}
            onChange={setEmail}
          />
          <Input
            placeholder="Senha"
            error={isError}
            type="password"
            value={password}
            onChange={setPassword}
          />
          {isError && <ErrorMessage>Email ou senha inválidos</ErrorMessage>}
          <Button onClick={onHandleLogin} label="Entrar" />
        </Container>
      </ContainerLogin>
    </Container>
  );
};
