import { useContext, useState } from "react";
import comprasIaLogo from "../../assets/icons/comprasIaLogo.svg";
// import close from "../../assets/icons/buttons/closeButton.svg"
import profile from "../../assets/icons/buttons/profileButton.svg";
import * as S from "../styleComponents";
import styled from "styled-components";
import { GlobalContext } from "../../context/GlobalContext";

const HeaderContainer = styled(S.Container)`
  display: flex;
  padding: 0em 6em 0em 1.5em;
  gap: 2em;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  background-color: var(--color-whitesmoke-100);
`;

const LogoContainer = styled(S.Container)`
  flex-direction: row;
  gap: var(--gap-8xs);
  width: 200px;
  display: flex;
  justify-content: center;
`;

const ProfileContainer = styled.div`
  position: relative;
`;

const ProfileMenu = styled.div`
  position: absolute;
  top: 100%; /* Posiciona o menu logo abaixo do botão de perfil */
  right: 0;
  background-color: white;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1000; /* Garante que o menu fique acima de outros elementos */
`;

const MenuButton = styled.button`
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 10px;
  font-size: 16px;
  color: black;
  &:hover {
    background-color: #f0f0f0;
  }
`;

function createNewTab() { }

export function Header() {
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);

  const { setCurrentPage } = useContext(GlobalContext);

  const toggleProfileMenu = () => {
    setIsProfileMenuOpen(!isProfileMenuOpen);
  };

  function onLogout() {
    setCurrentPage("login");
  }

  return (
    <S.Container style={{ height: "auto" }}>
      <HeaderContainer>
        <S.Container>
          <S.Button onClick={createNewTab}></S.Button>
          <LogoContainer>
            <S.Image className="logo" src={comprasIaLogo} />
          </LogoContainer>
          <ProfileContainer>
            <S.Button onClick={toggleProfileMenu}>
              <S.Image src={profile} style={{ width: "40px" }} />
            </S.Button>
            {isProfileMenuOpen && (
              <ProfileMenu>
                <MenuButton onClick={onLogout}>Sair</MenuButton>
              </ProfileMenu>
            )}
          </ProfileContainer>
        </S.Container>
      </HeaderContainer>
    </S.Container>
  );
}
