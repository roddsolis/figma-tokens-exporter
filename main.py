import os
import requests
from dotenv import load_dotenv

load_dotenv()

FIGMA_FILE_ID = os.getenv('FIGMA_FILE_ID')
FIGMA_API_TOKEN = os.getenv('FIGMA_API_TOKEN')

headers = {
    'X-Figma-Token': FIGMA_API_TOKEN
}

# aca se agrega el id del nodo especifico donde queremos acceder.
NODE_ID = '166-4766'
NODE_URL = f'https://api.figma.com/v1/files/{FIGMA_FILE_ID}/nodes?ids={NODE_ID}'

import os
import requests
from dotenv import load_dotenv

load_dotenv()

FIGMA_FILE_ID = os.getenv('FIGMA_FILE_ID')
FIGMA_API_TOKEN = os.getenv('FIGMA_API_TOKEN')

headers = {
    'X-Figma-Token': FIGMA_API_TOKEN
}

# Aquí se agrega el ID del nodo específico donde queremos acceder.
NODE_ID = '166-4766'
NODE_URL = f'https://api.figma.com/v1/files/{FIGMA_FILE_ID}/nodes?ids={NODE_ID}'

def obtener_datos_figma():
    """obtengo los datos de figma"""
    response = requests.get(NODE_URL, headers=headers)
    data = response.json()
    styles = data.get('styles', {})
    print(styles)

if __name__ == '__main__':
    obtener_datos_figma()
