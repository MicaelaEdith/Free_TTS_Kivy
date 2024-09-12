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
from platformdirs import user_documents_dir


class TTS_Kivy:
    def __init__(self):
        self.model_manager = ModelManager()
        self.models = self.model_manager.list_models()
        self.all_models= [['css10','tts_models/es/css10/vits'],['mai','tts_models/es/mai/tacotron2-DDC'],['Female1','tts_models/multilingual/multi-dataset/your_tts'],['Female2','tts_models/multilingual/multi-dataset/your_tts'],['Male1','tts_models/multilingual/multi-dataset/your_tts'],['Male2','tts_models/multilingual/multi-dataset/your_tts']]
        self.es_models = [['css10','tts_models/es/css10/vits'],['mai','tts_models/es/mai/tacotron2-DDC']]
        self.en_models = [['Female1','tts_models/multilingual/multi-dataset/your_tts'],['Female2','tts_models/multilingual/multi-dataset/your_tts'],['Male1','tts_models/multilingual/multi-dataset/your_tts'],['Male2','tts_models/multilingual/multi-dataset/your_tts']]
        self.filter = False
        self.filter_on = 'all'
        self.classify_and_list_models()
        self.file_path = ''

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

        dir_documents = user_documents_dir()  
        free_tts_folder = os.path.join(dir_documents, "free_tts")

        if not os.path.exists(free_tts_folder):
            os.makedirs(free_tts_folder)

        self.file_path= free_tts_folder

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        temp = os.path.join(free_tts_folder, f"output_{timestamp}.wav")

        if model in ['Female1', 'Female2', 'Male1', 'Male2']:
            self.model = 'your_tts'
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

        if result is not None:
            for i in self.all_models:
                if i[0] == model:
                    model_ = i[1]

                    if model in ['css10', 'mai']:
                        tts = TTS(model_name=model_)
                        tts.tts_to_file(text=text_input, file_path=temp)
                    else:
                        tts = TTS('tts_models/multilingual/multi-dataset/your_tts')

                        speaker_map = {
                            'Female1': 'female-en-5',
                            'Female2': 'female-en-5\n',
                            'Male1': 'male-en-2',
                            'Male2': 'male-en-2\n'
                        }
                        speaker_ = speaker_map.get(model, '')
                        tts.tts_to_file(text=text_input, language='en', speaker=speaker_, file_path=temp)
            
            return True
            
            
        

    def audio_speaker(self, text_, model):
        if model in ['Female1', 'Female2', 'Male1', 'Male2']:
            self.model = 'your_tts'
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

        if result is not None:     
            try:
                temp = "temp_audio.wav"
                for i in self.all_models:
                    if i[0] == model:
                        model_ = i[1]

                        if model in ['css10', 'mai']:
                            tts = TTS(model_name=model_)
                            tts.tts_to_file(text=text_, file_path=temp)
                        else:
                            tts = TTS('tts_models/multilingual/multi-dataset/your_tts')

                            speaker_map = {
                                'Female1': 'female-en-5',
                                'Female2': 'female-en-5\n',
                                'Male1': 'male-en-2',
                                'Male2': 'male-en-2\n'
                            }
                            speaker_ = speaker_map.get(model, '')
                            tts.tts_to_file(text=text_, language='en', speaker=speaker_, file_path=temp)

                audio = AudioSegment.from_wav(temp)
                play_obj = sa.play_buffer(audio.raw_data, 
                                        num_channels=audio.channels,
                                        bytes_per_sample=audio.sample_width, 
                                        sample_rate=audio.frame_rate)
                play_obj.wait_done()
                os.remove(temp)
                return True

            except:
                return False                         
           

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