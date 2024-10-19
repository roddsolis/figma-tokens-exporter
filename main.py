import os
import json
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# ID del archivo de Figma y token de autenticación (se obtiene desde las variables de entorno)
FIGMA_FILE_ID = os.getenv('FIGMA_FILE_ID')  # Asegúrate de que esto esté en tu archivo .env
FIGMA_API_TOKEN = os.getenv('FIGMA_API_TOKEN')

# Encabezado de autorización para la API de Figma
headers = {
    'X-Figma-Token': FIGMA_API_TOKEN
}

# URL base para la API de Figma
NODE_ID = '166-4766'  # El ID del nodo específico que quieres obtener
NODE_URL = f'https://api.figma.com/v1/files/{FIGMA_FILE_ID}/nodes?ids={NODE_ID}'

# Función para obtener los datos del archivo Figma
def get_figma_data():
    try:
        # Hacer la solicitud a la API
        response = requests.get(NODE_URL, headers=headers)  # Usa NODE_URL aquí
        response.raise_for_status()  # Verifica si hay errores en la respuesta
        
        data = response.json()
        
        # Guardar la respuesta en un archivo para analizarla
        with open('figma_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print('Datos de Figma guardados en figma_response.json')
        return data  # Devuelve los datos en formato JSON
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener los datos de Figma: {e}')
        return None

# Función para procesar los estilos y convertirlos a un formato compatible con Style Dictionary
def process_figma_styles(data):
    if not data:
        return {}

    tokens = {
        "color": {},
        "font": {},
        "spacing": {},
        "border": {},
        "border_radius": {},
    }

    # Asegúrate de que 'styles' esté presente en los datos de Figma
    if 'styles' in data:
        for key, style in data['styles'].items():
            # Procesar colores
            if 'style_type' in style:
                if style['style_type'] == 'FILL' and 'fills' in style and style['fills']:
                    color = style['fills'][0]['color']
                    tokens['color'][style['name']] = {
                        'value': f"rgba({int(color['r'] * 255)}, {int(color['g'] * 255)}, {int(color['b'] * 255)}, {color['a']})",
                        'type': 'color'
                    }
                
                # Procesar tipografías
                elif style['style_type'] == 'TEXT':
                    tokens['font'][style['name']] = {
                        'font_family': style['style']['fontFamily'],
                        'font_weight': style['style']['fontWeight'],
                        'font_size': style['style']['fontSize'],
                        'line_height': style['style']['lineHeightPx'],  # Ajusta según la estructura real
                    }

                # Procesar espaciados (asumiendo que tienes un estilo para espaciados)
                elif style['style_type'] == 'SPACING':
                    tokens['spacing'][style['name']] = {
                        'value': style['style']['value'],  # Ajusta según la estructura real
                        'type': 'spacing'
                    }

                # Procesar bordes
                elif style['style_type'] == 'BORDER':
                    tokens['border'][style['name']] = {
                        'width': style['style']['borderWidth'],  # Ajusta según la estructura real
                        'style': style['style']['borderStyle'],  # Si existe
                    }

                # Procesar radios de borde
                elif style['style_type'] == 'CORNER_RADIUS':
                    tokens['border_radius'][style['name']] = {
                        'value': style['style']['cornerRadius'],  # Ajusta según la estructura real
                    }

    return tokens


# Guardar los tokens en un archivo JSON compatible con Style Dictionary
def save_tokens_to_json(tokens, filename='tokens.json'):
    with open(filename, 'w') as f:
        json.dump(tokens, f, indent=2)
    print(f'Tokens guardados en {filename}')

# Función principal
def main():
    # Obtener los datos de Figma
    figma_data = get_figma_data()

    if figma_data:
        # Procesar los estilos de Figma y convertirlos en tokens
        tokens = process_figma_styles(figma_data)
        # Guardar los tokens en un archivo JSON
        save_tokens_to_json(tokens)

if __name__ == '__main__':
    main()
