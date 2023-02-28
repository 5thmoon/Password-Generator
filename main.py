import os, sys
# kivy config, not-resizable
from kivy.config import Config

Config.set('graphics', 'resizable', 0)
# kivymd imports
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy import require

require('2.1.0')
from kivy.resources import resource_add_path
from kivy.core.window import Window

Window.size = (400, 700)

# kivy imports
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen

# python imports
import secrets
import string


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
        toast("Copied", background=get_color_from_hex('#9063CD'))

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


class PasswordGeneratorApp(MDApp):

    def build(self):
        # Window.borderless = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        return Builder.load_file('main.kv')


if __name__ == '__main__':
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        app = PasswordGeneratorApp()
        app.run()
    except Exception as e:
        print(e)
        input("Press enter.")
