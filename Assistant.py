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

def find_nearby_food_shops(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=500&keyword=food&key=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()

    places = []
    if data['status'] == 'OK':
        for result in data['results']:
            places.append(result['name'])
    return places

def run_ng():
    while True:
        command = take_command()
        if command:
            if 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                response_text = 'The current time is ' + current_time
                talk(response_text)
                output_label.config(text=response_text)
            elif 'who is' in command:
                person = command.replace('who is', '')
                try:
                    info = wikipedia.summary(person, 1)
                    response_text = info
                    talk(response_text)
                    output_label.config(text=response_text)
                except wikipedia.exceptions.DisambiguationError:
                    response_text = 'There are multiple results. Please be more specific.'
                    talk(response_text)
                    output_label.config(text=response_text)
            elif 'play' in command:
                song = command.replace('play', '')
                response_text = 'Playing ' + song
                talk(response_text)
                output_label.config(text=response_text)
                pywhatkit.playonyt(song)
            elif 'are you single' in command:
                response_text = 'I am in a relationship with Wi-Fi'
                talk(response_text)
                output_label.config(text=response_text)
            elif 'joke' in command:
                joke = pyjokes.get_joke()
                response_text = joke
                talk(response_text)
                output_label.config(text=response_text)
            elif 'date' in command:
                response_text = 'Sorry, I have a headache'
                talk(response_text)
                output_label.config(text=response_text)
            elif 'how are you' in command:
                HruResponse = ['I am good, what about you?', 'I am great and you?', 'Great, thank you. How are you?', 'Fine, thanks. It\'s a beautiful day.']
                response_text = random.choice(HruResponse)
                talk(response_text)
                output_label.config(text=response_text)
            elif 'what is my current location' in command:
                location = geocoder.ip('me')
                response_text = 'Your current location is ' + location.city
                talk(response_text)
                output_label.config(text=response_text)
            elif 'food' in command or 'restaurant' in command:
                location = geocoder.ip('me')
                user_location = location.latlng
                if user_location:
                    places = find_nearby_food_shops(user_location[0], user_location[1])
                    if places:
                        response_text = "Here are some nearby food shops or famous restaurants:\n" + "\n".join(places)
                        talk(response_text)
                        output_label.config(text=response_text)
                    else:
                        response_text = "Sorry, I couldn't find any nearby food shops or famous restaurants."
                        talk(response_text)
                        output_label.config(text=response_text)
                else:
                    response_text = "Sorry, I couldn't determine your current location."
                    talk(response_text)
                    output_label.config(text=response_text)
            elif 'stop' in command or 'exit' in command:
                response_text = 'Goodbye.'
                talk(response_text)
                output_label.config(text=response_text)
                break
            else:
                response_text = 'Sorry, I did not understand that command.'
                talk(response_text)
                output_label.config(text=response_text)

            talk('Anything more?')  # Ask for further questions
            response = take_command()  # Get the user's response
            if response and ('no' in response or 'stop' in response or 'exit' in response):
                response_text = 'Goodbye.'
                talk(response_text)
                output_label.config(text=response_text)
                break
            elif response:
                command = response
                continue
            else:
                break

def on_button_click():
    run_ng()

# Create the GUI window
T = Tk()
T.title("Voice Assistant")
T.geometry("400x400")

# Create a button
button = Button(T, text="Click to Speak", command=on_button_click)
button.pack(pady=20)

# Create a label to display the output
output_label = Label(T, text="")
output_label.pack(pady=20)

# Run the GUI event loop
T.mainloop()
