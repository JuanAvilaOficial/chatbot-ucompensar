from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from keras._tf_keras.keras.models import load_model
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

# Inicializar la aplicación Flask
Ubot = Flask(__name__)

# Cargar el modelo y otros recursos necesarios
model = load_model('modelo_cnn_software.h5')

# Cargar el Tokenizer y el LabelEncoder
file_path = 'PreguntasChat.xlsx'
excel_data = pd.ExcelFile(file_path)
software_sheet = excel_data.parse('HARDWARE')
preguntas = software_sheet.iloc[:, 1].astype(str).tolist()  
respuestas = software_sheet.iloc[:, 2:31].values  

# Configuración del Tokenizer y LabelEncoder
tokenizer = Tokenizer()
tokenizer.fit_on_texts(preguntas)

le = LabelEncoder()
# Combinar todas las respuestas para entrenar el LabelEncoder
todos_los_datos = respuestas.flatten()
le.fit(todos_los_datos)

# Configuraciones adicionales
max_len = 50  # Longitud máxima de secuencia

# Función de predicción
def predecir_respuesta(pregunta_test):
    try:
        # Tokenizar la pregunta de entrada
        preguntas_test_tokens = tokenizer.texts_to_sequences([pregunta_test])
        preguntas_test_matrix = pad_sequences(preguntas_test_tokens, maxlen=max_len)

        # Realizar la predicción
        respuesta_secuencia = model.predict(preguntas_test_matrix)
        respuesta_idx = np.argmax(respuesta_secuencia, axis=-1).flatten()
        respuesta_texto = le.inverse_transform(respuesta_idx)
        return respuesta_texto[0]  # Retorna la primera respuesta como cadena
    except Exception as e:
        return f"Error en la predicción: {e}"

# Endpoint para predecir la respuesta
@Ubot.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        pregunta = data.get("pregunta")
        
        # Validar si la pregunta existe
        if not pregunta:
            return jsonify({"error": "No se proporcionó ninguna pregunta"}), 400

        # Predecir la respuesta
        respuesta_predicha = predecir_respuesta(pregunta)

        # Asegurarse de convertir cualquier objeto a cadena legible
        return jsonify({"respuesta": str(respuesta_predicha)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ejecutar la aplicación
if __name__ == '__main__':
    Ubot.run(debug=True)
