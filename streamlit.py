import streamlit as st
from main import run_crew

avatar = "./assets/img/toad_avatar.png"
user = "./assets/img/yoshi.png"
toad = "https://static.wikia.nocookie.net/characterprofile/images/2/2d/Toad_Mario_Party_10.png/revision/latest?cb=20210904032011"

st.set_page_config(
    page_title="Toad - Guia de Viagens",
    page_icon=avatar
    )

st.markdown(
    f"""
    <div style="text-align: center;">
        <div style=" display: flex; justify-content: center; align-items: center; margin: 20px; gap: 20px;">
            <img src={toad} width="60">
        </div>
        <h5>Olá turista! Sou o Toad! Serei seu assistente em planejamento de viagens!</h5><br><br>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Como o Toad pode te ajudar hoje?"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"], avatar=avatar if message["role"] == "assistant" else user).write(message["content"])

if prompt := st.chat_input("Digite as informações da viagem aqui..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=user).write(prompt)

    with st.spinner('Toad está pensando...'):
        response = run_crew(prompt)
        
        response_text = str(response) if response else "Desculpe, houve um erro."
        
        st.session_state["messages"].append({"role": "assistant", "content": response_text})
    st.chat_message("assistant", avatar=avatar).write(response_text)