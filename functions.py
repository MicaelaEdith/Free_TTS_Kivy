from kivy.uix.popup import Popup
from kivy.uix.label import Label
from TTS.utils.manage import ModelManager
from TTS.api import TTS
from datetime import datetime
from kivy.uix.spinner import Spinner
from pydub import AudioSegment
from pydub.playback import play
from app_data import voice_models
import simpleaudio as sa
from csv_functions import *
import os
from model_downloader import download_models


class TTS_Kivy:
    def __init__(self):
        self.model_manager = ModelManager()
        self.models = self.model_manager.list_models()
        self.all_models= [['css10','tts_models/es/css10/vits'],['Mai','tts_models/es/mai/tacotron2-DDC'],['Female1','tts_models/multilingual/multi-dataset/your_tts'],['Female2','tts_models/multilingual/multi-dataset/your_tts'],['Male1','tts_models/multilingual/multi-dataset/your_tts'],['Male2','tts_models/multilingual/multi-dataset/your_tts']]
        self.es_models = [['css10','tts_models/es/css10/vits'],['Mai','tts_models/es/mai/tacotron2-DDC']]
        self.en_models = [['Female1','tts_models/multilingual/multi-dataset/your_tts'],['Female2','tts_models/multilingual/multi-dataset/your_tts'],['Male1','tts_models/multilingual/multi-dataset/your_tts'],['Male2','tts_models/multilingual/multi-dataset/your_tts']]
        self.filter = False
        self.filter_on = 'all'
        self.classify_and_list_models()

    def list(self):
        print(self.all_models)
        return self.all_models

    def filter(self, lan):
        result= []
        if lan == 'All' or lan == 'Todas':
            result = self.all_models
        elif lan == 'Es' or lan == 'Sp':
            result = self.es_models
        elif lan == 'En' or lan == 'In':
            result = self.en_models
           
        return result

    def execute_action(self, text_input, model):
        for i in self.all_models:
            if i[0] == model:
                model_ = i[1]

        models_ok = read_models()
        if model_ in models_ok:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            temp = "output_" + timestamp + ".wav"
            tts = TTS(model_name=model_)  
            tts.tts_to_file(text=text_input, file_path=temp)
        else:
            print('model missing')


    def audio_speaker(self, text_, model):
        if model == 'Female1' or model == 'Female2' or model == 'Male1' or model == 'Male2':
            self.model= 'your_tts'
        else:
            self.model = model

        models_ok = read_models()
        result = None
        for key, value in models_ok.items():
            if self.model in key:
                print(f"Modelo encontrado: {value}")
                result = value
            else:
                print('model key: ', key)
            
            
        if result != None:                                
            temp = "temp_audio.wav"
            for i in self.all_models:
                if i[0] == model:
                    model_ = i[1]

                    if model == 'css10' or model == 'Mai':
                        tts = TTS(model_name=model_)
                        tts.tts_to_file(text=text_, file_path=temp)
                    else:
                        tts = TTS('tts_models/multilingual/multi-dataset/your_tts')

                        if model == 'Female1':
                            speaker_ = 'female-en-5'
                        if model == 'Female2':
                            speaker_ = 'female-en-5\n'
                        if model == 'Male1':
                            speaker_ = 'male-en-2'
                        if model == 'Male2':
                            speaker_ = 'male-en-2\n'

                        tts.tts_to_file(text=text_, language='en', speaker=speaker_, file_path=temp)

            audio = AudioSegment.from_wav(temp)
            play_obj = sa.play_buffer(audio.raw_data, 
                                    num_channels=audio.channels,
                                    bytes_per_sample=audio.sample_width, 
                                    sample_rate=audio.frame_rate)
            play_obj.wait_done()
            os.remove(temp)

        else:
            print("Modelo no encontrado")
            buscar = input('buscar?')

            if buscar.lower() == 'si':
                for i in self.all_models:
                    if i[0] == model:
                        model_ = i[1]
                download_models()


    def classify_and_list_models(self):
        result= []
        for model in self.all_models:
            name = model[0]
            result.append(name)
        return result

    def update_model_spinner(self, spinner, lan):
        result= []
        if lan == 'All' or lan == 'Todas':
            for m in self.all_models:
                result.append(m[0])
        elif lan == 'Es' or lan == 'Sp':
            for m in self.es_models:
                result.append(m[0])
        elif lan == 'En' or lan == 'In':
            for m in self.en_models:
                result.append(m[0])
                
        return result

    def update_model_data(new_data):
        voice_models.clear()
        for model in new_data:
            voice_models[model['id']] = model['name']


#