from flask import Flask, render_template, request, redirect
import speech_recognition as sr
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_started():
    if request.method == "POST":
        name = request.form.get("name")
        phone_number = request.form.get("phone_number")
        return redirect("/index?name={}&phone_number={}".format(name, phone_number))
    return render_template('getstarted.html')

@app.route("/index", methods=["GET", "POST"])
def index():
    transcript = ""
    name = request.args.get("name")
    phone_number = request.args.get("phone_number") 
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)

    return render_template('index.html', transcript=transcript, name=name, phone_number=phone_number)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
