from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import wave
import json
import os

vosk_model_path = "vosk-model"
model = Model(vosk_model_path)


def convert_mp3_to_wav(filepath):
    try:
        audio = AudioSegment.from_mp3(filepath)
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(16000)
        wav_path = filepath.replace('.mp3', '.wav')
        audio.export(wav_path, format='wav')
        return wav_path
    except Exception as e:
        print(f'Error converting file: {e}')
        return None
    

def transcribe_audio(wav_filepath):
    results = []
    try:
        wf = wave.open(wav_filepath, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            raise ValueError("Audio file must be WAV format PCM mono.")
        
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)  # чтобы возвращались слова с временем

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                if 'result' in part_result:
                    results.extend(part_result['result'])

        # Обработка последних данных
        final_result = json.loads(rec.FinalResult())
        if 'result' in final_result:
            results.extend(final_result['result'])

        # Вернём список слов с таймингами
        return results
    except Exception as e:
        print(f"Error recognizing speech with Vosk: {e}")
        return None
