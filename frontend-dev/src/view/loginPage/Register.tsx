import styled from "styled-components";
import { } from "../../components/styleComponents";
import logo from "../../assets/icons/logo-compras-ia.svg";
import { Button } from "../../components/button";
import { Divider } from "../../components/divider";

const Container = styled.div`
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
`

const ContainerLogin = styled.div`
    width: 100%;
    gap: 5em;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
`

const Image = styled.img`
    width: 100px;
`
const Title = styled.h1`
    font-size: 2.3em;
    font-weight: 500;
    margin: 0.5em 0;
`
const Description = styled.p`
    font-size: 1em;
    width: 80%;
    font-weight: 300;
    text-align: center;
    margin: 0.5em 0;
    opacity: 50%;
`

export const Register = () => {
    return (
        <Container style={{ height: "100vh" }}>
            <ContainerLogin>
                {/* Logo etc */}
                <Container>
                    <Image src={logo} />
                    <Title>Compras IA</Title>
                    <Description>Com o Compras IA, agilidade e precisão trabalham juntas para potencializar suas licitações.</Description>
                </Container>

                {/* Buttons */}
                <Container style={{ gap: "10px", width: "80%" }}>
                    <Button label="Criar conta" />
                    <Divider />
                    <Button label="Entrar" classname="secundary" />
                </Container>
            </ContainerLogin>
        </Container>
    )
};