# LinkedIn Connection Automation

Este projeto automatiza o processo de conexão com perfis do LinkedIn a partir de uma planilha do Excel usando o Selenium. A planilha contém links de perfis do LinkedIn e o script verifica se o perfil já foi adicionado, tenta se conectar com ele e atualiza o status na planilha.

## Funcionalidades

- **Automação de Conexão no LinkedIn**: Faz login no LinkedIn e tenta enviar solicitações de conexão para os perfis listados em uma planilha.
- **Verificação de Status**: A coluna `HasAdd` é usada para verificar e registrar se o convite foi enviado com sucesso (`"X"`).
- **Limite de Convites**: O script permite enviar até um número predefinido de convites (atualmente limitado a 8).
- **Atualização de Planilha**: O status de cada conexão é salvo de volta na planilha `Networking Escola da Nuvem.xlsx`.

## Pré-requisitos

- **Python 3.x**
- **Google Chrome** instalado.
- Bibliotecas Python:
  - `selenium`
  - `pandas`
  - `python-dotenv`
  - `openpyxl`
  - `xlsxwriter`

## Instalação

1. **Clone o repositório**:

  ```bash
  git clone git@github.com:xLucasSA/linkedin-network.git
  cd linkedin-network
  ```

2. **Crie um ambiente virtual:**

  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  venv\Scripts\activate     # Windows
  ```

3. **Instale as dependências:**
  ```bash
  pip install -r requirements.txt
  ```

4. **Crie um arquivo .env no diretório raiz do projeto com as credenciais do LinkedIn conforme example.env:**
  ```bash
  LINKEDIN_LOGIN=seu_email_no_linkedin
  LINKEDIN_PASSWORD=sua_senha_no_linkedin
  ```

## Como Usar

1. **Prepare a Planilha**:
   - Coloque sua planilha Excel chamada `Networking Escola da Nuvem.xlsx` no diretório raiz do projeto.
   - A planilha deve conter uma coluna chamada `Linkedin` com os URLs dos perfis e uma coluna opcional `HasAdd` que será preenchida pelo script.

2. **Execute o Script**:
   
   Para rodar o script, basta executar o seguinte comando:

   ```bash
   python main.py
   ```

   O script irá:
   - Fazer login no LinkedIn.
   - Iterar sobre os perfis da planilha.
   - Tentar se conectar com cada perfil que ainda não tenha o status "X" na coluna HasAdd.
   - Atualizar o status na planilha.

3. **Limite de Convites:**

    Por padrão, o script enviará no máximo 8 convites por execução. Você pode alterar o valor da variável limit no código, se desejar.

4. **Rodar em Segundo Plano:**
    Por padrão, o script exibirá a tela do navegador. Se quiser rodar em segundo plano, basta alterar o parametro hiden para `True`

## Estrutura do Projeto

  ```bash
  .
  ├── .env                    # Arquivo contendo suas credenciais do LinkedIn (não deve ser compartilhado)
  ├── Networking Escola da Nuvem.xlsx   # Planilha Excel com os perfis do LinkedIn
  ├── main.py                 # Script principal de automação
  ├── requirements.txt        # Lista de dependências do projeto
  └── README.md               # Este arquivo
  ```

## Notas Importantes
 - Uso de Contas LinkedIn: O LinkedIn tem políticas rigorosas contra automação. Use este script com moderação para evitar o bloqueio de sua conta.
 - Atraso Aleatório: O script adiciona um atraso aleatório nas interações para simular comportamentos humanos e reduzir o risco de detecção pelo LinkedIn.
 - Atualização da Planilha: Ao final do processo, a planilha Networking Escola da Nuvem.xlsx será atualizada com o status das conexões. Se um convite foi enviado com sucesso, a célula correspondente na coluna HasAdd será marcada com "X".