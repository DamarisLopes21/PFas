import streamlit as st
from streamlit_carousel import carousel
import spacy

nlp = spacy.load('pt_core_news_sm')

def verifica_comentario(comentario):
    palavras_ofensivas = set()

    with open('PFas/resources/palavroes.txt', 'r', encoding='UTF-8') as arquivo:
        for linha in arquivo:
            palavras_ofensivas.add(linha.strip().lower())

    comentario = remove_numeros_como_letras(comentario)
    doc = nlp(comentario)

    tokens = [token.text.strip().lower() for token in doc]
    lemas = [token.lemma_.strip().lower() for token in doc]
    
    for palavra in palavras_ofensivas:
        if palavra in tokens or palavra in comentario or palavra in lemas:
            return False
    return True

def remove_numeros_como_letras(texto):

    mapeamento = {
        '0': 'o',
        '1': 'i',
        '!': 'i',
        '3': 'e',
        '4': 'a',
        '5': 's',
        '7': 't',
    }

    for numero, letra in mapeamento.items():
        texto = texto.replace(numero, letra)

    return texto

# Dados de exemplo para o catálogo de filmes
catalogo_filmes = [
    {
        "img": "https://media.istockphoto.com/id/1457891405/pt/foto/four-fists-of-african-people-united-in-sky-photo-with-copy-space.jpg?s=1024x1024&w=is&k=20&c=CxxcZwvZQj9L7TDb-4D4gn9y8xNHKTpBxB8B5vW4NsI=", 
        "title": "Imagem 1",
        "text": "Descrição da img 1"
    },
    {
        "img": "https://cdn.pixabay.com/photo/2016/12/13/06/16/hiv-1903373_1280.jpg",
        "title": "Imagem 2",
        "text": "Descrição da img 2"
    },
    {
        "img": "https://media.istockphoto.com/id/1294996137/pt/vetorial/black-history-month-banner.jpg?s=1024x1024&w=is&k=20&c=CIuRpMMc6JXurU89N1rRrkxN3AOyLmKtqaKRpQEz5-0=", 
        "title": "Imagem 3",
        "text": "Descrição da img 3"
    }
]

# Página principal
st.title("Catálogo de Filmes")

# Loop através dos filmes no catálogo
for filme in catalogo_filmes:
    st.header(filme["title"])
    st.image(filme["img"], use_column_width=True, caption=filme["text"])
    
    # Seção de comentários
    st.subheader("Comentários")
    comentario = st.text_area(f'Deixe seu comentário para {filme["title"]}:')
    if st.button('Enviar comentário para o filme ' + filme["title"] ):
        if verifica_comentario(comentario):
            st.write(f'Comentário para {filme["title"]}: {comentario}')
        else:
            st.error('Comentário contém linguagem ofensiva. Por favor, revise.')

    # Quebra de seção entre os filmes
    st.markdown("---")

# Exibir o carrossel de imagens no final da página
carousel(catalogo_filmes)