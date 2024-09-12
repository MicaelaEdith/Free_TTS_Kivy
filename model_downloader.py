from TTS.utils.manage import ModelManager
from csv_functions import write_model, read_models, is_model_downloaded
from TTS.api import TTS

models_to_download = [
    "tts_models/es/css10/vits",
    "tts_models/multilingual/multi-dataset/your_tts",
    "tts_models/es/mai/tacotron2-DDC"]

models_your_tts = ['Female1', 'Female2', 'Male1', 'Male2']

def download_models():
    model_manager = ModelManager()
    models_in_csv = read_models()

    for model_name in models_to_download:
        if not is_model_downloaded(model_name):
            print(f"Descargando el modelo {model_name}...")
            model_path, config_path, model_item = model_manager.download_model(model_name)
            print(f"Modelo {model_name} descargado en: {model_path}")
            write_model(model_name, model_path)
        else:
            print(f"El modelo {model_name} ya está descargado.")

def download_one_model(model):
    model_ = model
    model_manager = ModelManager()
    
    if model in models_your_tts:
        model_ = "tts_models/multilingual/multi-dataset/your_tts"

    print('model_ : ',model_)

    for model_name in models_to_download:
        if model_ in model_name and not is_model_downloaded(model_name):
            model_path, config_path, model_item = model_manager.download_model(model_name)
            print(f"Modelo {model_name} descargado en: {model_path}")
            write_model(model_name, model_path)
            return True