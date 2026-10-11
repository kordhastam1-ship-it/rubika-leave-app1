from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class RubikaApp(App):

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title = Label(
            text="مدیریت کانال‌های روبیکا",
            font_size=24
        )
        layout.add_widget(title)

        info = Label(
            text="برای مدیریت کانال‌های حساب خودت",
            font_size=16
        )
        layout.add_widget(info)

        self.phone = TextInput(
            hint_text="شماره تلفن",
            multiline=False,
            input_type="tel",
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.phone)

        button = Button(
            text="شروع",
            size_hint_y=None,
            height=55
        )

        button.bind(on_press=self.show_message)
        layout.add_widget(button)

        return layout

    def show_message(self, instance):
        popup = Popup(
            title="اطلاع",
            content=Label(
                text="رابط برنامه آماده است؛ اتصال به روبیکا هنوز انجام نشده."
            ),
            size_hint=(0.85, 0.35)
        )
        popup.open()


if __name__ == "__main__":
    RubikaApp().run()
