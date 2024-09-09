from TTS.utils.manage import ModelManager
from csv_functions import write_model, read_models
from TTS.api import TTS

models_to_download = [
    "tts_models/es/css10/vits",
    "tts_models/multilingual/multi-dataset/your_tts",
    "tts_models/es/mai/tacotron2-DDC"]

def download_models():
    model_manager = ModelManager()
    models_ok = read_models()         

    for model_name in models_to_download:
        print(f"Descargando el modelo {model_name}...")
        model_path, config_path, model_item = model_manager.download_model(model_name)
        print(f"Modelo {model_name} descargado en: {model_path}")
        write_model(model_name, model_path)


def download_one_model(model):
    model__ = 'tts_models/es/mai/tacotron2-DDC'
    model_manager = ModelManager()
    print('paso')
    model_path, config_path, model_item = model_manager.download_model(model__)
    write_model(model, model_path)


download_one_model('m')