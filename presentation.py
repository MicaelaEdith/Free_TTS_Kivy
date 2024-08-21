from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from functions import TTS_Kivy
from kivy.uix.switch import Switch
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

LabelBase.register(name='MyFont', fn_regular='assets/NotoSans-VariableFont_wdthwght.ttf')

class MyGridLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [0, 0, 0, 0]
        self.spacing = 18
        self.theme = True
        self.tts = TTS_Kivy()
        self.selection_l = ('all', 'en', 'es')

        Window.borderless = False
        self.update_colors()

        # Action Bar
        action_bar = ActionBar(size_hint_y=None, height=45, padding=[0, 0, 0, 0])
        action_view = ActionView()

        action_previous = ActionPrevious(title='', with_previous=False)
        action_previous.icon = None
        action_view.add_widget(action_previous)

        theme_dropdown = DropDown()
        light_button = Button(text='Light', size_hint_y=None, height=44)
        light_button.bind(on_release=lambda btn: self.set_theme(True))
        dark_button = Button(text='Dark', size_hint_y=None, height=44)
        dark_button.bind(on_release=lambda btn: self.set_theme(False))
        theme_dropdown.add_widget(light_button)
        theme_dropdown.add_widget(dark_button)

        theme_button = ActionButton(text='Theme')
        theme_button.bind(on_release=theme_dropdown.open)
        action_view.add_widget(theme_button)

        language_dropdown = DropDown()
        english_button = Button(text='English', size_hint_y=None, height=44)
        english_button.bind(on_release=lambda btn: self.on_language_select(self.spinner_l, 'En'))
        spanish_button = Button(text='Español', size_hint_y=None, height=44)
        spanish_button.bind(on_release=lambda btn: self.on_language_select(self.spinner_l, 'Es'))
        language_dropdown.add_widget(english_button)
        language_dropdown.add_widget(spanish_button)

        language_button = ActionButton(text='Language')
        language_button.bind(on_release=language_dropdown.open)
        action_view.add_widget(language_button)

        action_bar.add_widget(action_view)
        self.add_widget(action_bar)

        Window.clearcolor = self.window_background_color

        row1 = BoxLayout(orientation='horizontal', spacing=30, size_hint_y=None, height=50, padding = [18, 0, 0, 0])

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

        row2 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50,  padding = [18, 4, 0, 18])
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