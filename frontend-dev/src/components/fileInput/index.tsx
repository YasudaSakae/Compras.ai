import React, { useState, useEffect } from "react";
import styled from "styled-components";

const StyledFileInput = styled.input`
  display: none;
`;

const RowContainer = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: space-between;
`;

const StyledLabel = styled.label`
  font-size: 16px;
  color: #333;
`;

const FileButton = styled.label`
  background-color: #1795a6;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  &:hover {
    background-color: #137a8a;
  }
`;

const FileNameContainer = styled.div`
  display: flex;
  align-items: center;
  margin: 5px;
  font-size: 13px;
  color: #333;
  background-color: #1795a6;
  padding: 0px 15px;
  border-radius: 30px;
  flex-wrap: nowrap;
`;

const FileName = styled.span`
  margin-right: 10px;
  color: white;
`;

const RemoveButton = styled.button`
  background-color: transparent;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
`;

const Container = styled.div`
  border: 2px dashed #ccc;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  text-align: center;
  max-height: 150px;
  overflow-y: auto;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: #adadad;
  }

  &::-webkit-scrollbar-thumb {
    background: #808080;
    border-radius: 10px;
  }
`;

const FileNamesWrapper = styled.div`
  display: flex;
  flex-wrap: wrap;
`;

const Description = styled.p`
  font-size: 1em;
  color: #b0b0b0;
  margin: 0;
`;

interface FileInputProps {
  id: string;
  label: string;
  setFiles: (files: File[]) => void;
  setCount?: React.Dispatch<React.SetStateAction<number>>;
  files?: File[];
  multiple?: boolean;
}

const FileInput: React.FC<FileInputProps> = ({
  id,
  label,
  setFiles,
  setCount,
  files = [],
  multiple = true,
}) => {
  const [fileNames, setFileNames] = useState<string[]>(
    files.map((file) => file.name)
  );
  const [dragActive, setDragActive] = useState<boolean>(false);

  useEffect(() => {
    setFileNames(files.map((file) => file.name));
  }, [files]);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const newFiles = Array.from(event.target.files);
      setFileNames(newFiles.map((file) => file.name));
      setFiles(newFiles);
      if (setCount) {
        setCount((prev) => prev + newFiles.length);
      }
    } else {
      if (setCount) {
        setCount((prev) => prev - files.length);
      }
      setFileNames([]);
      setFiles([]);
    }
  };

  const handleRemove = (fileName: string) => {
    const updatedFiles = files.filter((file) => file.name !== fileName);
    setFileNames(updatedFiles.map((file) => file.name));
    setFiles(updatedFiles);
    if (setCount) {
      setCount((prev) => prev - 1);
    }
  };

  const handleDrag = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    if (event.type === "dragenter" || event.type === "dragover") {
      setDragActive(true);
    } else if (event.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(false);
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      const newFiles = Array.from(event.dataTransfer.files);
      setFileNames(newFiles.map((file) => file.name));
      setFiles(newFiles);
      if (setCount) {
        setCount((prev) => prev + newFiles.length);
      }
    }
  };

  return (
    <>
      <StyledLabel>{label}</StyledLabel>
      <Container
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        style={{ borderColor: dragActive ? "#1795a6" : "#ccc" }}
      >
        {fileNames.length === 0 && (
          <RowContainer>
            <Description>
              Escolha um arquivo ou arraste e solte-o aqui.
            </Description>
            <StyledFileInput
              id={id}
              type="file"
              multiple={multiple}
              onChange={handleChange}
            />
            <FileButton htmlFor={id}>Selecione um arquivo</FileButton>
          </RowContainer>
        )}
        {fileNames.length > 0 && (
          <FileNamesWrapper>
            {fileNames.map((fileName, index) => (
              <FileNameContainer key={index}>
                <FileName>{fileName}</FileName>
                <RemoveButton onClick={() => handleRemove(fileName)}>
                  X
                </RemoveButton>
              </FileNameContainer>
            ))}
          </FileNamesWrapper>
        )}
      </Container>
    </>
  );
};

export default FileInput;
