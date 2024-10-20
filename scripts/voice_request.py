"""
This file is responsible for getting the audio from gaming.nightcore.pl Ivona API.
"""
import urllib.request
import urllib.parse
from tkinter import filedialog
import tempfile
import os
from time import sleep
from scripts import audio_manipulation


def get_final_string(voice: str, text: str) -> str:
    """This function adds voice and parsed text to the Ivona API URL."""
    return f"https://gaming.nightcore.pl/ivonaapi/{voice}?text={urllib.parse.quote(text)}"


def get_voice_request(voice: str, text: str, pitch: float, download: bool, progress_bar=None, progress_size=50) -> None:
    """
    This function calls the Ivona API to get a voice audio file.
    If it is for preview only it saves it as a temporary file,
    otherwise it saves it in a chosen location.
    If the pitch is different then 0 it also shifts the pitch.
    """

    def update_progress(blocknum, blocksize, totalsize):
        """
        This function is a download reporthook that updates the progress bar.
        """

        block_amount = totalsize / blocksize

        if progress_bar:

            if totalsize > 0:
                progress_bar["value"] = (blocknum / block_amount) * progress_size
                progress_bar.update_idletasks()
    
    def destroy_progress_bar():
        """
        This function sets the progress bar to max and destroys it.
        """
        if progress_bar:
            progress_bar["value"] = 99.9
            progress_bar.update_idletasks()
            sleep(0.2)
            progress_bar.pack_forget()


    url: str = get_final_string(voice, text)
    if download:
        file_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                                 filetypes=[("WAV Files", "*.wav")])
        if file_path:

            try:
                print("Downloading file...")
                urllib.request.urlretrieve(url, file_path, update_progress)

                if pitch != 0.0:
                    print(f"Shifting audio pitch to {pitch:.0f}...")
                    audio_manipulation.pitch_shift(file_path, pitch, progress_bar)
                    print("Pitch shifted")
                
                destroy_progress_bar()

                print("All done\n")
            except Exception as e:
                print(f"Error type: {type(e).__name__}, Message: {str(e)}")

    else:
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                print("Getting audio...")
                urllib.request.urlretrieve(url, temp_file.name, update_progress)

            if pitch != 0.0:
                print(f"Shifting audio pitch to {pitch:.0f}...")
                audio_manipulation.pitch_shift(temp_file.name, pitch, progress_bar)
            
            destroy_progress_bar()

            print("Playing audio...")
            audio_manipulation.play_audio(temp_file.name)
            os.remove(temp_file.name)
        except Exception as e:
            print(f"Error type: {type(e).__name__}, Message: {str(e)}")
