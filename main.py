from kivy.app import App
from presentation import MyGridLayout


class MyApp(App):
    def build(self):
        self.title = "TSS.kivy"
        return MyGridLayout()


if __name__ == '__main__':
    MyApp().run()
