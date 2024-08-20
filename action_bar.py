from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.actionbar import ActionPrevious, ActionButton

class CustomActionBar(BoxLayout):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10

        self.action_previous = ActionPrevious(title='MyApp')
        self.action_previous.with_previous = False
        self.add_widget(self.action_previous)

        action_button = ActionButton(text='Action')
        self.add_widget(action_button)

        self.theme_dropdown = DropDown()
        light_button = Button(text='Light', size_hint_y=None, height=44)
        light_button.bind(on_release=self.set_light_theme)
        dark_button = Button(text='Dark', size_hint_y=None, height=44)
        dark_button.bind(on_release=self.set_dark_theme)
        self.theme_dropdown.add_widget(light_button)
        self.theme_dropdown.add_widget(dark_button)

        theme_button = Button(text='Theme')
        theme_button.bind(on_release=self.theme_dropdown.open)
        self.add_widget(theme_button)

        self.language_dropdown = DropDown()
        english_button = Button(text='English', size_hint_y=None, height=44)
        english_button.bind(on_release=self.set_language_english)
        spanish_button = Button(text='Español', size_hint_y=None, height=44)
        spanish_button.bind(on_release=self.set_language_spanish)
        self.language_dropdown.add_widget(english_button)
        self.language_dropdown.add_widget(spanish_button)

        language_button = Button(text='Language')
        language_button.bind(on_release=self.language_dropdown.open)
        self.add_widget(language_button)

        self.parent = parent

    def set_light_theme(self, instance):
        self.parent.theme = True
        self.parent.update_colors()

    def set_dark_theme(self, instance):
        self.parent.theme = False
        self.parent.update_colors()

    def set_language_english(self, instance):
        self.parent.on_language_select(self.parent.spinner_l, 'En')

    def set_language_spanish(self, instance):
        self.parent.on_language_select(self.parent.spinner_l, 'Es')
