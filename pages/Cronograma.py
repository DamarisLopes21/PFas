import streamlit as st

st.title('Cronograma')

eventos = {
    "2023-11-10": ["Evento 1", "Evento 2"],
    "2023-11-15": ["Evento 3"],
    "2023-11-20": ["Evento 4", "Evento 5"],
}

st.title("Calendário de Eventos")

# Selecione a data a partir de um seletor
data_selecionada = st.date_input("Selecione uma data")

# Verifique se há eventos para a data selecionada
if data_selecionada in eventos:
    st.write(f"Eventos em {data_selecionada}:")
    for evento in eventos[data_selecionada]:
        st.write(evento)
else:
    st.write("Nenhum evento programado para esta data.")