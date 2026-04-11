import requests
import threading

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

SERVER = "https://messenger-6n21.onrender.com"


class ChatApp(App):

    def build(self):

        self.username = "User"

        root = BoxLayout(orientation='vertical')

        self.label = Label(text="Подключение...", size_hint_y=None)
        self.label.bind(texture_size=self.update_height)

        scroll = ScrollView()
        scroll.add_widget(self.label)

        root.add_widget(scroll)

        bottom = BoxLayout(size_hint_y=0.2)

        self.input = TextInput(multiline=False)
        bottom.add_widget(self.input)

        btn = Button(text="Отправить")
        btn.bind(on_press=self.send_message)
        bottom.add_widget(btn)

        root.add_widget(bottom)

        Clock.schedule_interval(self.load_messages, 3)

        return root

    def update_height(self, instance, value):
        self.label.height = self.label.texture_size[1]

    def send_message(self, instance):
        text = self.input.text.strip()
        if not text:
            return
        self.input.text = ""
        threading.Thread(target=self._send, args=(text,), daemon=True).start()

    def _send(self, text):
        try:
            requests.post(SERVER + "/send",
                          json={"name": self.username, "text": text},
                          timeout=5)
        except:
            pass

    def load_messages(self, dt):
        threading.Thread(target=self._load, daemon=True).start()

    def _load(self):
        try:
            r = requests.get(SERVER + "/messages", timeout=10)
            msgs = r.json()

            text = ""
            for m in msgs:
                text += f"{m['name']}: {m['text']}\n"

            Clock.schedule_once(lambda dt: self.update_chat(text))
        except:
            Clock.schedule_once(lambda dt: self.update_chat("Подключение..."))

    def update_chat(self, text):
        self.label.text = text


ChatApp().run()
