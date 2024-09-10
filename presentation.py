from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from functions import TTS_Kivy
from kivy.uix.switch import Switch
from kivy.uix.actionbar import ActionBar, ActionView, ActionButton
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.clock import Clock
from csv_functions import *
from app_data import *
from model_downloader import download_one_model

LabelBase.register(name='MyFont', fn_regular='assets/NotoSans-VariableFont_wdthwght.ttf')

class MyGridLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [0, 0, 0, 0]
        self.spacing = 18
        self.tts = TTS_Kivy()
        self.selection_l = ''
        self.config = read_config()
        self.theme = False
        self.lan_menu = 'en'
        self.alert_color = '#FD582F'    #'#DA370F'

        if self.config:
            if self.config[0] == 'True':
                self.theme = True
            else:
                self.theme = False
            self.lan_menu = self.config[1]


        Window.borderless = False
        self.update_colors()

        action_bar = BoxLayout(size_hint_y=None, height=38, padding=[15, 0, 0, 0], orientation='horizontal', spacing=10)
        
        action_view = BoxLayout(size_hint=(1, 1), padding=[0, 0, 0, 0], orientation='horizontal', spacing=10)

        self.theme_dropdown = DropDown()
        self.light_button = Button(
            text='Light',
            size_hint_y=None,
            height=44,
            background_color=self.button_color,
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
            background_color=self.button_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.dark_button.bind(on_press=lambda x: self.toggle_theme(False))
        self.theme_dropdown.add_widget(self.light_button)
        self.theme_dropdown.add_widget(self.dark_button)

        self.theme_button = ActionButton(text='Theme', background_color=self.spinner_background_color,font_name='MyFont',color=self.text_color)
        self.theme_button.bind(on_release=self.theme_dropdown.open)
        action_view.add_widget(self.theme_button)

        self.language_dropdown = DropDown()
        self.english_button = Button(
            text='English',
            size_hint_y=None,
            height=44,
            background_color=self.button_color,
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
            background_color=self.button_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.spanish_button.bind(on_release=lambda btn: self.update_menu('es'))
        self.language_dropdown.add_widget(self.english_button)
        self.language_dropdown.add_widget(self.spanish_button)

        self.language_button = ActionButton(text='Language', background_color=self.spinner_background_color, font_name='MyFont',color=self.text_color)
        self.language_button.bind(on_release=self.language_dropdown.open)
        action_view.add_widget(self.language_button)

        action_bar.add_widget(action_view)
        self.add_widget(action_bar)

        Window.clearcolor = self.window_background_color

        layout_v = BoxLayout(orientation='vertical', padding=[25, 0, 0, 0])

        self.label_voice = Label(
            markup=True,
            text='[b]* Select a voice[/b]',
            font_name='MyFont',
            font_size='14sp',
            color=get_color_from_hex(self.alert_color),
            halign='left',
            opacity=0
        )
        self.label_voice.bind(size=self.label_voice.setter('text_size'))
        layout_v.add_widget(self.label_voice)
        self.add_widget(layout_v)

        row1 = BoxLayout(orientation='horizontal', spacing=30, size_hint_y=None, height=50, padding=[18, 0, 0, 0])

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
        self.tts.update_model_spinner(self.spinner, 'All')

        self.spinner_l = Spinner(
            text='lan',
            values=['All', 'En', 'Sp'],
            size_hint=(None, None),
            size=(70, 35),
            background_color=self.spinner_background_color,
            color=self.text_color,
            font_size='18sp',
            font_name='MyFont'
        )

        self.spinner_l.bind(text=self.on_language_select)

        row1.add_widget(self.spinner_l)

        self.add_widget(row1)

        layout = BoxLayout(orientation='vertical', padding=[25, 0, 0, 5])

        self.label_text = Label(
            markup=True,
            text='[b]* The text field cannot be empty[/b]',
            font_name='MyFont',
            font_size='14sp',
            color=get_color_from_hex(self.alert_color),
            halign='left',
            opacity=0
        )
        self.label_text.bind(size=self.label_text.setter('text_size'))
        layout.add_widget(self.label_text)
        self.add_widget(layout)


        padding_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=300)
        padding_layout.padding = [18, 0, 0, 0]
        self.text_input = TextInput(
            hint_text='Type here',
            size_hint=(None, None),
            size=(500, 300),
            multiline=True,
            font_size='16sp',
            font_name='MyFont',
            background_color=self.window_background_color,
            foreground_color=self.text_color,
            cursor_color=self.text_color, 
            border=(1, 1, 1, 1),
            readonly=False,
            text_validate_unfocus=True,
        )
        padding_layout.add_widget(self.text_input)
        self.add_widget(padding_layout)


        row2 = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=50, padding=[18, 4, 0, 18])
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
        self.download_button.bind(on_press=self.on_download_button_press)

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
        self.update_menu(self.lan_menu)
        self.on_language_select(self.spinner, 'All')

    def update_colors(self):
        if not self.theme:          # dark
            self.action_background_color_hex = '#090909'
            self.window_background_color_hex = '#090909'
            self.button_color_hex = '#323232'
            self.spinner_background_color_hex = '#1a1a1a'
            self.text_color_hex = '#559e53'
            self.cursor_color_hex = '#ffffff' #'#559e53'
            self.selection_color_hex = '#323232'
        else:                       # light
            self.action_background_color_hex = '#0ffff0'
            self.window_background_color_hex = '#f2f5f2'
            self.button_color_hex = '#8d908d'
            self.spinner_background_color_hex = '#8d908d'
            self.text_color_hex = '#559e53'
            self.cursor_color_hex = '#ffffff' #'#559e53'
            self.selection_color_hex = '#8d908d'

        self.window_background_color = get_color_from_hex(self.window_background_color_hex)
        self.button_color = get_color_from_hex(self.button_color_hex)
        self.spinner_background_color = get_color_from_hex(self.spinner_background_color_hex)
        self.text_color = get_color_from_hex(self.text_color_hex)
        self.cursor_color = get_color_from_hex(self.cursor_color_hex)
        self.selection_color = get_color_from_hex(self.selection_color_hex)

        Window.clearcolor = self.window_background_color
              
    def toggle_theme(self, value):
        self.theme = value
        self.update_colors()
        self.apply_colors_to_widgets()
        self.theme_dropdown.dismiss()
        write_config(str(self.theme), self.lan_menu)

    def apply_colors_to_widgets(self):
        self.theme_button.background_color = self.spinner_background_color
        self.theme_button.color = self.text_color
        self.language_button.background_color = self.spinner_background_color
        self.language_button.color = self.text_color

        self.light_button.background_color = self.button_color
        self.light_button.color = self.text_color
        self.dark_button.background_color = self.button_color
        self.dark_button.color = self.text_color

        self.english_button.background_color = self.button_color
        self.english_button.color = self.text_color
        self.spanish_button.background_color = self.button_color
        self.spanish_button.color = self.text_color

        self.spinner.background_color = self.spinner_background_color
        self.spinner.color = self.text_color
        self.spinner_l.background_color = self.spinner_background_color
        self.spinner_l.color = self.text_color

        self.download_button.background_color = self.button_color
        self.download_button.color = self.text_color
        self.accept_button.background_color = self.button_color
        self.accept_button.color = self.text_color

        self.text_input.background_color = self.window_background_color
        self.text_input.foreground_color = self.text_color
        self.text_input.cursor_color = self.text_color 
        self.text_input.selection_color = self.text_color

    def on_download_button_press(self, instance):
        model_dict = self.tts.classify_and_list_models()
        selected_model_path = self.spinner.text
        self.selected_model = selected_model_path
        self.tts.execute_action(self.text_input.text,self.selected_model)


    def on_accept_button_press(self, instance):
        if self.validate():       
            selected_model_path = self.spinner.text
            self.selected_model = selected_model_path
            if not self.tts.audio_speaker(self.text_input.text,self.selected_model):
                self.popup_download()


    def popup_download(self):
        text_title = 'Model not found'
        text_context = 'Download model'
        text_cancel = 'Cancel'

        if self.lan_menu == 'es':
            text_title = 'Modelo no encontrado'
            text_context = 'Descargar Modelo'
            text_cancel = 'Cancelar'

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)

        btn_yes = Button(text=text_context, background_color=self.button_color, color=self.text_color, size_hint=(None, None), size=(150, 50))
        btn_yes.bind(on_press=lambda instance: self.start_download(pop))

        btn_cancel = Button(text=text_cancel, background_color=self.button_color, color=self.text_color, size_hint=(None, None), size=(150, 50))
        btn_cancel.bind(on_press=lambda instance: pop.dismiss())

        button_layout.add_widget(btn_yes)
        button_layout.add_widget(btn_cancel)

        layout.add_widget(button_layout)
        pop = Popup(title=text_title,
                    content=layout,
                    size_hint=(None, None), size=(360, 140),
                    separator_color=self.text_color,
                    auto_dismiss=False)

        pop.open()

    def start_download(self, popup):
        popup.dismiss()
        print('Descargando...')
        self.popup_progress()

    def popup_progress(self):
        text_progress = 'Descargando...'
        text_cancel_download = 'Cancelar descarga'
        text_accept = 'Aceptar'

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)

        self.progress_label = Label(text=text_progress, color=self.text_color)

        self.btn_accept = Button(text=text_accept, background_color=self.button_color, color=self.text_color, size_hint=(None, None), size=(160, 50))
        self.btn_accept.disabled = True
        self.btn_accept.bind(on_press = lambda instance: self.popup_progress.dismiss())

        self.btn_cancel_download = Button(text=text_cancel_download, background_color=self.button_color, color=self.text_color, size_hint=(None, None), size=(160, 50))
        self.btn_cancel_download.bind(on_press=lambda instance: self.popup_progress.dismiss())

        button_layout.add_widget(self.btn_accept)
        button_layout.add_widget(self.btn_cancel_download)
        layout.add_widget(self.progress_label)
        layout.add_widget(button_layout)

        self.popup_progress = Popup(title='Progreso de la descarga',
                                content=layout,
                                size_hint=(None, None), size=(400, 200),
                                separator_color=self.text_color,
                                auto_dismiss=False)

        self.popup_progress.open()

        Clock.schedule_once(self.start_download_process, 0)

    def start_download_process(self, dt):
        download_result = download_one_model(self.spinner.text)

        if download_result:
            self.btn_accept.disabled = False
            self.btn_cancel_download.disabled = True
            self.progress_label.text = "Descarga completada con éxito"
        else:
            self.progress_label.text = "La descarga falló"
        

    def on_spinner_select(self, spinner, text):
        model_dict = self.tts.classify_and_list_models()
        selected_model_path = text
        self.selected_model = selected_model_path

    def on_language_select(self,spinner, text):
        spinner = self.spinner
        self.selection_l = text
        self.spinner.values = self.tts.update_model_spinner(spinner, self.selection_l)
        self.language_dropdown.dismiss()
        
        
    def update_menu(self, text):
        if text=='en':
            self.theme_button.text = 'Theme'
            self.language_button.text = 'Language'
            self.accept_button.text = 'Try'
            self.download_button.text = 'Download'
            self.dark_button.text ='Dark'
            self.light_button.text ='Light'   
            self.spanish_button.text='Spanish'
            self.english_button.text='English'
            self.spinner.text='Select a voice'
            self.text_input.hint_text='Type here'
            self.spinner_l.text='lan'
            self.spinner_l.values=['All', 'En', 'Sp']
            self.lan_menu = 'en'
            self.label_text.text ='[b]* The text field cannot be empty[/b]'
            self.label_voice.text = '[b]* Select a voice[/b]'
            
        else:
            self.theme_button.text = 'Modo'
            self.language_button.text = 'Idioma'
            self.accept_button.text = 'Probar'
            self.download_button.text = 'Descargar'
            self.dark_button.text ='Oscuro'
            self.light_button.text ='Claro'
            self.spanish_button.text='Español'
            self.english_button.text='Ingles'
            self.spinner.text='Seleccionar voz'
            self.text_input.hint_text='Escriba aquí'
            self.spinner_l.text='len'
            self.spinner_l.values=['Todas', 'In', 'Es']
            self.lan_menu = 'es'
            self.label_text.text='[b]* El campo de texto no puede estar vacío[/b]'
            self.label_voice.text = '[b]* Seleccione una voz[/b]'

        self.on_language_select(self.spinner, 'All')
        write_config(str(self.theme), self.lan_menu)

    def validate(self):
        if (self.text_input.text.strip() != '') and (self.spinner.text != 'Seleccionar voz' and self.spinner.text != 'Select a voice'):
            self.label_text.opacity = 0
            self.label_voice.opacity = 0
            return True
        
        if self.text_input.text.strip() == '':
            self.label_text.opacity = 1
            return False
        
        if self.spinner.text == 'Seleccionar voz' or self.spinner.text == 'Select a voice':
            self.label_voice.opacity = 1
            return False
        

    def on_request_close(self, *args):
        return False