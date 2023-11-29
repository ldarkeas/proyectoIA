import whisper
import pytube
import pandas


youtubevideoId = "https://www.youtube.com/shorts/LIZat528bzE"  # URL del video de youtube
model = whisper.load_model('small')

youtubevideo = pytube.YouTube(youtubevideoId)
audio = youtubevideo.streams.get_audio_only()
audio.download(filename="tmp.mp4")

result = model.transcribe('tmp.mp4')
print(result["text"])