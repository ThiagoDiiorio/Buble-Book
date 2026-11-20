from flask import Flask, render_template, request, abort, url_for
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
BOOKS_DIR = BASE_DIR / "static" / "books"

# Os seis primeiros livros são exemplos fictícios para o protótipo.
# O EPUB comercial não acompanha este pacote. Para publicá-lo, coloque
# um arquivo autorizado em static/books/diario-banana-20.epub.
LIVROS = [
    {
        "slug": "jardim-estrelas",
        "titulo": "O Jardim das Pequenas Estrelas",
        "autor": "Lia Monteiro",
        "genero": "Fantasia",
        "simbolo": "✦",
        "capa": "rosa",
        "descricao": "Uma história delicada sobre sonhos, amizade e descobertas.",
        "texto": [
            "Na pequena cidade de Aurora, existia um jardim que só aparecia quando o céu ficava completamente escuro. Diziam que cada flor guardava um sonho esquecido por alguém.",
            "Clara encontrou aquele lugar numa noite de primavera. Entre folhas brilhantes e pétalas que pareciam pequenas estrelas, percebeu que algumas aventuras começam quando temos coragem de fazer uma pergunta.",
            "Naquela noite, Clara decidiu voltar ao jardim. Não sabia o que encontraria, mas descobriu que a curiosidade pode ser a primeira página de uma grande história."
        ],
    },
    {
        "slug": "cartas-lua",
        "titulo": "Cartas para a Lua",
        "autor": "Marina Alves",
        "genero": "Romance",
        "simbolo": "☾",
        "capa": "lilas",
        "descricao": "Uma narrativa sobre sentimentos, encontros e novos começos.",
        "texto": [
            "Todas as noites, Sofia escrevia uma carta para a lua. Não esperava resposta. Era apenas seu jeito de organizar os pensamentos antes de dormir.",
            "Numa terça-feira chuvosa, ela conheceu alguém que também gostava de escrever. A conversa começou por causa de um livro esquecido no banco de uma praça.",
            "A partir daquele dia, as cartas ficaram diferentes. Sofia continuou olhando para a lua, mas começou também a prestar atenção nas pessoas ao seu redor."
        ],
    },
    {
        "slug": "cidade-segredos",
        "titulo": "A Cidade dos Segredos",
        "autor": "Caio Nunes",
        "genero": "Mistério",
        "simbolo": "⌕",
        "capa": "azul",
        "descricao": "Uma rua silenciosa, uma chave antiga e um mistério.",
        "texto": [
            "A rua das Acácias tinha vinte e três casas e apenas uma janela que permanecia iluminada depois da meia-noite.",
            "Quando Miguel encontrou uma chave de cobre perto do portão da biblioteca, percebeu que havia algo estranho naquele bairro. O objeto trazia uma pequena inscrição quase apagada.",
            "Ele abriu seu caderno, anotou as primeiras pistas e decidiu começar pelo lugar onde todos diziam não haver nada interessante: a velha estação."
        ],
    },
    {
        "slug": "clube-coisas-perdidas",
        "titulo": "O Clube das Coisas Perdidas",
        "autor": "Nina Duarte",
        "genero": "Aventura",
        "simbolo": "☁",
        "capa": "menta",
        "descricao": "Quatro amigos descobrem que objetos esquecidos guardam histórias.",
        "texto": [
            "O clube funcionava no quartinho dos fundos de uma papelaria. Sua regra principal era simples: nenhum objeto encontrado poderia ser considerado sem importância.",
            "Uma luva sem par, um botão dourado e uma fotografia antiga foram as primeiras pistas da semana. Cada descoberta levava os amigos a um canto diferente do bairro.",
            "Eles logo perceberam que encontrar o dono de alguma coisa era só parte da aventura. A outra parte era descobrir a história que aquele objeto tinha para contar."
        ],
    },
    {
        "slug": "pequenas-coisas",
        "titulo": "Pequenas Coisas, Grandes Mundos",
        "autor": "Clara Reis",
        "genero": "Poesia",
        "simbolo": "❀",
        "capa": "amarelo",
        "descricao": "Pequenos textos sobre a natureza e os momentos cotidianos.",
        "texto": [
            "A manhã chegou devagar, vestindo as folhas com gotas de luz. No quintal, o vento ensaiava uma canção que ninguém precisava entender para gostar de ouvir.",
            "Há mundos inteiros escondidos nas coisas pequenas: uma semente, uma conversa, o cheiro da chuva chegando antes da primeira gota.",
            "Talvez viver também seja isso: prestar atenção, guardar alguns instantes com carinho e permitir que os dias comuns tenham sua própria beleza."
        ],
    },
    {
        "slug": "cafe-paginas",
        "titulo": "O Café das Páginas",
        "autor": "Tomás Vidal",
        "genero": "Contos",
        "simbolo": "☕",
        "capa": "pessego",
        "descricao": "Histórias acolhedoras que se encontram em uma pequena livraria.",
        "texto": [
            "A livraria abria às oito, mas o aroma do café já escapava pela porta antes mesmo de o primeiro cliente chegar.",
            "Dona Elisa acreditava que toda pessoa entrava ali procurando alguma coisa. Às vezes era um livro específico; em outras, era apenas um lugar tranquilo para respirar.",
            "Naquela manhã, seis desconhecidos escolheram mesas diferentes. Nenhum deles imaginava que, antes do fim do dia, suas histórias acabariam se cruzando."
        ],
    },
    {
        "slug": "diario-banana-20",
        "titulo": "Diário de um Banana 20: Festa Insana",
        "autor": "Jeff Kinney",
        "genero": "Humor",
        "simbolo": "☻",
        "capa": "azul",
        "descricao": "Título incluído no catálogo do protótipo. A leitura integrada requer que o arquivo autorizado seja incluído no projeto.",
        "epub": "books/diario-banana-20.epub",
        "texto": [],
    },
]

@app.get("/")
def inicio():
    busca = request.args.get("q", "").strip()
    categoria = request.args.get("categoria", "Todas").strip()
    categorias = ["Todas"] + sorted({livro["genero"] for livro in LIVROS})
    if categoria not in categorias:
        categoria = "Todas"

    consulta = busca.casefold()
    resultados = []
    for livro in LIVROS:
        alvo = f"{livro['titulo']} {livro['autor']} {livro['genero']}".casefold()
        if consulta in alvo and (categoria == "Todas" or livro["genero"] == categoria):
            resultados.append(livro)

    return render_template(
        "index.html",
        livros=resultados,
        categorias=categorias,
        busca=busca,
        categoria=categoria,
    )

@app.get("/livro/<slug>")
def ler_livro(slug):
    livro = next((item for item in LIVROS if item["slug"] == slug), None)
    if livro is None:
        abort(404)

    if livro.get("epub"):
        epub_path = BASE_DIR / "static" / livro["epub"]
        epub_disponivel = epub_path.is_file()
        return render_template(
            "reader.html",
            livro=livro,
            epub_disponivel=epub_disponivel,
            epub_url=url_for("static", filename=livro["epub"]) if epub_disponivel else None,
        )

    return render_template("reader.html", livro=livro, epub_disponivel=False, epub_url=None)

@app.get("/health")
def health():
    return {"status": "ok", "app": "Buble Book"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
