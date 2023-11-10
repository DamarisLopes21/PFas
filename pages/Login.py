import streamlit as st
import mysql.connector
import bcrypt

def login(name, password):
    conn = mysql.connector.connect(
        host='localhost',
        database='site_consciencia_negra',
        user='root',
        password='root'
    )

    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = %s"
    cursor.execute(query, (name,))
    
    user = cursor.fetchone()
        
    cursor.close()
    conn.close()
    
    if user:
        stored_hashed_password = user[2]  # Índice correspondente à coluna 'password' na tabela
        
        # Verifica se as senhas coincidem
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
        
    return False

# Configuração da página de login
st.title("Página de Login")

name = st.text_input("name")
password = st.text_input("password", type="password")

if st.button("Login"):
    if login(name, password):
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha inválidos.")