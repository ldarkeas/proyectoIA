import pytube  # libreria pytube para descargar videos de YouTube
import whisper  # libreria whisper para transcribir el audio
import subprocess

valid_url = False  # variable para verificar si la URL es válida


while not valid_url:
    # solicitamos al usuario que ingrese la URL del video de YouTube
    youtubevideoId = input("Por favor, ingrese la URL del video de YouTube: ")

    try:
        model = whisper.load_model('small') # cargamos el modelo de transcripción

        youtubevideo = pytube.YouTube(youtubevideoId) # creamos un objeto YouTube con la URL proporcionada por el usuario
        audio = youtubevideo.streams.get_audio_only() # Obtenemos el audio del video
        audio.download(filename='tmp.mp4')

        result = model.transcribe('tmp.mp4') # transcribe the downloaded audio
        print(result["text"])

        # Call the JavaScript file
        subprocess.run(["node", "toxicity.js", result["text"]], check=True)

        valid_url = True

    except Exception as e:
        print(f"Ocurrió un error: {e}. Por favor, intente con otra URL.") #se solicita un nuevo URL si es invalido ademas imprimimos el error


