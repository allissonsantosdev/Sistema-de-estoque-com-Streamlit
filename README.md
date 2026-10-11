# 📦 Sistema de Gestão de Estoque

Aplicação desktop e web para gerenciamento e controle de estoque de materiais e equipamentos, construída com **Streamlit**, **Pandas** e **SQLite**.

---

## 🚀 Funcionalidades

- **Consultar Estoque:** Busca dinâmica por descrição ou localização, listagem completa com status e quantidades.
- **Cadastrar Novo Item:** Adição de novos materiais com categorização por estado (Novo, Usado, etc.) e localização física.
- **Entrada de Itens:** Adição rápida de saldo/quantidade para itens já existentes.
- **Saída de Itens (Baixa):** Registro de saída com validação contra saldos negativos.
- **Atualização / Edição:** Alteração detalhada de dados de itens cadastrados.
- **Gerenciamento / Exclusão:** Remoção segura de itens com confirmação operacional.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** (Interface gráfica interativa)
- **Pandas** (Tratamento e exibição de dados)
- **SQLite3** (Banco de dados relacional local embutido)
- **PyInstaller** (Compilação para executável `.exe`)

---

## 💻 Como Executar o Projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd NOME_DO_REPOSITORIO
```

### 2. Criar e ativar o ambiente virtual (Recomendado)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação
```bash
streamlit run app.py
```
ou pelo inicializador com abertura automática de navegador:
```bash
python run.py
```

---

## ⚙️ Compilação para Executável (.exe)

O projeto possui suporte à geração de executável standalone via PyInstaller:
```cmd
compilar.bat
```
O executável final será gerado dentro da pasta `dist/GestaoManutencao/`.
