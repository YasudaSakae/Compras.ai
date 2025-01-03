import React from "react";
import {
  CheckboxContainer,
  CheckboxInput,
  CheckboxLabel,
} from "../styleComponents";

interface CheckboxProps {
  value: boolean | null;
  onChange: (value: boolean) => void;
}

export const CheckBoxS: React.FC<CheckboxProps> = ({ value, onChange }) => (
  <CheckboxContainer>
    <CheckboxLabel>
      <CheckboxInput
        type="radio"
        checked={value === true}
        onChange={() => onChange(true)}
      />
      Sim
    </CheckboxLabel>
    <CheckboxLabel>
      <CheckboxInput
        type="radio"
        checked={value === false}
        onChange={() => onChange(false)}
      />
      Não
    </CheckboxLabel>
  </CheckboxContainer>
);
