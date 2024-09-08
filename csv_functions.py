import csv
import os

config_csv = 'config.csv'
models_csv = 'models.csv'

def check_and_create_config_csv():
    if not os.path.exists(config_csv):
        with open(config_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['theme', 'language', 'init']) 
            writer.writerow(['False', 'en', 'False'])      

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
    models = {}
    with open(models_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            models[row['model_path']] = row['model_name']
    return models

def write_model(model_name, model_path):
    check_and_create_models_csv()
    with open(models_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([model_name, model_path])

def is_model_downloaded(model_path):
    models = read_models()
    return model_path in models
