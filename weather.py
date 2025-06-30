import requests

import pyaudio
import wave
import streamlit as st
import numpy as np
import whisper 
import time
from playsound import playsound

print("Welcome to AI\n")
print("As soon as you see the mic icon, begin speaking for 5 seconds\n")
st.write("Welcome to AI\n")
st.write("As soon as you see the mic icon, begin speaking for 5 seconds\n")


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
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

playsound('output.wav')


model = whisper.load_model("base")
result = model.transcribe("output.wav")
print(result["text"])
st.text(result["text"])


OPENWEATHER_API_KEY = "689de3ceb70edd29fd1ffd01adec3f5c"

class WeatherAgent:
    def _init_(self, api_key):
        self.api_key = api_key
    
    def get_weather(self, city_name):
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        return response.json()
    
    def parse_weather_info(self, weather_data, days):
        temperatures = []
        probabilities = []

        for forecast in weather_data['list'][:days]:  
            temperature = forecast['main']['temp']
            rain = forecast.get('rain', {}).get('3h', 0) 
            temperatures.append(f"{temperature}°C")
            probabilities.append(f"{rain}%")

        return temperatures, probabilities
    
    def format_weather_info(self, city_name, temperatures, probabilities, days):
        formatted_info = f"Weather forecast for {city_name} for the next {days} days:\n"
        for i in range(days):
            formatted_info += f"Day {i+1}: Temperature: {temperatures[i]}, Rainfall Probability: {probabilities[i]}\n"
        return formatted_info
    
    def run(self):
        user_input = result 
        parts = user_input.split()
        city_name = " ".join(parts[:-1])
        days = int(parts[-1])

        weather_data = self.get_weather(city_name)
        temperatures, probabilities = self.parse_weather_info(weather_data, days)
        formatted_info = self.format_weather_info(city_name, temperatures, probabilities, days)

        print(formatted_info)


weather_agent = WeatherAgent(OPENWEATHER_API_KEY)
weather_agent.run()

