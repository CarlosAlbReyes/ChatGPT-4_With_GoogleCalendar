from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import requests

SCOPES = ['https://www.googleapis.com/auth/calendar']
JSON_FILE = 'credentials.json' # Ruta al archivo JSON de credenciales
CHATGPT_API_KEY = 'sk-proj-UZCxZMfEJP5RkXuABqpeT3BlbkFJ5NCJFjkBvdTEOfQrVzXf' # Tu clave API de ChatGPT

def authenticate_google_calendar():
    credentials = service_account.Credentials.from_service_account_file(JSON_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    return service

def generate_events(user_input):
    # Usa ChatGPT para procesar la entrada del usuario y generar un resumen del evento
    chatgpt_response = requests.post(
        'https://api.openai.com/v1/engines/davinci/completions',
        headers={'Authorization': f'Bearer {CHATGPT_API_KEY}'},
        json={'prompt': user_input, 'temperature': 0.7, 'max_tokens': 100})
    event_summary = chatgpt_response.json()['choices'][0]['text']

    # Extrae información relevante del resumen del evento
    event_details = parse_event_details(event_summary)

    # Crea un objeto de evento de Google Calendar
    event = {
        'summary': event_summary,
        'location': event_details['location'],
        'start': {
            'dateTime': event_details['start_time'],
            'timeZone': event_details['timezone']
        },
        'end': {
            'dateTime': event_details['end_time'],
            'timeZone': event_details['timezone']
        }
    }

    return event

def create_event(service, event):
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Evento creado: {event["summary"]}')
    
    def main():
        service = authenticate_google_calendar()

    while True:
        user_input = input('Ingrese una descripción de evento o escriba "salir" para finalizar: ')

        if user_input.lower() == 'salir':
            break

        event = generate_events(user_input)
        create_event(service, event)

if __name__ == '__main__':
    main()


