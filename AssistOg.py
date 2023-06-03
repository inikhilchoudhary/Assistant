from tkinter import *
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random
import geocoder
import requests
import threading
from PIL import ImageTk, Image
import googlesearch


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
baby_voice_id = 'insert_voice_id_for_baby_voice'  # Replace with the actual voice ID for a baby voice
engine.setProperty('voice', baby_voice_id)
engine.setProperty('rate', 150)  # Adjust the speech rate as needed

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_voice_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source, timeout=1)  # Set a timeout of 1 second for listening
        command = listener.recognize_google(audio)
        command = command.lower()
        if 'ng' in command:
            command = command.replace('ng', '')
        return command
    except sr.UnknownValueError:
        return ''
    except sr.RequestError:
        return ''

def take_text_command():
    command = input("Enter command: ")
    command = command.lower()
    if 'ng' in command:
        command = command.replace('ng', '')
    return command

def find_nearby_food_shops(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=500&keyword=food&key=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()

    places = []
    if data['status'] == 'OK':
        for result in data['results']:
            places.append(result['name'])
    return places

def search_google(query):
    search_results = googlesearch.search(query, num_results=1)
    if search_results:
        return search_results[0]
    else:
        return None
    
def run_ng(input_method, command=None):
    while True:
        if command:
            if 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                response_text = 'The current time is ' + current_time
                talk(response_text)

            elif 'who is' in command:
                person = command.replace('who is', '')
                try:
                    info = wikipedia.summary(person, 1)
                    response_text = info
                    talk(response_text)
                except wikipedia.exceptions.DisambiguationError:
                    response_text = 'There are multiple results. Please be more specific.'
                    talk(response_text)

            elif 'play' in command:
                song = command.replace('play', '')
                response_text = 'Playing ' + song
                talk(response_text)
                pywhatkit.playonyt(song)

            elif 'are you single' in command:
                response_text = 'I am in a relationship with Wi-Fi'
                talk(response_text)

            elif 'joke' in command:
                joke = pyjokes.get_joke()
                response_text = joke
                talk(response_text)

            elif 'date' in command:
                response_text = 'Sorry, I have a headache'
                talk(response_text)

            elif 'how are you' in command:
                HruResponse = ['I am good, what about you?', 'I am great and you?', 'Great, thank you. How are you?', 'Fine, thanks. It\'s a beautiful day.']
                response_text = random.choice(HruResponse)
                talk(response_text)

            elif 'what is my current location' in command:
                location = geocoder.ip('me')
                response_text = 'Your current location is ' + location.city
                talk(response_text)

            elif 'food' in command or 'restaurant' in command:
                location = geocoder.ip('me')
                user_location = location.latlng
                if user_location:
                    places = find_nearby_food_shops(user_location[0], user_location[1])
                    if places:
                        response_text = "Here are some nearby food shops or famous restaurants:\n" + "\n".join(places)
                        talk(response_text)
                    else:
                        response_text = "Sorry, I couldn't find any nearby food shops or famous restaurants."
                        talk(response_text)
                else:
                    response_text = "Sorry, I couldn't determine your current location."
                    talk(response_text)

            elif any(word in command for word in ['what', 'when', 'which', 'who', 'where']):
                try:
                    query = command.replace('what', '').replace('when', '').replace('which', '').replace('who', '').replace('where', '')
                    search_result = search_google(query)
                    if search_result:
                        response_text = "According to Google, " + search_result
                    else:
                        response_text = "I'm sorry, I couldn't find the information."
                except:
                    response_text = 'There was an error while searching. Please try again later.'
                talk(response_text)

            elif 'stop' in command or 'exit' in command:
                response_text = 'Goodbye.'
                talk(response_text)
                break

            else:
                response_text = 'Sorry, I did not understand that command.'
                talk(response_text)

            talk('Anything more?')  # Ask for further questions
            if input_method == 'voice':
                response = take_voice_command()
            else:
                response = take_text_command()

            if response and any(word in response for word in ['no', 'stop', 'exit']):
                response_text = 'Goodbye.'
                talk(response_text)
                break
            elif response:
                command = response
                continue
            else:
                break
        else:
            if input_method == 'voice':
                command = take_voice_command()
            else:
                command = take_text_command()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_voice_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source, timeout=1)  # Set a timeout of 1 second for listening
        command = listener.recognize_google(audio)
        command = command.lower()
        if 'ng' in command:
            command = command.replace('ng', '')
        return command
    except sr.UnknownValueError:
        return ''
    except sr.RequestError:
        return ''

def take_text_command():
    command = input("Enter command: ")
    command = command.lower()
    if 'ng' in command:
        command = command.replace('ng', '')
    return command

def find_nearby_food_shops(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=500&keyword=food&key=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()

    places = []
    if data['status'] == 'OK':
        for result in data['results']:
            places.append(result['name'])
    return places

def search_google(query):
    search_results = googlesearch.search(query, num_results=1)
    if search_results:
        return search_results[0]
    else:
        return None

def on_mic_button_click():
    threading.Thread(target=lambda: run_ng('voice')).start()

def on_text_button_click():
    threading.Thread(target=lambda: run_ng('text')).start()

# Create the GUI window
T = Tk()
T.title("HelpU")
T.geometry("530x510")

# Set the window icon
T.iconbitmap("AssistantIcon.ico")

# Load the background image
background_image = ImageTk.PhotoImage(Image.open("WinBackIma.png"))

# Create a Label widget to hold the background image
background_label = Label(T, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load the "Mic" and "Text" button images and resize them
mic_button_image = ImageTk.PhotoImage(Image.open("mic.png").resize((30, 30)))
text_button_image = ImageTk.PhotoImage(Image.open("text.png").resize((30, 30)))

# Create buttons for Mic and Text input
mic_button = Button(T, image=mic_button_image, bd=0, command=on_mic_button_click)
mic_button.grid(row=0, column=0, padx=10, pady=10)

text_button = Button(T, image=text_button_image, bd=0, command=on_text_button_click)
text_button.grid(row=0, column=1, padx=10, pady=10)

# Configure grid weights to make the background image resize with the window
T.grid_rowconfigure(0, weight=1)
T.grid_columnconfigure(0, weight=1)
T.grid_columnconfigure(1, weight=1)

# Run the GUI event loop
T.mainloop()
