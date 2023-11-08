import streamlit as st
import mysql.connector

def insert_user(nome, senha):
    conn = mysql.connector.connect(
        host='localhost',
        database='nome',
        user='root',
        password=''
    )

    cursor = conn.cursor()
    query = "INSERT INTO cadastro (nome, senha) VALUES (%s, %s)"
    cursor.execute(query, (nome, senha))
    conn.commit()

    cursor.close()
    conn.close()

# Configuração da página de cadastro

st.title("Página de Cadastro")

nome = st.text_input("Nome")
senha = st.text_input("Senha", type="password")

if st.button("Cadastrar"):
    insert_user(nome, senha)
    st.success("Cadastro realizado com sucesso!")
