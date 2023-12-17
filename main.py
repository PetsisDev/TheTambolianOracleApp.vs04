from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial
from kivy.lang import Builder
from kivy.app import App
from styles import DefaultStyle
from utils.DataBase import DataBase
from game_screens import *
from utils.func import *

from pprint import pprint


LabelBase.register(name="Mystic", fn_regular="fonts/mystical.ttf")
Builder.load_file('kv/buttons.kv')
Builder.load_file('kv/popups.kv')
Builder.load_file('kv/more_popups.kv')
Builder.load_file('kv/headers.kv')
Builder.load_file('kv/screens.kv')
Builder.load_file('kv/images.kv')
Builder.load_file('kv/inputs.kv')


class ColoredRow(BoxLayout):
    def __init__(self, **kwargs):
        super(ColoredRow, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(pos=self.pos, size=self.size, source="images/journal_bg.jpg")
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class JournalScreen(Screen):
    popup = None
    popup_open = False
    def on_enter(self, instance=None, value=None):
        def add_label_and_input(layout, label_width, data_width, label_text, input_text):
            label = Label(
                text=label_text,
                color=(0,0,0, 1),
                size_hint=(label_width, .1),
                font_name="Gabriola",
                font_size=18,
                halign='right'
            )
            data_field = Builder.load_string('Journal_data_field')
            data_field.text = input_text
            data_field.ids = {'name': label_text}
            data_field.on_release = partial(self.open_popup, data_field)
            data_field.size_hint = (data_width, .1)


            #data_field.background_down = data_field.background_normal
            layout.add_widget(label)
            layout.add_widget(data_field)
            ''
        ''''''
        label_width = 0.05
        data_width = 0.2

        journal_layout = self.ids.journal_layout
        journal_layout.clear_widgets()

        rows = self.parent.DB.get_table(table='journal')
        for date, entry in reversed(sorted(rows.items())):
            colored_row = ColoredRow(orientation='horizontal', size_hint_y=None, height=125)
            layout = GridLayout(cols=4, size_hint_y=None, height=125)

            add_label_and_input(layout, label_width, data_width, 'Date:', date)
            add_label_and_input(layout, label_width, data_width, 'Question:', entry['question'])
            add_label_and_input(layout, label_width, data_width, 'Round 1:', str(entry['result_1']))
            add_label_and_input(layout, label_width, data_width, 'Round 2:', str(entry['result_2']))
            add_label_and_input(layout, label_width, data_width, 'Round 3:', str(entry['result_3']))
            add_label_and_input(layout, label_width, data_width, 'Round 4:', str(entry['result_4']))
            add_label_and_input(layout, label_width, data_width, 'Answer:', entry['final_answer'])

            layout.add_widget(Button(size_hint=(label_width, .1), opacity=0, disabled=True))
            layout.add_widget(Button(text='delete', size_hint=(data_width, .1), on_release=partial(self.delete_entry, date)))

            colored_row.add_widget(layout)
            journal_layout.add_widget(colored_row)
        ''
    def open_popup(self, instance):
        def fill_popup():
            definition = self.parent.DB.get_table('definitions')[instance.text]
            self.boxlayout = Builder.load_string('DefinitionPopup')
            self.boxlayout.ids.header_label.text = f"[b]{instance.text}[/b]"
            self.boxlayout.ids.definition_label.text = definition
            self.boxlayout.ids.close_button.bind(on_release=self.close_popup)

            self.add_widget(self.boxlayout)
            self.bind(size=self.on_enter)
            self.popup_open = True
            ''
        def fill_popup_for_answer():
            self.boxlayout = Builder.load_string('DefinitionPopup')
            self.boxlayout.ids.definition_label.text = instance.text
            self.boxlayout.ids.close_button.bind(on_release=self.close_popup)
            self.add_widget(self.boxlayout)
            self.bind(size=self.on_enter)
            self.popup_open = True
            ''
        ''''''
        if self.popup_open == False:
            try:
                if instance.ids['name'] == 'Answer:' or instance.ids['name'] == 'Question:':
                    fill_popup_for_answer()
                elif instance.ids['name'] == 'Date:':
                    pass

                else:
                    fill_popup()

            except KeyError:
                print('error')
        ''
    def close_popup(self, instance):
        try:
            self.remove_widget(self.boxlayout)
            self.popup_open = False
        except:
            pass
    def delete_entry(self, date, button_instance):
        if self.popup_open == False:
            table = 'journal'
            self.parent.DB.delete_row(table=table, row=date)
            self.on_enter()


class WelcomeScreen(Screen):
    pass


class WindowManager(ScreenManager):
    DB = DataBase()
    GAME_PROCESS = dict()
    INFLUENCES = dict()
    INFLUENCES['game_start'] = get_timestamp()
    sound = SoundLoader.load('audio/audio.mp3')
    sound.volume = 1
    #sound.play()

    def clear_influences(self):
        self.INFLUENCES = {
            'game_start': get_timestamp()
        }
        ''
    def clear_game_process(self):
        self.GAME_PROCESS = dict()
    ''''''
    def animation_rotate(self):
        animate = Animation(angle=-360, duration=0.5) + Animation(angle=0, duration=0)
        animate.repeat = True
        return animate
        ''
    def animation_pulse(self):
        animate = Animation(size=(150, 150), duration=.2) + Animation(size=(125, 125), duration=.05)
        animate.repeat = True
        return animate
        ''


class TamboliaApp(App, DefaultStyle):
    def build(self):
        Window.clearcolor = (32 / 255, 67 / 255, 80 / 255, 1)


if __name__ == '__main__':
    TamboliaApp().run()


"""
up next

- style config
- button designs
- kv structure -> all elements in kv files
- scaling sizes
"""