import { Container, Title, TitleSection } from "./styles";

import { IATextArea } from "../../components/iaTextArea";

type sideBarOption = {
  title: string;
  sideBarOption: string;
};
interface ETPProps {
  sideBarOption: sideBarOption;
}

export const ETP: React.FC<ETPProps> = ({ sideBarOption }) => {
  return (
    <Container>
      <TitleSection>
        <Title>{sideBarOption.title}</Title>
      </TitleSection>
      <IATextArea
        inputName={sideBarOption.sideBarOption + 13}
        label="Descrição da necessidade"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 14}
        label="Descrição dos requisitos de contratação"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 15}
        label="Levantamento de mercado"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 16}
        label="Descrição da solução como um todo"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 17}
        label="Justificativa para parcelamento ou não da solução"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 18}
        label="Contratações correlatas e/ou interdependentes"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 19}
        label="Alinhamento entre a contratação e o planejamento"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 20}
        label="Resultados pretendidos"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 21}
        label="Providências a serem adotadas"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 22}
        label="Possíveis impactos ambientais"
      />
    </Container>
  );
};
