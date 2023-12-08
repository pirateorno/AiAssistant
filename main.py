import pyttsx3
from tkinter import *
from tkinter import messagebox
from openai import OpenAI
import speech_recognition as sr
import webbrowser


# tkinter
root = Tk()
# tts
engine = pyttsx3.init()
for voice in engine.getProperty('voices'):
    print(voice, voice.id)
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0")
# openai
client = ""
# voice to text
r = sr.Recognizer()

OpenAIkey = StringVar()
text = StringVar()

def SaveSetting():
    global client
    client = OpenAI(api_key=OpenAIkey.get())
    if "sk-" in OpenAIkey.get():
        messagebox.showinfo(title="Внимание!", message="Сохранено!")
    else:
        messagebox.showerror(title="Внимание!", message="Ключ не написан или в начале нету sk-")

def startRecording():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        global text
        text = r.recognize_whisper(audio, language="Russian")
        userText.config(text=text.get())
        askai()
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper")

def startWriting():
    userText.config(text=text.get())
    askai()

completion = ""


def askai():
    if "Открой ютуб" in text.get() and not "и найди" in text.get():
        webbrowser.open_new_tab("https://www.youtube.com")
    elif "Открой ютуб и найди" in text.get():
        search = text.get().replace("Открой ютуб и найди", "")
        webbrowser.open_new_tab("https://www.youtube.com/results?search_query=" + search)
    global completion
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": 'Ты теперь личный асистент. Тебя зовут Олег. Говори не много и по делу'},
            {"role": "user", "content": text.get()}
        ],
        temperature=1
    )
    aiText.config(text=completion.choices[0].message.content)
    engine.say(completion.choices[0].message.content)
    engine.runAndWait()


openaiApitext = Label(root, text="Ваш openai api ключ:")
openaiApitext.pack()
openaiApi = Entry(root, textvariable=OpenAIkey)
openaiApi.pack()
openaiApiButton = Button(root, text="Сохранить", command=SaveSetting)
openaiApiButton.pack()

recordButton = Button(root, text='Включить микрофон', command=startRecording)
recordButton.pack()
orText = Label(root, text="Или")
orText.pack()
writeButton = Button(root, text='Написать вручную', command=startWriting)
writeButton.pack()
writeField = Entry(root, textvariable=text)
writeField.pack()

userText = Label(root)
userText.pack()
aiText = Label(root)
aiText.pack()

root.mainloop()
