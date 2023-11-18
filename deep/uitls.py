import tensorflow as tf
import os
import soundfile as sf


def read_audio_to_wavform(file_name: str):
    convert_to_16bit(file_name)
    x = tf.io.read_file(str(file_name))
    x, sample_rate = tf.audio.decode_wav(x, desired_channels=1, desired_samples=32000,)
    x = tf.squeeze(x, axis=-1)
    waveform = x
    return waveform

def convert_to_16bit(input_path):
    data, sample_rate = sf.read(input_path)
    sf.write(input_path, data, sample_rate, subtype='PCM_16')

def predict(model, wavform):
    return model(wavform[tf.newaxis, :])