import os
import pymysql
from fastapi import FastAPI, HTTPException, Query, requests
from pydantic import BaseModel
import uvicorn
import cohere
from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()
app = FastAPI()

# Modelo de datos para la solicitud
class ConsultaRequest(BaseModel):
    consulta: str

# Cargo variables de entorno desde un .env
load_dotenv()

# Configuro variables de entorno en el script
USERNAME = os.getenv("USERNAME_BD")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Endpoints
@app.get("/")
async def home():
    return {"message": "¡Bienvenido a KuHmar, tu asistente virtual de telefonía móvil!"}

@app.post("/recomendacion")
async def consulta(pregunta: ConsultaRequest):
    print('hola2')
    co = cohere.ClientV2(COHERE_API_KEY)
    response = co.chat(
    model="command-r-plus",
    messages=[{"role": "system", "content": "eres un experto en telefonía móvil de 2023 en adelante, da respuestas resumidas con la información esencial"},
            {"role": "user", "content": pregunta.consulta}
            ]
)
    
    recomendacion = response.message.content[0].text

    db = pymysql.connect(host = HOST,
                    user = USERNAME,
                    password = PASSWORD,
                    port = 3306,
                    cursorclass = pymysql.cursors.DictCursor
                    
)

    cursor = db.cursor()
    use_db = '''USE kuhmarapp_database'''
    cursor.execute(use_db)
    query = '''INSERT INTO consultas (consulta, respuesta)
    VALUES (%s, %s)'''
    cursor.execute(query, (pregunta.consulta, recomendacion))
    db.commit()
    cursor.close()
    db.close()
    return recomendacion

# Ejecutar la aplicación
uvicorn.run(app, host="0.0.0.0", port=8000)