from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from functions import TTS_Kivy
from kivy.uix.switch import Switch
from kivy.uix.actionbar import ActionBar, ActionView, ActionButton
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget



LabelBase.register(name='MyFont', fn_regular='assets/NotoSans-VariableFont_wdthwght.ttf')

class MyGridLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [0, 0, 0, 0]
        self.spacing = 18
        self.theme = False
        self.tts = TTS_Kivy()
        self.selection_l = ('all', 'en', 'es')
        self.lan_menu = 'en'

        Window.borderless = False
        self.update_colors()

        # Action Bar
        action_bar = BoxLayout(size_hint_y=None, height=45, padding=[18, 0, 0, 0], orientation='horizontal', spacing=10)
        
        action_view = BoxLayout(size_hint=(1, 1), padding=[0, 0, 0, 0], orientation='horizontal', spacing=10)

        theme_dropdown = DropDown()
        self.light_button = Button(
            text='Light',
            size_hint_y=None,
            height=44,
            background_color=self.window_background_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.light_button.bind(on_press=lambda x: self.toggle_theme(True))
        self.dark_button = Button(
            text='Dark',
            size_hint_y=None,
            height=44,
            background_color=self.window_background_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.dark_button.bind(on_press=lambda x: self.toggle_theme(False))
        theme_dropdown.add_widget(self.light_button)
        theme_dropdown.add_widget(self.dark_button)

        self.theme_button = ActionButton(text='Theme', background_color=(0, 0, 0, 0),font_name='MyFont',color=self.text_color)
        self.theme_button.bind(on_release=theme_dropdown.open)
        action_view.add_widget(self.theme_button)

        language_dropdown = DropDown()
        self.english_button = Button(
            text='English',
            size_hint_y=None,
            height=44,
            background_color=self.window_background_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.english_button.bind(on_release=lambda btn: self.update_menu('en'))
        self.spanish_button = Button(
            text='Spanish',
            size_hint_y=None,
            height=44,
            background_color=self.window_background_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.spanish_button.bind(on_release=lambda btn: self.update_menu('es'))
        language_dropdown.add_widget(self.english_button)
        language_dropdown.add_widget(self.spanish_button)

        self.language_button = ActionButton(text='Language', background_color=(0, 0, 0, 0), font_name='MyFont',color=self.text_color)
        self.language_button.bind(on_release=language_dropdown.open)
        action_view.add_widget(self.language_button)

        action_bar.add_widget(action_view)
        self.add_widget(action_bar)

        Window.clearcolor = self.window_background_color

        row1 = BoxLayout(orientation='horizontal', spacing=30, size_hint_y=None, height=50, padding=[18, 0, 0, 0])

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
            values=['All', 'En', 'Es'],
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

        self.select_button = Button(
            text='Select',
            size_hint=(None, None),
            size=(90, 35),
            background_color=self.button_color,
            color=self.text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        row1.add_widget(self.select_button)

        self.add_widget(row1)

        padding_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=300)
        padding_layout.padding = [18, 0, 0, 0]
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
            text_validate_unfocus=True,
        )
        padding_layout.add_widget(self.text_input)
        self.add_widget(padding_layout)

        row2 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50, padding=[18, 4, 0, 18])
        self.download_button = Button(
            text='Download',
            size_hint=(None, None),
            size=(105, 40),
            background_color=self.button_color,
            color=self.text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        self.download_button.bind(on_press=lambda x: self.tts.execute_action(self.text_input))

        row2.add_widget(self.download_button)

        self.accept_button = Button(
            text='Try',
            size_hint=(None, None),
            size=(95, 40),
            background_color=self.button_color,
            color=self.text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        self.accept_button.bind(on_press=self.on_accept_button_press)

        row2.add_widget(self.accept_button)
        self.add_widget(row2)

    def update_colors(self):
        if not self.theme:
            self.action_background_color_hex = '#000001'
            self.window_background_color_hex = '#000000'
            self.button_color_hex = '#121212'
            self.spinner_background_color_hex = '#1a1a1a'
            self.text_color_hex = '#BB86FC'
        else:
            self.action_background_color_hex = '#0ffff0'
            self.window_background_color_hex = '#ffffff'
            self.button_color_hex = '#252525'
            self.spinner_background_color_hex = '#181818'
            self.text_color_hex = '#BB86FC'

        self.window_background_color = get_color_from_hex(self.window_background_color_hex)
        self.button_color = get_color_from_hex(self.button_color_hex)
        self.spinner_background_color = get_color_from_hex(self.spinner_background_color_hex)
        self.text_color = get_color_from_hex(self.text_color_hex)

        Window.clearcolor = self.window_background_color

    def toggle_theme(self, value):
        self.theme = value
        self.update_colors()

    def on_accept_button_press(self, instance):
        self.tts.audio_speaker(self.text_input.text)

    def on_spinner_select(self, spinner, text):
        model_dict = self.tts.classify_and_list_models()
        selected_model_path = model_dict.get(text)
        self.selected_model = selected_model_path
        print(f"Modelo seleccionado: {self.selected_model}")

    def on_language_select(self,spinner, text):
        self.tts.update_model_spinner(text, self.spinner)
        
    def update_menu(self, text):
        if text=='en':
            self.theme_button.text = 'Theme'
            self.language_button.text = 'Language'
            self.accept_button.text = 'Try'
            self.download_button.text = 'Download'
            self.dark_button.text ='Dark'
            self.light_button.text ='Light'   
            self.select_button.text='Select'
            self.spanish_button.text='Spanish'
            self.english_button.text='English'
            self.spinner.text='Select a voice'
            self.spinner_l.text='lan'
            self.spinner_1.values=['All', 'En', 'Es']
            
        else:
            self.theme_button.text = 'Tema'
            self.language_button.text = 'Idioma'
            self.accept_button.text = 'Probar'
            self.download_button.text = 'Descargar'
            self.dark_button.text ='Oscuro'
            self.light_button.text ='Claro'
            self.select_button.text='Seleccion'
            self.spanish_button.text='Español'
            self.english_button.text='Ingles'
            self.spinner.text='Seleccionar voz'
            self.spinner_l.text='len'
            self.spinner_1.values=['Todas', 'In', 'Es']

    def on_request_close(self, *args):
        return False
