from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from keras._tf_keras.keras.models import load_model
from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

# Inicializar la aplicación Flask
Ubot = Flask(__name__)

# Cargar el modelo y otros recursos necesarios
model = load_model('modelo_chatbot.keras')

# Cargar el Tokenizer y el LabelEncoder
file_path = 'Preguntas_Universidad.xlsx'
excel_data = pd.ExcelFile(file_path)
software_sheet = excel_data.parse('ESTUDIANTES')
print(software_sheet.columns)
preguntas = software_sheet.iloc[:, 1].values
respuestas = software_sheet.iloc[:, 3:13].values  

# Configuración del Tokenizer y LabelEncoder
tokenizer = Tokenizer()
tokenizer.fit_on_texts(preguntas)

le = LabelEncoder()

todos_los_datos = np.concatenate((respuestas.flatten(), respuestas.flatten()))
le.fit(todos_los_datos)

max_len = 100 
umbral = 0.35

def predecir_respuesta(pregunta_hecha):
    try:
        if len(pregunta_hecha.split()) < 2:
            return "Parece que tu pregunta está incompleta o no tiene sentido."
            
        preguntas_test_tokens = tokenizer.texts_to_sequences([pregunta_hecha])
        preguntas_test_matrix = pad_sequences(preguntas_test_tokens, maxlen=max_len)

        respuesta_secuencia = model.predict(preguntas_test_matrix)
        respuesta_idx = np.argmax(respuesta_secuencia, axis=-1).flatten()

        acierto = np.max(respuesta_secuencia)
        if acierto < umbral:
            return "No puedo responder a esa pregunta"

        respuesta_texto = le.inverse_transform(respuesta_idx)
        return respuesta_texto[0] 
     
    except Exception as e:
        return f"Error en la predicción: {e}"

@Ubot.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        pregunta = data.get("pregunta")
        
        if not pregunta:
            return jsonify({"error": "No se proporcionó ninguna pregunta"}), 400

        respuesta_predicha = predecir_respuesta(pregunta)
        
        print(f"Respuesta: {respuesta_predicha}")
        return jsonify({"respuesta": str(respuesta_predicha)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    Ubot.run(debug=True)
