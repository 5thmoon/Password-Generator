import kivy
kivy.require('2.1.0')
# kivy config, not-resizable
from kivy.config import Config

Config.set('graphics', 'resizable', 0)

# set kivy window size
from kivy.core.window import Window

Window.size = (400, 700)

# kivy imports
from kivy.core.clipboard import Clipboard
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen

# kivymd imports
from kivymd.toast import toast
from kivymd.app import MDApp

# python imports
import secrets
import string

kv = """
ScreenManager:
    Generator:
<Generator>:
    MDScreen:
    MDFloatLayout:
        slider_val: slider_val
        new_password: new_password
        MDCard:
            padding: 4
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: None, None
            size: "385dp", "680dp"
            line_color: '#9063CD'
        MDLabel:
            text: 'Password Generator'
            halign: 'center'
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
            font_size: 24
        MDTextField:
            id: new_password
            text: "New Password"
            multiline: True
            size_hint: .9, None
            password: True
            font_size: 19
            pos_hint: {"center_x": 0.5, "center_y": 0.75}
            password: False
            mode: "rectangle"
        MDLabel:
            text: 'Password Length:'
            pos_hint: {"center_x": 0.7, "center_y": 0.6}
            font_size: 20
        MDLabel:
            id: slider_val
            halign: "center"
            pos_hint: {"center_x": 0.75, "center_y": 0.6}
            value: 4
            font_size: 20
            text: str(int(slider.value))
        MDSlider:
            id: slider
            color: '#9063CD'
            size_hint: .9, .02
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            hint: True
            hint_bg_color: '#9063CD'
            hint_radius: [6, 0, 6, 0]
            hint_text_color: "white"
            thumb_color_inactive: "white"
            min: 4
            max: 40
            value: 4
            on_value: root.slider_value(*args)
        MDRaisedButton:
            icon: "content-copy"
            text: "Copy"
            size_hint: .9, None
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            font_size: "16sp"
            on_press: root.copy()
        MDRaisedButton:
            icon: "creation"
            text: "Generate Password"
            size_hint: .9, None
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            font_size: "16sp"
            on_press: root.press_to_generate()
        FloatLayout:
            MDLabel:
                text: 'Letters (e.g. Aa)'
                pos_hint: {"center_x": 0.75, "center_y": 0.225}
            Check:
                id: check1
                pos_hint: {"center_x": 0.15, "center_y": 0.225}
                active: True
                on_active: root.on_checkbox_active(*args)
            MDLabel:
                text: 'Digits (e.g. 345)'
                pos_hint: {"center_x": 0.75, "center_y": 0.14}
            Check:
                id: check2
                pos_hint: {"center_x": 0.15, "center_y": 0.14}
                active: True
                on_active: root.on_checkbox_active(*args)
            MDLabel:
                text: 'Symbols (@&$!#?)'
                pos_hint: {"center_x": 0.75, "center_y": 0.055}
            Check:
                id: check3
                pos_hint: {"center_x": 0.15, "center_y": 0.055}
                active: True
                on_active: root.on_checkbox_active(*args)

<Check@MDCheckbox>:
    size_hint: None, None
    width: dp(28) 
    height: dp(28)             
                  
"""


class Generator(Screen):
    new_password = ObjectProperty(None)
    slider_val = ObjectProperty(None)
    container = ObjectProperty(None)
    length = NumericProperty(0)
    passwd = ObjectProperty(None)

    # use def on_kv_post in place of __init__ to load ids before initialization

    def press_to_generate(self):
        """create a press function to generate password."""
        try:
            pw = self.secret_password()
            self.ids.new_password.text = pw
        except AttributeError as e:
            print(e)

    def copy(self):
        """copy to clipboard"""
        Clipboard.copy(self.ids.new_password.text)

    def slider_value(self, *args):
        """fetch value from slider, return 2nd index of object as integer."""
        self.ids.slider_val.value = str(int(args[1]))

    def secret_password(self):
        """Generate a random password based on checked options."""
        self.length = self.ids.slider_val.value
        if self.ids.check1.active and self.ids.check2.active and self.ids.check3.active:
            alphabet = string.ascii_letters + string.digits + string.punctuation
            self.passwd = self.gen_pw(alphabet)
        if self.ids.check1.active:
            alphabet = string.ascii_letters
            self.passwd = self.gen_pw(alphabet)
        if self.ids.check2.active:
            alphabet = string.digits
            self.passwd = self.gen_pw(alphabet)
        if self.ids.check3.active:
            alphabet = string.punctuation
            self.passwd = self.gen_pw(alphabet)
        if self.ids.check1.active and self.ids.check2.active:
            alphabet = string.ascii_letters + string.digits
            self.passwd = self.gen_pw(alphabet)
        if self.ids.check1.active and self.ids.check3.active:
            alphabet = string.ascii_letters + string.punctuation
            self.passwd = self.gen_pw(alphabet)
        if self.ids.check2.active and self.ids.check3.active:
            alphabet = string.digits + string.punctuation
            self.passwd = self.gen_pw(alphabet)
        elif not self.ids.check1.active and not self.ids.check2.active and not self.ids.check3.active:
            toast("Please select an option", background=[1, 0, 0, 1])  # set toast popup to red(RGB format)
        return self.passwd

    def gen_pw(self, alphabet) -> object:
        password = []
        for i in range(int(self.length)):
            password += secrets.choice(alphabet)
        pw = "".join(password)
        return pw

    @staticmethod
    def on_checkbox_active(checkbox, value):
        """Method for testing state of the checkboxes, for debugging purposes only."""
        if value:
            print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')


class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        return Builder.load_string(kv)


MainApp().run()
