import tkinter as tk
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
baby_voice_id = 'insert_voice_id_for_baby_voice'  # Replace with the actual voice ID for a baby voice
engine.setProperty('voice', baby_voice_id)
engine.setProperty('rate', 150)  # Adjust the speech rate as needed

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source, timeout=3)  # Set a timeout of 3 seconds for listening
        command = listener.recognize_google(audio)
        command = command.lower()
        if 'ng' in command:
            command = command.replace('ng', '')
            print(command)
        return command
    except sr.UnknownValueError:
        return ''
    except sr.RequestError:
        print('Could not connect to the speech recognition service.')
        return ''

def run_ng():
    command = take_command()
    if command:
        print(command)
        if 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk('The current time is ' + current_time)
        elif 'who is' in command:
            person = command.replace('who is', '')
            try:
                info = wikipedia.summary(person, 1)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                talk('There are multiple results. Please be more specific.')
        elif 'date' in command:
            talk('Sorry, I have a headache')
        elif 'are you single' in command:
            talk('I am in a relationship with Wi-Fi')
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif 'how are you' in command:
            HruResponse = ['I am good, what about you?', 'I am great and you?', 'Great, thank you. How are you?', 'Fine, thanks. It\'s a beautiful day.']
            talk(random.choice(HruResponse))
        elif 'hello' in command:
            talk("Hi am NG the Virtual Assist how may i help you")
        else:
            talk('Sorry, I did not understand that command.')

def start_program():
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
    while True:
        run_ng()
        response = input("Anything more, Sir? (yes/no): ")
        if response.lower() == 'no':
            break

# Create the GUI
window = tk.Tk()
window.title("NG Voice Assistant")
window.geometry("300x200")

start_button = tk.Button(window, text="Start", command=start_program)
start_button.pack(pady=20)

# Start the GUI event loop
window.mainloop()
