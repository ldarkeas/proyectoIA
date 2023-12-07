from flask import Flask, request, jsonify #importamos flask para crear la aplicacion web
from flask_cors import CORS #importamos flask_cors para habilitar las rutas
import pytube #importamos pytube para descargar videos de YouTube
import whisper  # libreria whisper para transcribir el audio
import subprocess  # libreria subprocess para llamar al archivo toxicity.js

app = Flask(__name__) #creamos la aplicacion flask y habilitar todas las rutas
CORS(app)  

@app.route('/process', methods=['POST'])
def process_video():
    youtubevideoId = request.json['url']
    try:
        model = whisper.load_model('small') # cargamos el modelo de transcripción
        youtubevideo = pytube.YouTube(youtubevideoId) # creacion de un objeto con el url del usuario
        audio = youtubevideo.streams.get_audio_only() #obtiene el audio del video
        audio.download(filename='tmp.mp4') #descarga el audio del video

        result = model.transcribe('tmp.mp4') #transcripcion del audio
        toxicity_result = subprocess.run(["node", "toxicity.js", result["text"]], check=True, capture_output=True, text=True) # se llama el archivo toxicity.js que contiene el modelo

        print('Transcripción:', result['text']) 
        print('Resultado del modelo de toxicidad:', toxicity_result.stdout) 

        return jsonify({'transcription': result['text'], 'result': toxicity_result.stdout}) 

    except Exception as e:
        return jsonify({'error': str(e)}) #se solicita un nuevo URL si es invalido ademas imprimimos el error

if __name__ == '__main__': #inicializa el servidor
    app.run(debug=True) 