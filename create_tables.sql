-- Script SQL para criação das tabelas no PostgreSQL

-- Tabela Usuario
CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    nivel_permissao VARCHAR(50)
);

-- Tabela Aluno
CREATE TABLE Aluno (
    id SERIAL PRIMARY KEY,
    matricula VARCHAR(50) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    possui_necessidade_especial BOOLEAN DEFAULT FALSE,
    documento_identidade VARCHAR(50),
    usuario_id INT UNIQUE NOT NULL REFERENCES Usuario(id),
    ponto_embarque_preferencial_id INT -- FK para PontoDeParada, será adicionado após a criação da tabela PontoDeParada
);

-- Tabela Motorista
CREATE TABLE Motorista (
    id SERIAL PRIMARY KEY,
    cnh VARCHAR(20) UNIQUE NOT NULL,
    data_admissao DATE NOT NULL,
    status_ativo BOOLEAN DEFAULT TRUE,
    usuario_id INT UNIQUE NOT NULL REFERENCES Usuario(id)
);

-- Tabela Veiculo
CREATE TABLE Veiculo (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(10) UNIQUE NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    capacidade_passageiros INT NOT NULL,
    status_manutencao VARCHAR(50),
    adaptado_pcd BOOLEAN DEFAULT FALSE,
    ano_fabricacao INT
);

-- Tabela Rota
CREATE TABLE Rota (
    id SERIAL PRIMARY KEY,
    nome_rota VARCHAR(255) NOT NULL,
    descricao TEXT,
    turno VARCHAR(50) NOT NULL,
    limite_atrasos_semanal INT DEFAULT 0,
    ativa BOOLEAN DEFAULT TRUE
);

-- Tabela PontoDeParada
CREATE TABLE PontoDeParada (
    id SERIAL PRIMARY KEY,
    nome_ponto VARCHAR(255) NOT NULL,
    endereco TEXT,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    ordem INT NOT NULL,
    rota_id INT NOT NULL REFERENCES Rota(id)
);

-- Adicionar FK ponto_embarque_preferencial_id na tabela Aluno
ALTER TABLE Aluno
ADD CONSTRAINT fk_ponto_embarque_preferencial
FOREIGN KEY (ponto_embarque_preferencial_id)
REFERENCES PontoDeParada(id);

-- Tabela Viagem
CREATE TABLE Viagem (
    id SERIAL PRIMARY KEY,
    data_viagem DATE NOT NULL,
    hora_partida TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    vagas_ocupadas INT DEFAULT 0,
    rota_id INT NOT NULL REFERENCES Rota(id),
    motorista_id INT NOT NULL REFERENCES Motorista(id),
    veiculo_id INT NOT NULL REFERENCES Veiculo(id)
);

-- Tabela RegistroFrequencia
CREATE TABLE RegistroFrequencia (
    id SERIAL PRIMARY KEY,
    data_hora_embarque TIMESTAMP NOT NULL,
    tipo_registro VARCHAR(50) NOT NULL,
    viagem_id INT NOT NULL REFERENCES Viagem(id),
    aluno_id INT NOT NULL REFERENCES Aluno(id)
);

-- Tabela Incidente
CREATE TABLE Incidente (
    id SERIAL PRIMARY KEY,
    descricao TEXT,
    tipo_incidente VARCHAR(100),
    data_hora_registro TIMESTAMP NOT NULL,
    status_resolucao VARCHAR(50),
    viagem_id INT NOT NULL REFERENCES Viagem(id),
    reportado_por_usuario_id INT NOT NULL REFERENCES Usuario(id)
);