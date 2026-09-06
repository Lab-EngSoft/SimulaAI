-- =====================================================================
-- Sistema: SimulaAI
-- Arquivo: schema.sql
-- Descrição: Script DDL para criação do banco de dados relacional baseado 
--            no Modelo Entidade-Relacionamento (UML) e no Backlog do Projeto.
-- Integrantes: 
--   - Gabriel Reis de Souza (2840482421005)
--   - Cesar Augusto Saraiva Fifolato (2840482421022)
--   - Davi Sousa Cirilo (2840482421006)
--   - Vinicius Brasileiro Veras (2840482421021)
-- =====================================================================

-- Criação do Banco de Dados (Opcional, descomentar se necessário)
-- CREATE DATABASE simulaai;
-- USE simulaai;

-- -----------------------------------------------------
-- Tabela: USUARIO
-- Suporta o Requisito 1 (Perfis: Aluno e Administrador, Autenticação)
-- -----------------------------------------------------
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    perfil VARCHAR(50) NOT NULL CHECK (perfil IN ('ALUNO', 'ADMINISTRADOR')),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Tabela: MATERIA
-- Suporta o Requisito 2 (Cadastro e gerenciamento de matérias)
-- -----------------------------------------------------
CREATE TABLE materia (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    descricao TEXT
);

-- -----------------------------------------------------
-- Tabela: ASSUNTO
-- Suporta o Requisito 2 (Cadastro e gerenciamento de assuntos vinculados a matérias)
-- -----------------------------------------------------
CREATE TABLE assunto (
    id SERIAL PRIMARY KEY,
    materia_id INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    CONSTRAINT fk_assunto_materia FOREIGN KEY (materia_id) 
        REFERENCES materia(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tabela: QUESTAO
-- Suporta o Requisito 3 (Cadastro de questões classificadas por assunto)
-- -----------------------------------------------------
CREATE TABLE questao (
    id SERIAL PRIMARY KEY,
    assunto_id INT NOT NULL,
    enunciado TEXT NOT NULL,
    nivel_dificuldade VARCHAR(30),
    CONSTRAINT fk_questao_assunto FOREIGN KEY (assunto_id) 
        REFERENCES assunto(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tabela: ALTERNATIVA
-- Suporta o Requisito 3 (Alternativas de múltipla escolha com indicação de correta)
-- -----------------------------------------------------
CREATE TABLE alternativa (
    id SERIAL PRIMARY KEY,
    questao_id INT NOT NULL,
    texto TEXT NOT NULL,
    correta BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_alternativa_questao FOREIGN KEY (questao_id) 
        REFERENCES questao(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tabela: SIMULADO
-- Suporta o Requisito 4 (Estrutura de um simulado)
-- -----------------------------------------------------
CREATE TABLE simulado (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Tabela Associativa: SIMULADO_QUESTAO
-- Relaciona Simulado e Questão (muitos para muitos)
-- -----------------------------------------------------
CREATE TABLE simulado_questao (
    simulado_id INT NOT NULL,
    questao_id INT NOT NULL,
    PRIMARY KEY (simulado_id, questao_id),
    CONSTRAINT fk_sq_simulado FOREIGN KEY (simulado_id) 
        REFERENCES simulado(id) ON DELETE CASCADE,
    CONSTRAINT fk_sq_questao FOREIGN KEY (questao_id) 
        REFERENCES questao(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tabela: TENTATIVA
-- Suporta os Requisitos 4, 6, 8, 9, 10 (Registro de simulado realizado pelo aluno)
-- -----------------------------------------------------
CREATE TABLE tentativa (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    simulado_id INT NOT NULL,
    data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_fim TIMESTAMP,
    acertos INT DEFAULT 0,
    erros INT DEFAULT 0,
    percentual_aproveitamento NUMERIC(5,2) DEFAULT 0.00,
    status VARCHAR(30) DEFAULT 'EM_ANDAMENTO' CHECK (status IN ('EM_ANDAMENTO', 'FINALIZADO')),
    CONSTRAINT fk_tentativa_usuario FOREIGN KEY (usuario_id) 
        REFERENCES usuario(id) ON DELETE CASCADE,
    CONSTRAINT fk_tentativa_simulado FOREIGN KEY (simulado_id) 
        REFERENCES simulado(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tabela: RESPOSTA
-- Suporta os Requisitos 5, 6, 7 (Armazena a resposta escolhida pelo aluno e feedback/explicação da IA)
-- -----------------------------------------------------
CREATE TABLE resposta (
    id SERIAL PRIMARY KEY,
    tentativa_id INT NOT NULL,
    questao_id INT NOT NULL,
    alternativa_id INT NOT NULL,
    correta BOOLEAN NOT NULL,
    explicacao_ia TEXT, -- Suporta o Requisito 7 (Explicação da IA em caso de erro ou consulta)
    CONSTRAINT fk_resposta_tentativa FOREIGN KEY (tentativa_id) 
        REFERENCES tentativa(id) ON DELETE CASCADE,
    CONSTRAINT fk_resposta_questao FOREIGN KEY (questao_id) 
        REFERENCES questao(id) ON DELETE CASCADE,
    CONSTRAINT fk_resposta_alternativa FOREIGN KEY (alternativa_id) 
        REFERENCES alternativa(id) ON DELETE CASCADE
);

-- =====================================================================
-- FIM DO SCRIPT DDL
-- =====================================================================