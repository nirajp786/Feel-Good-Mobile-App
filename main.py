from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json
import datetime
import glob
from pathlib import Path
import random

Builder.load_file('design.kv')
            
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        
        for i in users:
            if uname == i and pword == users[i]["password"]:
                self.manager.current = "login_screen_success"
            else:
                self.ids.LoginStatus.text = "Wrong username or password"
        
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
            
    def get_quote(self, feeling):
        feeling = feeling.lower()
        available_feelings = glob.glob("quotes/*txt")

        
        available_feelings = [Path(filename).stem for filename in
                                available_feelings]
        print(available_feelings)
        
        if feeling in available_feelings:
            with open(f"quotes/{feeling}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass
        
class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        
        with open("users.json", 'w') as file:
            json.dump(users, file)
 
        self.manager.current = "sign_up_screen_success"
        
class SignUpScreenSuccess(Screen):
    def success(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__ == "__main__":
    MainApp().run()