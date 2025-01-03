import { Container, Title } from "./styles";
import FileInput from "../../components/fileInput";
import { useContext, useState } from "react";
import { Button } from "../../components/button";
import { GlobalContext } from "../../context/GlobalContext";

export const SEIPage = () => {
  const [files, setFiles] = useState<File[]>([]);

  const { setSeiCount } = useContext(GlobalContext);

  return (
    <Container
      style={{
        height: "86vh",
      }}
    >
      <Title>Documentos relacionados a este processo</Title>
      <FileInput
        id="file-input-1"
        setCount={setSeiCount}
        label="Adicionar documento"
        setFiles={setFiles}
        files={files}
        multiple={true}
      />

      <Button
        label="Salvar ajustes do sistema"
        onClick={() => {
          console.log(files);
        }}
      />
    </Container>
  );
};
