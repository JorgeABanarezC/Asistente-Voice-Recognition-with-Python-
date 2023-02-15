# Asistente-Voice-Recognition-with-Python-

Explicacion del codigo y como realizarlo.

Instalar las bibliotecas necesarias:

Copy code
pip install google-cloud-speech google-cloud-texttospeech
Configurar las credenciales de Google Cloud Platform. Para hacer esto, debemos crear una cuenta de Google Cloud y obtener un archivo JSON de credenciales.

Crear un archivo Asistente.py e importar las bibliotecas necesarias:


import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech as tts

Definir una función para reconocer la voz del usuario:

def recognize_speech():
    client = speech.SpeechClient()

    # Configurar la entrada de audio
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='es-MX',
    )

    # Detectar el audio del micrófono
    mic = speech.MicrophoneStream(
        sample_rate_hertz=16000,
        chunk_size=1024,
    )

    with mic as source:
        audio = client.recognize(config=config, audio=source)
        return audio.results[0].alternatives[0].transcript
        
Definir una función para sintetizar una respuesta de voz:

def synthesize_speech(text):
    client = tts.TextToSpeechClient()

    # Configurar la síntesis de voz
    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code='es-MX',
        ssml_gender=tts.SsmlVoiceGender.FEMALE
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16
    )

    # Generar el audio
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Guardar el audio en un archivo
    with open('response.wav', 'wb') as out:
        out.write(response.audio_content)
        
Definir una función principal para controlar el asistente de voz:

def main():
    while True:
        # Escuchar la entrada de voz del usuario
        print('Escuchando...')
        text = recognize_speech()
        print('Usuario: ', text)

        # Procesar la entrada de voz
        if 'hola' in text:
            response_text = 'Hola, ¿en qué puedo ayudarte?'
        elif 'adiós' in text:
            response_text = 'Hasta luego!'
            synthesize_speech(response_text)
            break
        else:
            response_text = 'No entendí lo que dijiste.'

        # Sintetizar la respuesta de voz
        print('Asistente: ', response_text)
        synthesize_speech(response_text)
Ejecutar la función principal:
python
Copy code
if __name__ == '__main__':
    main()


Recuerda que debes tener creada una cuenta en Google Colud para poder utilizar esta biblioteca.
