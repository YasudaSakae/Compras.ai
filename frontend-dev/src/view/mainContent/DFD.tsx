import { useState } from "react";
import { CheckBoxS } from "../../components/checkbox";
import { IATextArea } from "../../components/iaTextArea";
import { Container, Title, TitleSection } from "./styles";
import { RadioGroup } from "../../components/radioGroup";
import IAInput from "../../IaINput";

type sideBarOption = {
  title: string;
  sideBarOption: string;
};

interface DFDProps {
  sideBarOption: sideBarOption;
}

export const DFD: React.FC<DFDProps> = ({ sideBarOption }) => {
  const [checkboxStates, setCheckboxStates] = useState({
    essentialsTecCheckbox: false,
    alternativesCheckbox: false,
    especificModelCheckbox: false,
    sustentabilityCheckbox: false,
    restricitionsCheckbox: false,
    hasRestrictions: false,
  });
  const [radioValue, setRadioValue] = useState("height");
  const [valuesInputNumber, setValuesInputNumber] = useState("");
  const handleChange = (checkboxName: string, value: boolean) => {
    setCheckboxStates((prevState) => ({
      ...prevState,
      [checkboxName]: value,
    }));
  };

  return (
    <Container>
      <TitleSection>
        <Title>{sideBarOption.title}</Title>
      </TitleSection>
      <IATextArea
        inputName={sideBarOption.sideBarOption + 1}
        label="Descrição sucinta do objeto"
      />
      <Title>Especificações técnicas essenciais</Title>
      <CheckBoxS
        value={checkboxStates.essentialsTecCheckbox}
        onChange={(value) => handleChange("essentialsTecCheckbox", value)}
      />

      {checkboxStates.essentialsTecCheckbox && (
        <IATextArea
          inputName={sideBarOption.sideBarOption}
          label="Especificação"
        />
      )}
      <Title>Justificativa de necessidade</Title>
      <IATextArea
        inputName={sideBarOption.sideBarOption + 2}
        label="Problema ou necessidade a ser solucionado"
      />
      <IATextArea
        inputName={sideBarOption.sideBarOption + 3}
        label="Impacto da contração"
      />

      <Title>Alternativas avaliadas</Title>
      <CheckBoxS
        value={checkboxStates.alternativesCheckbox}
        onChange={(value) => handleChange("alternativesCheckbox", value)}
      />
      {checkboxStates.alternativesCheckbox && (
        <IATextArea
          inputName={sideBarOption.sideBarOption + 4}
          label="Justificativa"
        />
      )}

      <Title>Necessidade de marca ou modelo específico?</Title>
      <CheckBoxS
        value={checkboxStates.especificModelCheckbox}
        onChange={(value) => handleChange("especificModelCheckbox", value)}
      />
      {checkboxStates.especificModelCheckbox && (
        <IATextArea
          inputName={sideBarOption.sideBarOption + 5}
          label="Descreva a necessidade"
        />
      )}
      <Title>Urgência ou prioridade?</Title>

      <RadioGroup
        name="radioGroup"
        options={[
          { label: "Alto", value: "height" },
          { label: "Médio", value: "medium" },
          { label: "Baixo", value: "low" },
        ]}
        selectedValue={radioValue}
        onChange={(value) => setRadioValue(value)}
      />
      {radioValue.includes("height") && (
        <IATextArea
          inputName={sideBarOption.sideBarOption + 6}
          label="Justifique"
        />
      )}

      <IATextArea
        inputName={sideBarOption.sideBarOption + 7}
        label="Base legal associada à contratação"
      />
      <Title>Sustenbilidade</Title>
      <Title>Critérios de sustentabilidade aplicáveis?</Title>
      <CheckBoxS
        value={checkboxStates.sustentabilityCheckbox}
        onChange={(value) => handleChange("sustentabilityCheckbox", value)}
      />
      {checkboxStates.sustentabilityCheckbox && (
        <IATextArea
          inputName={sideBarOption.sideBarOption + 8}
          label="Descreva os critérios"
        />
      )}
      <IATextArea
        inputName={sideBarOption.sideBarOption + 9}
        label="Impactos ambientais positivos ou mitigatórios"
      />
      <IAInput
        label="Valor estimado"
        setValue={setValuesInputNumber}
        inputName={sideBarOption.sideBarOption + "number"}
        value={valuesInputNumber}
      />

      <IATextArea
        inputName={sideBarOption.sideBarOption + 10}
        label="Frequência ou prazo de execução"
      />
      <Title>Restrições ou vedações</Title>
      <Title>
        O serviço solicitado está relacionado às atribuições de cargos internos?
      </Title>
      <CheckBoxS
        value={checkboxStates.restricitionsCheckbox}
        onChange={(value) => handleChange("restricitionsCheckbox", value)}
      />
      {checkboxStates.restricitionsCheckbox && (
        <IATextArea
          inputName={sideBarOption.sideBarOption + 11}
          label="Justifique a necessidade"
        />
      )}

      <Title>
        Existem restrições a fornecedores, marcas ou modelos específicos?
      </Title>
      <CheckBoxS
        value={checkboxStates.hasRestrictions}
        onChange={(value) => handleChange("hasRestrictions", value)}
      />
      {checkboxStates.hasRestrictions && (
        <IATextArea
          inputName={sideBarOption.sideBarOption + 12}
          label="Descreva as restrições"
        />
      )}
    </Container>
  );
};
