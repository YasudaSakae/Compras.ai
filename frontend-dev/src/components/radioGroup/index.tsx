import React from "react";
import { RadioContainer, RadioLabel, RadioInput } from "../styleComponents";

interface RadioGroupProps {
  name: string;
  options: { label: string; value: string }[];
  selectedValue: string;
  onChange: (value: string) => void;
}

export const RadioGroup: React.FC<RadioGroupProps> = ({
  name,
  options,
  selectedValue,
  onChange,
}) => (
  <RadioContainer>
    {options.map((option) => (
      <RadioLabel key={option.value}>
        <RadioInput
          name={name}
          value={option.value}
          checked={selectedValue === option.value}
          onChange={() => onChange(option.value)}
        />
        {option.label}
      </RadioLabel>
    ))}
  </RadioContainer>
);
