"""
This file is responsible for playing the audio,
stopping the audio and pitch shifting it.
"""
import contextlib
import librosa
import numpy as np
import soundfile
with contextlib.redirect_stdout(None):
    from pygame import mixer


def play_audio(filename: str) -> None:
    """This function is responsible for playing the audio."""
    sound = mixer.Sound(filename)
    sound.play()


def stop_audio() -> None:
    """This function is responsible for stopping the audio."""
    if mixer.get_busy():
        mixer.stop()


def pitch_shift(filename: str, shift: float, progress_bar=None, progress_size=49.9, progress_offset=50) -> None:
    """
    This function is responsible for resampling the audio
    and then pitch shifting it.
    """
    res_type: str = "soxr_vhq"
    y, sr = librosa.load(filename)
    new_sr = 48000
    chunk_size = 1024
    total_chunks = int(np.ceil(len(y) / chunk_size))
    res_y = []

    for i in range(total_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, len(y))
        chunk_resampled = librosa.resample(y=y[start:end], orig_sr=sr, target_sr=new_sr, res_type=res_type)
        res_y.append(chunk_resampled)

        if progress_bar:
            progress_bar["value"] = (i / total_chunks * (progress_size * 0.5)) + progress_offset
            progress_bar.update_idletasks()

    res_y = np.concatenate(res_y)
    new_y = librosa.effects.pitch_shift(
        y=res_y, sr=new_sr, n_steps=shift, res_type=res_type, bins_per_octave=32)

    if progress_bar:
        progress_bar["value"] = (progress_size * 0.75) + progress_offset
        progress_bar.update_idletasks()
    
    soundfile.write(filename, new_y, new_sr)

    if progress_bar:
        progress_bar["value"] = progress_size + progress_offset
        progress_bar.update_idletasks()
