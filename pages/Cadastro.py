import streamlit as st
import mysql.connector
import bcrypt

def insert_user(name, password):
    # Gera um salt aleatório
    salt = bcrypt.gensalt()
    
    # Gera o hash da senha utilizando o salt
    hashed_senha = bcrypt.hashpw(password.encode('utf-8'), salt)

    conn = mysql.connector.connect(
        host='localhost',
        database='site_consciencia_negra',
        user='root',
        password='root'
    )

    cursor = conn.cursor()
    query = "INSERT INTO users (name, password, salt) VALUES (%s, %s)"
    cursor.execute(query, (name, hashed_senha))
    
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
