from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
import os

client = genai.Client(api_key=os.getenv("api_key"))

def get_transcript(video_id):
    """
    Obtiene y concatena el transcript de un video de YouTube.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["es", "en"])
        return " ".join([entry["text"] for entry in transcript])  
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error obteniendo transcript: {str(e)}")

router = APIRouter(
    prefix='/link',
    tags=['link']
)

class ChatRequest(BaseModel):
    link: str

@router.post("/")
async def chat_bot(request: ChatRequest):
    try:  
        video_transcript = get_transcript(request.link)

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
si es la primer hora no pongas 00:minuto:segundo

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
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return {"response": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la generación de respuesta: {str(e)}")
