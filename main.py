from kivy.app import App
from presentation import MyGridLayout
from kivy.config import Config


Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '650')
Config.set('graphics', 'height', '500')
Config.write()

class MyApp(App):
    def build(self):
        self.title = "TSS.kivy"
        return MyGridLayout()


if __name__ == '__main__':
    MyApp().run()
