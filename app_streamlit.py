# app_streamlit.py
import streamlit as st
import requests
from datetime import datetime

# Configuración de la API
API_URL = "http://localhost:8000" 

# Estilos CSS personalizados
st.markdown("""
<style>
.chat-bubble {
    padding: 1rem;
    border-radius: 1rem;
    margin: 0.5rem 0;
    max-width: 80%;
}
.user-bubble {
    background-color: #e3f2fd;
    margin-left: auto;
}
.assistant-bubble {
    background-color: #f5f5f5;
}
</style>
""", unsafe_allow_html=True)

def mostrar_historial():
    """Muestra el historial de conversación"""
    if 'historial' in st.session_state:
        for mensaje in st.session_state.historial:
            clase = "user-bubble" if mensaje['rol'] == 'usuario' else "assistant-bubble"
            st.markdown(f'<div class="chat-bubble {clase}">{mensaje["contenido"]}</div>', 
                    unsafe_allow_html=True)

def obtener_recomendacion(pregunta: str):
    """Obtiene recomendación de la API"""
    try:
        response = requests.post(
            f"{API_URL}/recomendacion",
            json={"consulta": pregunta}
        )
        
        if response.status_code == 200:
            return response.text
        return "❌ Error al obtener la recomendación"
    
    except requests.exceptions.RequestException:
        return "🔌 Error de conexión con el servidor"

def main():
    st.title("📲 KuHmar, asistente virtual")
    st.markdown("¡Hola! Soy tu experto en telefonía móvil. ¿En qué puedo ayudarte?")
    
    # Inicializar historial de chat
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    
    # Entrada de usuario
    with st.form("chat_form"):
        pregunta = st.text_input("Escribe tu pregunta:")
        enviado = st.form_submit_button("Enviar")
        
        if enviado and pregunta:
            # Añadir pregunta al historial
            st.session_state.historial.append({
                "rol": "usuario",
                "contenido": f"👤 Tú: {pregunta}",
                "timestamp": datetime.now().isoformat()
            })
            
            # Obtener respuesta de la API
            respuesta = obtener_recomendacion(pregunta)
            
            # Añadir respuesta al historial
            st.session_state.historial.append({
                "rol": "asistente",
                "contenido": f"🤖 KuHmar: {respuesta}",
                "timestamp": datetime.now().isoformat()
            })
    
    # Mostrar historial de chat
    mostrar_historial()

if __name__ == "__main__":
    main()