from flask import Flask, request, render_template, jsonify
import serial
import speech_recognition as sr

app = Flask(__name__)
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)  # Replace with the correct serial port

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Recognized:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        voice_input = recognize_speech()
        if voice_input:
            ser.write(voice_input.encode())
            temperature_data = ser.readline().decode().strip()
            return jsonify({'temperature': temperature_data})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
