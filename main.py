import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

SERVER = "https://messenger-6n21.onrender.com"

class ChatApp(App):
    def build(self):
        self.name = "User"

        layout = BoxLayout(orientation='vertical')

        self.chat = Label(text="Чат\n")
        layout.add_widget(self.chat)

        self.input = TextInput(multiline=False)
        layout.add_widget(self.input)

        btn = Button(text="Отправить")
        btn.bind(on_press=self.send)
        layout.add_widget(btn)

        Clock.schedule_interval(self.load, 2)

        return layout

    def send(self, instance):
        if self.input.text:
            requests.post(SERVER + "/send", json={
                "name": self.name,
                "text": self.input.text
            })
            self.input.text = ""

    def load(self, dt):
        try:
            r = requests.get(SERVER + "/messages")
            msgs = r.json()
            self.chat.text = ""
            for m in msgs:
                self.chat.text += m["name"] + ": " + m["text"] + "\n"
        except:
            self.chat.text = "Ошибка"

ChatApp().run()
