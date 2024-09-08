from kivy.app import App
from presentation import MyGridLayout
from kivy.config import Config


Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '650')
Config.set('graphics', 'height', '520')
Config.write()

class MyApp(App):
    def build(self):
        self.title = "Free TTS"
        self.icon = 'assets/img/favicon.png'
        return MyGridLayout()


if __name__ == '__main__':
    MyApp().run()
