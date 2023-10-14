import google.generativeai as palm
import speech_recognition as sr
import pyttsx3 as text_to_speech

palm.configure(api_key="YOUR API KEY")
listener = sr.Recognizer()

assistant_name = 'computer'
messages = []

defaults = {
    'model': 'models/chat-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
}


def speak(text):
    engine = text_to_speech.init()
    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[1].id)

    print(f'{assistant_name}: {text}')
    engine.say(text)
    engine.runAndWait()


def get_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=0.2)

            print('listening')
            audio = listener.listen(source)

            user_input = listener.recognize_google(audio)

            if assistant_name in user_input:
                command = user_input.replace(assistant_name, '')

                print(f'User command: {command}')
                return command
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Unknown value error.")


def send_command():
    response = palm.chat(
        **defaults,
        context="Limit yourself to 5 sentences",  # No listening to big paragraphs
        messages=messages,
    )

    messages.append({'author': '1', 'content': response.last})
    return response.last


def run_assistant():
    command = get_command()

    if command:
        messages.append({"author": '0', "content": command})

        response = send_command()
        speak(response)
        print(messages)


while True:
    run_assistant()
