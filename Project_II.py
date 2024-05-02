import datetime
from googleapiclient.discovery import build
from chatgpt import ChatGPT

# Credenciales de Google Calendar
credentials, _ = 'GoogleAuth'().load_from_storage_file('credentials.json')
calendar = build('calendar', 'v3', credentials=credentials)

# Instancia de ChatGPT
chatgpt = ChatGPT(token="sk-proj-UZCxZMfEJP5RkXuABqpeT3BlbkFJ5NCJFjkBvdTEOfQrVzXf")  # Reemplaza con tu clave API

# Función para agendar cita
def agendar_cita(fecha_hora, descripcion):
    # Convertir fecha y hora a formato ISO
    fecha_hora_iso = datetime.datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M').isoformat()

    # Generar resumen de la cita con ChatGPT
    resumen_cita = chatgpt.generate_text(
        prompt=f"Generar resumen de cita para {fecha_hora} con descripción {descripcion}"
    )

    # Crear evento en Google Calendar
    event = {
        'summary': resumen_cita,
        'start': {
            'dateTime': fecha_hora_iso,
            'timeZone': 'America/Santo_Domingo'  # Ajusta la zona horaria según tu ubicación
        },
        'end': {
            'dateTime': fecha_hora_iso,
            'timeZone': 'America/Santo_Domingo'  # Ajusta la zona horaria según tu ubicación
        }
    }

    calendar.events().insert(calendarId='primary', body=event).execute()

# Ejemplo de uso
fecha_hora = "2024-05-04 16:00"
descripcion = "Reunión de equipo"

agendar_cita(fecha_hora, descripcion)
