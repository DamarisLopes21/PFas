import streamlit as st

# Leia o conteúdo do arquivo HTML
with open('resources/carrossel/carrossel.html', "r") as file:
    html_content = file.read()

with open('resources/carrossel/carrossel.css', "r") as file:
    css_content = file.read()

with open('resources/carrossel/carrossel.js', "r") as file:
    js_content = file.read()

# Exiba o conteúdo HTML no Streamlit
st.components.v1.html(
    html_content + f"<style>{css_content}</style><script>{js_content}</script>",
    scrolling=True,
    height=800
)
