from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
from preprocessing.text import Tokenizer
from sequence import pad_sequences

# Inicializar la aplicación Flask
Ubot = Flask(__name__)

# Cargar el modelo y otros recursos necesarios
model = load_model('CNN_BF_PY.h5')

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
todos_los_datos = np.concatenate((respuestas.flatten(), respuestas.flatten()))
le.fit(todos_los_datos)

max_len = 50  

def predecir_respuesta(pregunta_test):
    preguntas_test_tokens = tokenizer.texts_to_sequences([pregunta_test])
    preguntas_test_matrix = pad_sequences(preguntas_test_tokens, maxlen=max_len)
    respuesta_secuencia = model.predict(preguntas_test_matrix)
    respuesta_idx = np.argmax(respuesta_secuencia, axis=-1).flatten()
    return le.inverse_transform(respuesta_idx)

# Endpoint para predecir la respuesta
@Ubot.route('/predict', methods=['POST'])
def predict():
    data = request.json
    pregunta = data.get("pregunta","")

    # Validar si la pregunta existe
    if not pregunta:
        return jsonify({"error": "No se proporcionó ninguna pregunta"}), 400

    # Predecir la respuesta
    respuesta_predicha = predecir_respuesta(pregunta)
    return jsonify({"respuesta": respuesta_predicha.tolist()})

# Ejecutar la aplicación
if __name__ == '__main__':
    Ubot.run(debug=True)