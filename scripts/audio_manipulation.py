import librosa
import soundfile
import contextlib
with contextlib.redirect_stdout(None):
    from pygame import mixer


def play_audio(filename: str) -> None:
    sound = mixer.Sound(filename)
    sound.play()


def stop_audio() -> None:
    if mixer.get_busy():
        mixer.stop()


def pitch_shift(filename: str, shift: float) -> None:
    res_type: str = "soxr_vhq"
    y, sr = librosa.load(filename)
    new_sr = 48000
    res_y = librosa.resample(y=y, orig_sr=sr, target_sr=new_sr, res_type=res_type)
    new_y = librosa.effects.pitch_shift(y=res_y, sr=new_sr, n_steps=shift, res_type=res_type, bins_per_octave=32)
    soundfile.write(filename, new_y, new_sr)
