import csv
import os

config_csv = 'config.csv'
models_csv = 'cloned_models.csv'

def check_and_create_config_csv():
    if not os.path.exists(config_csv):
        with open(config_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['theme', 'language']) 
            writer.writerow(['False', 'en'])      

def read_config():
    check_and_create_config_csv()
    with open(config_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            return row['theme'], row['language']
        
    return None, None


def write_config(color, language):
    check_and_create_config_csv()
    with open(config_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['theme', 'language'])
        writer.writerow([color, language])      

def check_and_create_models_csv():
    if not os.path.exists(models_csv):
        with open(models_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['model_name', 'model_path'])

def read_models():
    check_and_create_models_csv()
    models = []
    with open(models_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            models.append({'model_name': row['model_name'], 'model_path': row['model_path']})
    return models

def write_model(model_name, model_path):
    check_and_create_models_csv()
    with open(models_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([model_name, model_path])

# Ejemplo de uso
if __name__ == '__main__':
    # Guardar configuración
    write_config('#ffffff', 'en')

    # Leer configuración
    color, language = read_config()
    print(f"Color: {color}, Language: {language}")

    # Guardar modelos clonados
    write_model('VoiceClone1', '/path/to/model1')
    write_model('VoiceClone2', '/path/to/model2')

    # Leer modelos clonados
    models = read_models()
    for model in models:
        print(f"Model Name: {model['model_name']}, Model Path: {model['model_path']}")

