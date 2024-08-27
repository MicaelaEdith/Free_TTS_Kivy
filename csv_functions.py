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


