import requests
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Recuerda reemplazar con tu clave API de OpenAI
openai_api_key = "sk-proj-UZCxZMfEJP5RkXuABqpeT3BlbkFJ5NCJFjkBvdTEOfQrVzXf"

# Crea una instancia de la API de ChatGPT4
chatgpt = OpenAIApi(openai_api_key)

# Recuerda reemplazar con la ruta de tu archivo JSON de credenciales
credentials_file_path = "credentials.json"

# Crea una instancia del servicio Google Calendar
credentials = Credentials.from_service_account_file(credentials_file_path, scopes=["https://www.googleapis.com/auth/calendar"])
calendar_service = build('calendar', 'v3', credentials=credentials)

def process_user_request(user_request):
    # Envía la solicitud del usuario a ChatGPT4 para obtener una respuesta
    chatgpt_response = chatgpt.complete(user_request)["choices"][0]["text"]

    # Procesa la respuesta de ChatGPT4 para extraer información relevante (doctor, fecha, hora, motivo)
    # Utiliza técnicas de procesamiento del lenguaje natural (NLP) para extraer esta información
    # Ejemplo de código para extraer la fecha y hora:
    date_time_regex = r"(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2})"
    match = "re.search"(date_time_regex, chatgpt_response)
    if match:
        appointment_date = match.group(1) + "-" + match.group(2) + "-" + match.group(3)
        appointment_time = match.group(4) + ":" + match.group(5)
    else:
        appointment_date = None
        appointment_time = None

    # Construye un diccionario con la información extraída
    appointment_info = {
        "doctor": "DR. WHITE",  # Ejemplo de cómo extraer el doctor
        "date": appointment_date,
        "time": appointment_time,
        "reason": chatgpt_response  # Motivo de la cita (toda la respuesta de ChatGPT4)
    }

    return appointment_info

def create_calendar_event(appointment_info):
    # Construye el evento de Google Calendar
    event = {
        'summary': f"Cita con {appointment_info['doctor']}",
        'location': 'Clínica Ejemplo',  # Ejemplo de ubicación
        'description': appointment_info['reason'],
        'start': {
            'dateTime': f"{appointment_info['date']}T{appointment_info['time']}:00-05:00",  # Zona horaria -5
            'timeZone': 'America/New_York'  # Zona horaria -5
        },
        'end': {
            'dateTime': f"{appointment_info['date']}T{appointment_info['time']+30}:00-05:00",  # Cita de 30 minutos
            'timeZone': 'America/New_York'  # Zona horaria -5
        }
    }

    # Crea el evento en el calendario
    calendar_service.events().insert(calendarId='primary', body=event).execute()


while True:
    # Solicita la solicitud del usuario
    user_request = input("Ingrese su solicitud de cita (por ejemplo, 'Quiero agendar una cita con el Dr. White el 2024-04-20 a las 10:00 para un chequeo'): ")

    # Procesa la solicitud del usuario
    appointment_info = process_user_request(user_request)

    # Si se extrajo información válida, crea la cita en Google Calendar
    if appointment_info["date"] and appointment_info["time"]:
        create_calendar_event