import speech_recognition as sr
import playsound
from gtts import gTTS
import random
import webbrowser
import pyttsx3
import os


class Virtual_assistance():
    def __init__(self, assist_name, person_name):
        self.person_name = person_name
        self.assist_name = assist_name

        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.voice_data = ''

    def engine_speak(self, text):
        text = str(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def record_audio(self, ask=''):
        with sr.Microphone() as source:
            if ask:
                print('Ouvindo...')
                self.engine_speak(ask)

            audio = self.r.listen(source, 10, 5)
            print('Procurando dados...')

            try:
                self.voice_data = self.r.recognize_google(
                    audio, language='pt-BR')
            except sr.UnknownValueError:
                self.engine_speak(
                    f'Desculpe, {self.person_name} eu não consegui entender')
            except sr.RequestError:
                self.engine_speak(
                    f'Desculpe, {self.person_name} eu não consegui conectar')

            print('>>', self.voice_data.lower())
            self.voice_data = self.voice_data.lower()

            return self.voice_data.lower()

    def engine_speak(self, audio_string):
        audio_string = str(audio_string)
        tts = gTTS(text=audio_string, lang='pt-BR')
        r = random.randint(1, 20000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(self.assist_name+':'+audio_string)
        os.remove(audio_file)

    def there_exist(self, terms):
        for term in terms:
            if term in self.voice_data:
                return True

    def respond(self, voice_data):
        if self.there_exist(['hi', 'hello', 'hey', 'oi', 'olá']):
            greetings = [f'Olá {self.person_name} o que faremos hoje? ',
                         f'Oi {self.person_name}, como posso ajudar?'
                         f'{self.person_name} do que você precisa?']
            greet = greetings[random.randint(0, len(greetings)-1)]
            self.engine_speak(greet)

        # Pesquisa no Google
        if self.there_exist(['procure por']) and 'youtube' not in voice_data:
            search_term = voice_data.split('for')[-1]
            url = 'https://www.google.com/search?q=' + search_term
            webbrowser.get().open(url)
            self.engine_speak(
                'aqui está o que eu encontrei sobre' + search_term + 'no google')
            return

        # Pesquisa no youtube
        if self.there_exist(['procure no youtube por']):
            search_term = voice_data.split('for')[-1]
            url = 'https://www.youtube.com/results?search_query=' + search_term
            webbrowser.get().open(url)
            self.engine_speak(
                'aqui está o que eu encontrei sobre' + search_term + 'no google')
            return


assistente = Virtual_assistance('assistente', 'Pedro')
while True:
    voice_data = assistente.record_audio()
    assistente.respond(voice_data)
    if assistente.there_exist(['encerrar', 'acabou', 'desligar', 'fim']):
        assistente.engine_speak('Tenha um bom dia')
        break
