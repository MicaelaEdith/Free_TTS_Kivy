from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from functions import TTS_Kivy
from kivy.uix.switch import Switch
from action_bar import CustomActionBar

#from kivy.lang import Builder

#Builder.load_file('style.kv')

LabelBase.register(name='MyFont', fn_regular='assets/KodeMono-VariableFont_wght.ttf')

class MyGridLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 80, 0, 10]
        self.spacing = 10
        self.theme = True
        self.tts = TTS_Kivy()
        self.selection_l = ('all', 'en', 'es')

        # Configure colors based on the theme
        self.update_colors()

        # Initialize the ActionBar
        #self.action_bar = CustomActionBar(self)
        #self.add_widget(self.action_bar)
        Window.clearcolor = self.window_background_color

        row1 = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=50)

        model_dict = self.tts.classify_and_list_models()
        self.spinner = Spinner(
            text='Select a voice',
            values=[],
            size_hint=(None, None),
            size=(220, 35),
            background_color=self.spinner_background_color,
            color=self.text_color,
            font_size='18sp',
            font_name='MyFont'
        )
        self.spinner.bind(text=self.on_spinner_select)
        row1.add_widget(self.spinner)

        self.spinner_l = Spinner(
            text='lan',
            values=('All', 'En', 'Es'),
            size_hint=(None, None),
            size=(70, 35),
            background_color=self.spinner_background_color,
            color=self.text_color,
            font_size='18sp',
            font_name='MyFont'
        )
        self.spinner_l.bind(text=self.on_language_select)
        row1.add_widget(self.spinner_l)

        self.on_language_select(self.spinner_l, 'All')

        select_button = Button(
            text='Select',
            size_hint=(None, None),
            size=(90, 35),
            background_color=self.button_color,
            color=self.text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        row1.add_widget(select_button)

        theme_switch_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(80, 50), spacing=0, padding=[50, 50, 50, 40])

        theme_switch = Switch(
            active=self.theme,
            size_hint=(None, None),
            size=(40, 25),
        )
        theme_switch.bind(active=self.toggle_theme)

        theme_switch_layout.add_widget(theme_switch)
        row1.add_widget(theme_switch_layout)

        self.add_widget(row1)

        self.text_input = TextInput(
            hint_text='Type here',
            size_hint=(None, None),
            size=(480, 300),
            multiline=True,
            font_size='16sp',
            font_name='MyFont',
            background_color=self.spinner_background_color,
            foreground_color=self.text_color,
            readonly=False,
            text_validate_unfocus=True
        )

        self.add_widget(self.text_input)

        row2 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)

        download_button = Button(
            text='Download',
            size_hint=(None, None),
            size=(105, 40),
            background_color=self.button_color,
            color=self.text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        download_button.bind(on_press=lambda x: self.tts.execute_action(self.text_input))

        row2.add_widget(download_button)

        accept_button = Button(
            text='try',
            size_hint=(None, None),
            size=(95, 40),
            background_color=self.button_color,
            color=self.text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        accept_button.bind(on_press=self.on_accept_button_press)

        row2.add_widget(accept_button)
        self.add_widget(row2)

    def update_colors(self):
        if self.theme:
            self.window_background_color_hex = '#000000'
            self.button_color_hex = '#121212'
            self.spinner_background_color_hex = '#1a1a1a'
            self.text_color_hex = '#BB86FC'
        else:
            self.window_background_color_hex = '#ffffff'
            self.button_color_hex = '#252525'
            self.spinner_background_color_hex = '#181818'
            self.text_color_hex = '#BB86FC'

        self.window_background_color = get_color_from_hex(self.window_background_color_hex)
        self.button_color = get_color_from_hex(self.button_color_hex)
        self.spinner_background_color = get_color_from_hex(self.spinner_background_color_hex)
        self.text_color = get_color_from_hex(self.text_color_hex)

        Window.clearcolor = self.window_background_color

    def toggle_theme(self, instance, value):
        self.theme = value
        self.update_colors()

    def on_accept_button_press(self, instance):
        self.tts.audio_speaker(self.text_input.text)

    def on_spinner_select(self, spinner, text):
        model_dict = self.tts.classify_and_list_models()
        selected_model_path = model_dict.get(text)
        self.selected_model = selected_model_path
        print(f"Modelo seleccionado: {self.selected_model}")

    def on_language_select(self, spinner, text):
        self.tts.update_model_spinner(text, self.spinner)
        
    def on_request_close(self, *args):
        return False