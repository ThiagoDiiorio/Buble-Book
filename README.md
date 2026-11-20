# Buble Book — versão para hospedagem

Projeto Flask com catálogo responsivo e páginas de leitura. Preparado para deploy no Render.

## Executar localmente

1. Instale Python 3.11 ou 3.12.
2. Crie um ambiente virtual, se desejar.
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie:

   ```bash
   python app.py
   ```

5. Abra `http://127.0.0.1:5000` no navegador.

## Publicar e obter um endereço fixo

1. Extraia o ZIP.
2. Crie um repositório no GitHub e envie os arquivos desta pasta, preservando a estrutura (`app.py`, `requirements.txt`, `templates/`, `static/`).
3. Crie uma conta no Render e escolha **New + → Web Service**.
4. Conecte o repositório GitHub da Buble Book.
5. Configure:
   - Runtime/Language: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance type: Free (para demonstração)
6. Clique em **Deploy Web Service**. Após o deploy, o Render mostrará o URL público. Esse URL será o endereço fixo da aplicação enquanto o serviço e o projeto existirem.

O serviço gratuito pode entrar em repouso depois de 15 minutos sem acesso e demorar cerca de um minuto para acordar, mas o URL não muda. Para funcionamento sempre ativo, será necessário um plano sem suspensão.

## EPUB

O livro comercial não foi incluído no pacote. O catálogo contém uma entrada de demonstração que abre a página de disponibilidade. Para ativar o leitor, coloque um EPUB autorizado em `static/books/diario-banana-20.epub` e publique a atualização. Arquivos dentro de `static/` são acessíveis publicamente: confirme que a autorização permite a distribuição online.

## Arquivos principais

- `app.py`: aplicação Flask e catálogo.
- `templates/index.html`: página inicial e pesquisa.
- `templates/reader.html`: página de leitura.
- `static/css/style.css`: visual responsivo.
- `static/books/`: pasta para EPUBs com permissão de publicação.
- `requirements.txt`: dependências Python.
- `render.yaml`: configuração opcional de deploy.
