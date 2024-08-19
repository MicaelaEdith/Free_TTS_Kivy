from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from functions import TTS_Kivy

LabelBase.register(name='MyFont', fn_regular='assets/KodeMono-VariableFont_wght.ttf')

class MyGridLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 80, 0, 10]
        self.spacing = 10
        self.theme = True
        self.tss = TTS_Kivy()
        self.selection_l = ('all','en','es')

        Window.size = (650, 450)
        Window.minimum_width = 650
        Window.minimum_height = 450
        Window.maximum_width = 650
        Window.maximum_height = 450 
        Window.bind(on_request_close=self.on_request_close)
        Window.allow_stretch = False

        if self.theme:
            window_background_color_hex = '#000000'
            button_color_hex = '#121212'
            spinner_background_color_hex = '#1a1a1a'
            text_color_hex = '#BB86FC'
        else:
            window_background_color_hex = '#ffffff'
            button_color_hex = '#121212'
            spinner_background_color_hex = '#1a1a1a'
            text_color_hex = '#BB86FC'
        
        window_background_color = get_color_from_hex(window_background_color_hex)
        button_color = get_color_from_hex(button_color_hex)
        spinner_background_color = get_color_from_hex(spinner_background_color_hex)
        text_color = get_color_from_hex(text_color_hex)
        
        Window.clearcolor = window_background_color

        row1 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)    

        self.spinner = Spinner(
            text='Select a voice',
            values=list(self.tss.list()),
            size_hint=(None, None),
            size=(250, 50),
            background_color=spinner_background_color,
            color=text_color,
            font_size='18sp',
            font_name='MyFont'
        )
        row1.add_widget(self.spinner)

        self.spinner_l = Spinner(
            text='lan',
            values=('All', 'En', 'Es'),
            size_hint=(None, None),
            size=(90, 50),
            background_color=spinner_background_color,
            color=text_color,
            font_size='18sp',
            font_name='MyFont'
        )
        row1.add_widget(self.spinner_l)

        select_button = Button(
            text='Select',
            size_hint=(None, None),
            size=(97, 50),
            background_color=button_color,
            color=text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        row1.add_widget(select_button)

        self.add_widget(row1)
        theme_switch = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(100, 50), spacing=10)
        theme_toggle = ToggleButton(
            text='Theme',
            size_hint=(None, None),
            size=(80, 50),
            background_color=window_background_color,
            color=text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        theme_toggle.bind(on_press=self.toggle_theme)
        theme_switch.add_widget(theme_toggle)
        row1.add_widget(theme_switch)

        self.text_input = TextInput(
            hint_text='Type here',
            size_hint=(None, None),
            size=(480, 300),
            multiline=True,
            font_size='24sp',
            font_name='MyFont',
            background_color=spinner_background_color,
            foreground_color=text_color,
            
            readonly=False,
            text_validate_unfocus=True
        )

        self.add_widget(self.text_input)

        accept_button = Button(
            text='Accept',
            size_hint=(None, None),
            size=(95, 50), 
            background_color=button_color,
            color=text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont' 
        )
        accept_button.bind(on_press=lambda x: self.tss.execute_action(self.text_input))
        self.add_widget(accept_button)

    def toggle_theme(self, instance):

        self.update_colors()
        self.theme = not self.theme

    def update_colors(self):
        if self.theme:
            window_background_color_hex = '#000000'
            button_color_hex = '#121212'
            spinner_background_color_hex = '#1a1a1a'
            text_color_hex = '#BB86FC'
        else:
            window_background_color_hex = '#ffffff'
            button_color_hex = '#252525'
            spinner_background_color_hex = '#181818'
            text_color_hex = '#BB86FC'
        
        window_background_color = get_color_from_hex(window_background_color_hex)
        button_color = get_color_from_hex(button_color_hex)
        spinner_background_color = get_color_from_hex(spinner_background_color_hex)
        text_color = get_color_from_hex(text_color_hex)
        
        Window.clearcolor = window_background_color
        
        self.spinner.background_color = spinner_background_color
        self.spinner.color = text_color
        self.text_input.background_color = spinner_background_color
        self.text_input.foreground_color = text_color



    def on_request_close(self, *args):
        return False

