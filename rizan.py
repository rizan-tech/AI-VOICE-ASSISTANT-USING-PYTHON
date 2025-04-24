import openai
import pyttsx3
import speech_recognition as sr
from datetime import datetime

# === CONFIGURE OPENAI API KEY ===
OPENAI_API_KEY = "your_openai_api_key_here"
openai.api_key = OPENAI_API_KEY

# === INIT TTS ENGINE ===
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    """Convert text to speech."""
    print("rizan:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for user commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return ""

def ask_gpt(prompt):
    """Ask GPT-4 for a response."""
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Use GPT-4 turbo for a faster response
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def get_time():
    """Return the current time."""
    current_time = datetime.now().strftime("%H:%M")
    return f"The current time is {current_time}."

def smart_rizan(prompt):
    """Process the command and call relevant functions."""
    try:
        # Handle simple built-in commands
        if "time" in prompt.lower():
            return get_time()

        # Ask GPT-4 for general queries
        return ask_gpt(prompt)
    except Exception as e:
        return f"Something went wrong: {e}"

# === MAIN LOOP ===
if __name__ == "__main__":
    speak("Hello, I'm rizan. What can I do for you?")
    while True:
        command = listen()
        if command.lower() in ["exit", "quit", "stop"]:
            speak("Goodbye!")
            break
        if command:
            reply = smart_rizan(command)
            speak(reply)
