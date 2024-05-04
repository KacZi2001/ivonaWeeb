import urllib.request
import urllib.parse
from tkinter import filedialog
import tempfile
from scripts import audio_manipulation
import os


def get_final_string(voice: str, text: str) -> str:
    return "https://gaming.nightcore.pl/ivonaapi/{}?text={}".format(voice, urllib.parse.quote(text))


def get_voice_request(voice: str, text: str, pitch: float, download: bool) -> None:
    url: str = get_final_string(voice, text)
    if download:
        file_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                                 filetypes=[("WAV Files", "*.wav")])
        if file_path:
            print("Downloading file...")
            urllib.request.urlretrieve(url, file_path)

            if pitch != 0.0:
                print("Shifting audio pitch to {:.0f}...".format(pitch))
                audio_manipulation.pitch_shift(file_path, pitch)
                print("Pitch shifted")
            print("All done\n")

    else:
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        print("Getting audio...")
        urllib.request.urlretrieve(url, temp_file.name)
        temp_file.close()

        if pitch != 0.0:
            print("Shifting audio pitch to {:.0f}...".format(pitch))
            audio_manipulation.pitch_shift(temp_file.name, pitch)

        print("Playing audio...")
        audio_manipulation.play_audio(temp_file.name)
        os.remove(temp_file.name)
