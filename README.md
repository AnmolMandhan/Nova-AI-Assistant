# Virtual Assistant 🤖

Virtual Assistant is a powerful AI-based voice assistant built using Python. It provides both GUI and voice-based interactions to help users with a wide range of tasks like checking the weather, playing music, web searches, to-do list management, sending emails, and answering general questions using an AI model.

---

## ✨ Features & Functionality

Below is a list of Virtual Assistant core features with brief explanations:


| Feature | Description |
|--------|-------------|
| 🎙️ **Voice Recognition** | Listens to your commands using `speech_recognition` and a microphone. |
| 🧠 **AI Responses (Hugging Face)** | Uses Zephyr-7B model from Hugging Face for natural language responses when it doesn’t match any predefined command. |
| 🌤️ **Weather Updates** | Speaks and shows the current weather of any city using OpenWeatherMap API. |
| 📆 **Date & Time Reporting** | Tells the current date and time using the system clock. |
| 🎵 **Music Playback** | Plays a song on YouTube using `pywhatkit` — just say "Play music [song name]". |
| 🔍 **Google Search** | Opens search results in the browser for any topic using Google search (manual or voice input). |
| 📚 **Wikipedia Info** | If AI fails, it tries to fetch summary info from Wikipedia as fallback. |
| ✅ **To-do List** | You can add tasks ("new work ...") and view them ("tell me work" or "show work"). |
| 💬 **GUI Chat Interface** | Provides a text chat interface using `tkinter` with chat history and speech output. |
| 📧 **Email Sending** | Can send a predefined email using SMTP (credentials required in code). |
| 💬 **WhatsApp Message** | Sends a message at a given time to a specified number using `pywhatkit.sendwhatmsg`. |
| 📲 **App Launcher** | Opens apps installed on your system by voice or text command like "open calculator". |
| 🔔 **Desktop Notifications** | Sends pop-up notifications for tasks and weather via `plyer`. |
| 🖼️ **Avatar UI** | Displays a friendly robot avatar image in the GUI window. |

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Tkinter | GUI |
| pyttsx3 | Text-to-speech |
| speech_recognition | Speech-to-text |
| pywhatkit | YouTube & WhatsApp |
| wikipedia | Information fallback |
| requests | API interactions |
| plyer | Notifications |
| Hugging Face API | AI chat model |
| OpenWeatherMap API | Weather updates |
| Google Custom Search API | Final fallback |

## 🔧 How to Run Locally

1. **Clone the repository**
   
2. **Install the dependencies**
   
   **pip install -r requirements.txt**
   
3. **Set API Keys**
   
   Replace placeholders in Nova.py:
   
   model_api_key_here (Hugging Face)
   
   your weather-api key here (OpenWeather)
   
   Google_api_key_here & search_engine_id_here
   
   
4. **Run the app**
   
    python Nova.py
   
   
**💡 Example Commands**

"What's the weather in Lahore?"

"New work complete the report"

"Tell me my work"

"Play music Faded"

"Who created you?"

"Search Google for Python projects"

"Open calculator"

"Send WhatsApp message"

**🙌 Credits**

Hugging Face

OpenWeatherMap

Google Programmable Search

Wikipedia API

pywhatkit

💼 Author

👤 Anmol Mandhan

💻 Django | Python | Frontend Developer | AI/ML

📎 LinkedIn Profile | www.linkedin.com/in/anmol-mandhan-6a80362a8

🌟 Give a Star!

If you like this project, don’t forget to ⭐ star it on GitHub!








