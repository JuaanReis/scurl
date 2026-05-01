# Instalação

## Requisitos

Antes de instalar o projeto, certifique-se de que os seguintes requisitos estão instalados no sistema:

* **Python 3.11 ou superior**
* **Git**
* **pip** (gerenciador de pacotes do Python)

Para verificar a versão do Python instalada, execute:

```bash
python --version
```

ou

```bash
python3 --version
```

---

# Windows

## 1. Instalar o Python

Baixe o Python no site oficial: *https://www.python.org/downloads/*

Durante a instalação, **marque a opção**:

```
Add Python to PATH
```

Após a instalação, verifique se o Python foi instalado corretamente:

```bash
python --version
```

---

## 2. Clonar o repositório

```bash
git clone https://github.com/JuaanReis/scurl.git
cd scurl
```

---

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Iniciar o servidor

```bash
uvicorn app.main:app --reload
```

---

# Linux

## Debian / Ubuntu

### 1. Instalar dependências do sistema

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

---

### 2. Clonar o repositório

```bash
git clone https://github.com/JuaanReis/scurl.git
cd scurl
```

---

### 3. Instalar dependências do projeto

```bash
pip3 install -r requirements.txt
```

---

### 4. Iniciar o servidor

```bash
uvicorn app.main:app --reload
```

---

## Arch Linux

### 1. Instalar dependências do sistema

```bash
sudo pacman -S python python-pip git
```

---

### 2. Clonar o repositório

```bash
git clone https://github.com/JuaanReis/scurl.git
cd scurl
```

---

### 3. Instalar dependências do projeto

```bash
pip install -r requirements.txt
```

---

### 4. Iniciar o servidor

```bash
uvicorn app.main:app --reload
```

---

# macOS

## 1. Instalar dependências do sistema

Utilizando **Homebrew**:

```bash
brew install python git
```

Se o Homebrew não estiver instalado, consulte: *https://brew.sh/*

---

## 2. Clonar o repositório

```bash
git clone https://github.com/JuaanReis/scurl.git
cd scurl
```

---

## 3. Instalar dependências do projeto

```bash
pip3 install -r requirements.txt
```

---

## 4. Iniciar o servidor

```bash
uvicorn app.main:app --reload
```

---

# Acessando a aplicação

Após iniciar o servidor, abra o navegador e acesse:

```
http://localhost:8000
```

---

# Observações para desenvolvimento

A flag `--reload` ativa o **auto-reload**, fazendo com que o servidor reinicie automaticamente sempre que houver alterações no código.
Esse modo é recomendado apenas para ambiente de desenvolvimento.
