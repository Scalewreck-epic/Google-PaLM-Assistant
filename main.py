import google.generativeai as palm
import speech_recognition as sr
import pyttsx3 as text_to_speech

listener = sr.Recognizer()
engine = text_to_speech.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

palm.configure(api_key="YOUR API KEY")

assistant_name = 'computer'

defaults = {
    'model': 'models/chat-bison-001',
    'temperature': 0.6,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
}


def respond(text):
    engine.say(text)
    engine.runAndWait()


def get_command():
    try:
        with sr.Microphone() as source:
            print('listening')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

            if assistant_name in command:
                command = command.replace(assistant_name, '')

                print('You: ' + command)
    except:
        pass
    return command


def run_assistant():
    command = get_command()

    if command:
        print("Loading response..")
        response = palm.chat(
            **defaults,
            prompt=command
        )

        print(response)
        respond(response.last)
    else:
        pass


run_assistant()
