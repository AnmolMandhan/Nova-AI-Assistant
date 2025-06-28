import urllib.request
import tkinter as tk
from tkinter import scrolledtext, PhotoImage
import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import os
import smtplib
import re
import requests
from googleapiclient.discovery import build

# === Hugging Face Model (Zephyr 7B) ===
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {
    "Authorization": "Bearer model_api_key_here"
}

# === Weather API ===
WEATHER_API_KEY = "your weather-api key here"

def get_ai_response(prompt):
    try:
        formatted_prompt = f"User: {prompt}\nAssistant:"
        response = requests.post(API_URL, headers=headers, json={"inputs": formatted_prompt})
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"].split("Assistant:")[-1].strip()
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text'].strip()
            else:
                return "Sorry, I couldn't understand the AI response."
        else:
            return "I'm having trouble reaching the AI model."
    except Exception:
        return "Something went wrong with the AI response."

def get_weather(city="Karachi"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()
        print("🔎 WEATHER DEBUG:", data)  # ← Add this line
        if data.get("cod") != 200:
            return "City not found."

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_report = (
            f"Weather in {city}:\n"
            f"Condition: {weather}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

        notification.notify(
            title=f"Weather Update - {city}",
            message=f"{weather.title()}, {temp}°C\nHumidity: {humidity}% | Wind: {wind_speed} m/s",
            timeout=8
        )

        return weather_report

    except:
        return "Could not retrieve the weather information."

def ask_city():
    speak("Sure, for which city?")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        append_chat("Nova", "Listening for city name...")
        audio = r.listen(source)
    try:
        city = r.recognize_google(audio, language='en-in')
        append_chat("You", city)
        return city
    except Exception:
        speak("Sorry, I didn't catch the city name.")
        append_chat("Nova", "Couldn't recognize the city.")
        return None

# === Avatar Image ===
image_url = "https://icons.iconarchive.com/icons/iconarchive/robot-avatar/128/Blue-3-Robot-Avatar-icon.png"
local_image_path = "nova.png"
if not os.path.exists(local_image_path):
    urllib.request.urlretrieve(image_url, local_image_path)

# === TTS Engine ===
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        append_chat("Nova", "Listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        append_chat("You", query)
        return query
    except Exception:
        response = "Please try again."
        speak(response)
        append_chat("Nova", response)
        return ""

# === Google Custom Search ===
GOOGLE_API_KEY = "Google_api_key_here"
SEARCH_ENGINE_ID = "search_engine_id_here"

def google_custom_search(query):
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()
        return res['items'][0]['snippet'] if 'items' in res else "No results found on Google."
    except:
        return "Google search failed."

def wikipedia_fallback(query):
    try:
        return wikipedia.summary(query, sentences=5)
    except:
        return "Wikipedia could not find anything relevant."

def is_math_expression(query):
    return bool(re.match(r'^[\d\s\.\+\-\*\/\%\(\)]+$', query))

def evaluate_math(query):
    try:
        return f"{query} = {eval(query, {'__builtins__': None}, {})}"
    except:
        return None

# === GUI ===
root = tk.Tk()
root.title("Nova - AI Assistant")
root.geometry("600x650")
root.configure(bg="#f5f5f5")

avatar_img = PhotoImage(file=local_image_path)
tk.Label(root, image=avatar_img, bg="#f5f5f5").pack(pady=10)

chat_log = scrolledtext.ScrolledText(root, height=20, width=70, state="disabled", wrap="word", font=("Arial", 12))
chat_log.pack(pady=10)

entry = tk.Entry(root, width=50, font=("Arial", 14))
entry.pack(pady=5, side="left", padx=(20, 10))

def append_chat(sender, text):
    chat_log.config(state="normal")
    chat_log.insert(tk.END, f"{sender}: {text}\n")
    chat_log.yview(tk.END)
    chat_log.config(state="disabled")

def process_request(request):
    request = request.lower().strip()

    if is_math_expression(request):
        response = evaluate_math(request) or "Sorry, I couldn't calculate that."

    elif "hello" in request:
        response = "Welcome, how can I help you?"
    elif "how are you" in request:
        response = "I'm doing great, thank you for asking! 😊 How are you doing today? How can I assist you?"

    elif "what can you do" in request or "your features" in request or "what you can do" in request:
        response = (
            "I can perform tasks like telling the time/date, playing music, doing Google and Wikipedia searches, "
            "answering questions using AI, managing your to-do list, sending emails/WhatsApp messages, checking weather, and more!"
        )
    elif request.startswith("play music"):
        song_name = request.replace("play music", "").strip()
        if song_name:
            pwk.playonyt(song_name)
            response = f"Playing {song_name} on YouTube."
        else:
            music_links = [
                "https://www.youtube.com/watch?v=c-FKlE3_kHo",
                "https://www.youtube.com/watch?v=sUf2PtEZris",
                "https://www.youtube.com/watch?v=LK7-_dgAVQE"
            ]
            webbrowser.open(random.choice(music_links))
            response = "Playing a random music track."

    elif "say time" in request:
        response = datetime.datetime.now().strftime("Current time is %H:%M")
    elif "say date" in request:
        response = datetime.datetime.now().strftime("Current date is %d-%m-%Y")
    elif "new work" in request:
        task = request.replace("new work", "").strip()
        with open("todo.txt", "a") as f:
            f.write(task + "\n")
        response = f"Task added: {task}"
    elif "tell me work" in request:
        try:
            with open("todo.txt", "r") as f:
                response = "Tasks: " + f.read()
        except FileNotFoundError:
            response = "No tasks found."
    elif "show work" in request:
        try:
            with open("todo.txt", "r") as f:
                notification.notify(title="Today's work", message=f.read())
            response = "Work shown in notification."
        except FileNotFoundError:
            response = "No tasks found to show."
    elif "open youtube" in request:
        webbrowser.open("https://youtube.com")
        response = "Opening YouTube."
    elif "open facebook" in request:
        webbrowser.open("https://www.facebook.com/")
        response = "Opening Facebook."
    elif "open Instagram" in request:
        webbrowser.open("https://www.instagram.com/")
        response = "Opening Instagram."
    elif "open Linkedin" in request:
        webbrowser.open("https://www.linkedin.com/")
        response = "Opening LinkedIn."
    elif "open whatsapp" in request:
        webbrowser.open("https://web.whatsapp.com/")
        response = "Opening WhatsApp."



    elif "open" in request:
        app = request.replace("open", "").strip()
        pyautogui.press("super")
        pyautogui.typewrite(app)
        pyautogui.sleep(2)
        pyautogui.press("enter")
        response = f"Opening {app}."
    elif "search google" in request:
        search_query = request.replace("search google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        response = f"Searching Google for {search_query}."
    elif "send whatsapp" in request:
        pwk.sendwhatmsg("+910123456789", "Hi How are you", 16, 9)
        response = "WhatsApp message sent."
    elif "send email" in request:
        try:
            sender = "your_email@gmail.com"
            pwd = "your_app_password"
            with smtplib.SMTP("smtp.gmail.com", 587) as s:
                s.starttls()
                s.login(sender, pwd)
                s.sendmail(sender, "email@gmail.com", "Subject: Hello\n\nHello, how are you...")
            response = "Email sent successfully."
        except:
            response = "Failed to send email."
    elif any(x in request for x in ["who created you", "your name", "who creates you", "who are you", "what is your name", "tell me something about you"]):
        response = "I am Nova, your AI assistant, created by Madam Anmol Mandhan."
    elif "weather" in request:
        city_match = re.search(r'in ([a-zA-Z\s]+)', request) or re.search(r'of ([a-zA-Z\s]+)', request)
        if city_match:
            city = city_match.group(1).strip()
        else:
            city = ask_city()

        if city:
            response = get_weather(city)
        else:
            response = "I couldn't get the city name. Please try again."
    else:
        response = get_ai_response(request)
        if response.startswith("Sorry") or "trouble" in response or "couldn't" in response:
            response = wikipedia_fallback(request)
        if response.startswith("Sorry") or "could not" in response or "Wikipedia" in response:
            response = google_custom_search(request)

    append_chat("Nova", response)
    speak(response)

def on_enter(event=None):
    query = entry.get()
    if query:
        append_chat("You", query)
        process_request(query)
        entry.delete(0, tk.END)

def on_mic():
    query = command()
    if query:
        process_request(query)

def clear_chat():
    chat_log.config(state="normal")
    chat_log.delete("1.0", tk.END)
    chat_log.config(state="disabled")

tk.Button(root, text="🎙️", font=("Arial", 12), command=on_mic).pack(side="left", padx=5)
tk.Button(root, text="Send", font=("Arial", 12), command=on_enter).pack(side="left", padx=5)
tk.Button(root, text="Clear", font=("Arial", 12), command=clear_chat).pack(side="left", padx=5)

root.bind("<Return>", on_enter)
root.mainloop()
