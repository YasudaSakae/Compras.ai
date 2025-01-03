import styled from "styled-components"

const FooterDiv = styled.footer`
    width: auto;
    background-color: var(--color-whitesmoke-100);
    flex-direction: row;
    padding: var(--padding-5xs);
    border-top: 1px solid #00000020;
    text-align: center;
`

const FooterText = styled.p`
    font-size: 10px;
    color: var(--color-black-100);
    margin: 0;
`

export function Footer() {
    return (
        <FooterDiv>
            <FooterText>
                O Compras IA pode cometer erros. Considere verificar as informações
                antes de utilizá-las nos processos licitatórios.
            </FooterText>
        </FooterDiv>
    )
}