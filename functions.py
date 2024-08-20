from kivy.uix.popup import Popup
from kivy.uix.label import Label
from TTS.utils.manage import ModelManager
from TTS.api import TTS
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
import io

class TTS_Kivy():
    def __init__(self):
        self.model_manager = ModelManager()
        self.models = self.model_manager.list_models()
        self.multilingual_models = []
        self.es_models = []
        self.en_models = []
        self.filter = False
        self.filter_on = 'all'


    def list(self):
        if not self.filter or self.filter_on == 'all':
            list_ = self.classify_and_list_models()
        if self.filter:
            if self.filter_on == 'en':
                list_ = self.en_models
            if self.filter_on == 'es':
                list_ = self.es_models
        return list_
        

    def filter(self, lan):
        self.lan = lan
        models_= [model for model in self.models if self.lan in model]
        return models_

    def execute_action(text_input, model):
        tts = TTS(model_name=model)
        text = text_input.text
        tts.tts_to_file(text=text, file_path="output"+str(datetime.now())+".wav")

        print(f'Action executed with text: {text}')


    def classify_and_list_models(self):

        for path in self.models:
            parts = path.split('/')

            if 'multilingual' in parts:
                index = parts.index('multilingual') + 2
                if index < len(parts):
                    model_name = parts[index].replace('_', ' ').capitalize()
                    self.multilingual_models.append(model_name)

            elif 'es' in parts:
                index = parts.index('es') + 1
                if index < len(parts):
                    model_name = parts[index].replace('_', ' ').capitalize()
                    self.es_models.append(model_name)

            elif 'en' in parts:
                index = parts.index('en') + 1
                if index < len(parts):
                    model_name = parts[index].replace('_', ' ').capitalize()
                    self.en_models.append(model_name)

        return list(self.multilingual_models+self.es_models+self.en_models)

    def audio_speaker(self, text):
        self.text = text
        tts = TTS(model_name=self.models[0])

        audio_data = tts.tts(text=self.text)

        audio_segment = AudioSegment(
            data=io.BytesIO(audio_data).getvalue(),
            sample_width=2,
            frame_rate=22050,
            channels=1
        )
        
        play(audio_segment)