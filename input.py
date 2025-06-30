import pyaudio
import wave
import streamlit as st
import numpy as np
import whisper 
import time
#from playsound import playsound

print("Welcome to AI\n")
print("As soon as you see the mic icon, begin speaking for 5 seconds\n")
st.write("Welcome to AI\n")
st.write("As soon as you see the mic icon, begin speaking for 5 seconds\n")



CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5  
WAVE_OUTPUT_FILENAME = "output.wav"  

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("speak\n")
st.write("how may i help you?\n")

def sleep():
    for i in range(1,6):
        print(i)
        st.write(i)
        time.sleep(1)
        i+=1


frames = []

sleep()

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    


print("Processing...\n")
st.write("Processing...\n")



stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


print('Playing sound to check')
st.write('Playing sound to check')

#playsound('output.wav')
def play_audio(filename):
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()

# Replace playsound with this
play_audio('output.wav')


model = whisper.load_model("base")
result = model.transcribe("output.wav")
print(result["text"])
st.text(result["text"])