import streamlit as st
from streamlit_carousel import carousel

st.title('Exposição das Fotos')
st.divider()



tab5, tab6, tab7, tab8 = st.tabs(["CINEAFRO", "Roda de conversa", "Oficina de Argila", 'Mural'])

with tab5:
    st.header('CINEAFRO')

    image_data = [
    {"img": "https://media.istockphoto.com/id/1457891405/pt/foto/four-fists-of-african-people-united-in-sky-photo-with-copy-space.jpg?s=1024x1024&w=is&k=20&c=CxxcZwvZQj9L7TDb-4D4gn9y8xNHKTpBxB8B5vW4NsI=", "title": "Imagem 1", "text": "Descrição da imagem 1"},
    {"img": "https://cdn.pixabay.com/photo/2016/12/13/06/16/hiv-1903373_1280.jpg", "title": "Imagem 2", "text": "Descrição da imagem 2"},
    {"img": "https://media.istockphoto.com/id/1294996137/pt/vetorial/black-history-month-banner.jpg?s=1024x1024&w=is&k=20&c=CIuRpMMc6JXurU89N1rRrkxN3AOyLmKtqaKRpQEz5-0=", "title": "Imagem 3", "text": "Descrição da imagem 3"},
    ]

    carousel(image_data)

    
with tab6:
    st.header('Roda de conversa')
    
with tab7:
    st.header('Oficina de Argila')
    

with tab8:
    st.header('Mural')
    

