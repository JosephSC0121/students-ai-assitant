from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import os

# Cargar claves de API desde variables de entorno
GOOGLE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Clave de API de Google Cloud
GENAI_API_KEY = os.getenv("GENAI_API_KEY")  # Clave de API para Gemini AI

# Inicializar cliente de Google Gemini
client = genai.Client(api_key=GENAI_API_KEY)

# Inicializar cliente de la API de YouTube
youtube = build("youtube", "v3", developerKey=GOOGLE_API_KEY)

def get_transcript(video_id):
    """
    Intenta obtener la transcripción del video de YouTube.
    Primero usa YouTubeTranscriptApi, si falla, usa la API oficial de YouTube.
    """
    try:
        # Intentar obtener los subtítulos con la API no oficial
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["es", "en"])
        return " ".join([entry["text"] for entry in transcript])

    except Exception as e:
        print(f"⚠️ Error con YouTubeTranscriptApi: {e}")
        print("🔄 Intentando con la API oficial de YouTube...")

        try:
            # Intentar obtener los subtítulos con la API oficial de YouTube
            response = youtube.captions().list(part="snippet", videoId=video_id).execute()
            captions = response.get("items", [])

            if not captions:
                raise Exception("No se encontraron subtítulos en la API oficial.")

            # Obtener el ID de los subtítulos en español o inglés
            caption_id = None
            for caption in captions:
                lang = caption["snippet"]["language"]
                if lang in ["es", "en"]:
                    caption_id = caption["id"]
                    break

            if not caption_id:
                raise Exception("No hay subtítulos disponibles en español o inglés.")

            # Descargar los subtítulos
            caption_response = youtube.captions().download(id=caption_id).execute()
            return caption_response.decode("utf-8")  # Convertir a texto

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error obteniendo transcript: {str(e)}")

# Configuración del router de FastAPI
router = APIRouter(
    prefix='/link',
    tags=['link']
)

class ChatRequest(BaseModel):
    link: str  # Se espera la URL completa del video

@router.post("/")
async def chat_bot(request: ChatRequest):
    try:
        # Extraer el ID del video de la URL
        video_id = request.link.split("v=")[-1].split("&")[0]

        # Obtener la transcripción
        video_transcript = get_transcript(video_id)

        # Construcción del prompt para Gemini AI
        prompt = f"""
Eres un asistente de IA especializado en analizar transcripciones de videos académicos.  
Tu tarea es extraer conceptos clave, identificar temas relevantes y proporcionar referencias confiables de libros, artículos de investigación y fuentes académicas.  
Es **MUY IMPORTANTE** que siempre mantengas el mismo formato estructurado en tu respuesta, ya que se mostrará en una aplicación frontend.

### **Estructura Esperada (Sigue siempre este formato):**

#### **Resumen de la Transcripción:**
Breve resumen del contenido de la transcripción en unas pocas frases.

#### **Conceptos Claves y Temas Relevantes:**
1. **Tema 1** (hora:minuto:segundo en el que se habla del tema): Explicación.
2. **Tema 2** (hora:minuto:segundo en el que se habla del tema): Explicación.
3. **Tema 3** (hora:minuto:segundo en el que se habla del tema): Explicación.
Si es la primera hora, no pongas 00:minuto:segundo.

#### **Referencias y Fuentes de Apoyo:**
1. **Categoría de Referencia (ejemplo: 'Formación e Historia')**:
   - **Autor, Año**. *Título*. Editorial.
   - **Autor, Año**. *Título*. Editorial.

2. **Categoría de Referencia (ejemplo: 'Análisis Literario')**:
   - **Autor, Año**. *Título*. Editorial.

#### **Citas Formateadas (Estilo APA):**
- **Autor, Año**. *Título*. Editorial.
- **Autor, Año**. *Título*. Editorial.

### **Reglas:**
1. **Siempre proporciona al menos 5 referencias** de libros académicos o artículos de investigación.
2. **Sigue el formato de citación APA** en la última sección.
3. **NO generes fuentes ficticias**—solo libros y artículos reales.
4. **Asegúrate de que la salida sea siempre consistente en su estructura**.

---
Ahora, analiza la siguiente transcripción y genera la respuesta estructurada:
---
{video_transcript}
"""

        # Llamar a Gemini AI
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la generación de respuesta: {str(e)}")
