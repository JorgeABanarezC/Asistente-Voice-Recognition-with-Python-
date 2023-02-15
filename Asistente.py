
import os
import time

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech as tts

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

def main():
    # Configurar las credenciales de Google Cloud
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/credentials.json'

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

        # Reproducir la respuesta de voz
        os.system('aplay response.wav')

if __name__ == '__main__':
    main()
