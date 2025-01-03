import { Container, Title } from "./styles";
import FileInput from "../../components/fileInput";
import { useState } from "react";
import { Button } from "../../components/button";

export const ConfigPage = () => {
  const [PEIFile, setPEIFile] = useState<File | null>(null);
  const [PDTICFile, setPDTICFile] = useState<File | null>(null);
  const [vigentYearFile, setVigentYearFile] = useState<File | null>(null);
  const [othersFiles, setOthersFiles] = useState<File[]>([]);

  const handleSetFile =
    (setFile: React.Dispatch<React.SetStateAction<File | null>>) =>
      (files: File[]) => {
        setFile(files[0] || null);
      };

  const handleSetMultipleFiles = (files: File[]) => {
    setOthersFiles(files);
  };

  return (
    <Container
      style={{
        height: "86vh",
        padding: "20px",

      }}
    >
      <Title>Configurações</Title>
      <FileInput
        id="file-input-config-1"
        label="Plano estratégico institucional (PEI)"
        setFiles={handleSetFile(setPEIFile)}
        files={PEIFile ? [PEIFile] : []}
        multiple={false}
      />
      <FileInput
        id="file-input-config-2"
        label="Plano diretor de TIC (PDTIC)"
        setFiles={handleSetFile(setPDTICFile)}
        files={PDTICFile ? [PDTICFile] : []}
        multiple={false}
      />
      <FileInput
        id="file-input-config-3"
        label="Ano vigente"
        setFiles={handleSetFile(setVigentYearFile)}
        files={vigentYearFile ? [vigentYearFile] : []}
        multiple={false}
      />
      <FileInput
        id="file-input-config-4"
        label="Outros"
        setFiles={handleSetMultipleFiles}
        files={othersFiles}
        multiple={true}
      />

      <Button
        label="Salvar ajustes do sistema"
        onClick={() => {
          console.log(PEIFile);
          console.log(PDTICFile);
          console.log(vigentYearFile);
          console.log(othersFiles);
        }}
      />
    </Container>
  );
};
