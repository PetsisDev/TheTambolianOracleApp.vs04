from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App

from utils.RandomGenerator import Random
from utils.DataBase import DataBase
from utils.func import *

from pprint import pprint


Builder.load_file('kv/buttons.kv')
Builder.load_file('kv/popups.kv')
Builder.load_file('kv/headers.kv')
Builder.load_file('kv/screens.kv')
Builder.load_file('kv/images.kv')
Builder.load_file('kv/inputs.kv')


class WelcomeScreen(Screen):
    pass


class GameScreenStart(Screen):
    def start(self):
        self.parent.INFLUENCES['question'] = self.ids.text_input.text
        self.parent.GAME_PROCESS['question'] = self.ids.text_input.text
        self.ids.text_input.text = ''

    def clear(self):
        self.parent.clear_influences()
        self.parent.clear_game_process()


class GameScreenRound1(Screen):
    def on_enter(self, *args):
        self.pulse_animation = self.parent.animation_pulse()
        self.pulse_animation.start(self.ids['roll_dice_button'])
        ''
    ''''''
    def game_step1(self):
        def stop_pulse():
            button_object = self.ids['roll_dice_button']
            self.pulse_animation.stop(button_object)
            ''
        def start_rotation():
            image_object = self.ids['image_wheel1']
            animate = self.parent.animation_rotate()
            animate.repeat = True
            animate.start(image_object)
            animate.bind(on_complete=self.game_step2)
            self.parent.INFLUENCES['now'] = get_timestamp()
            chaos_time = Random.get_random_number(self.parent.INFLUENCES, range=(1, 12))
            Clock.schedule_once(lambda dt: animate.stop(image_object), (chaos_time * .1 + 3))
            self.ids.roll_dice_button.opacity = 0
            self.ids.roll_dice_button.disabled = True
        ''''''
        stop_pulse()
        start_rotation()
        ''
    def game_step2(self, *args):
        def get_chaos(ra):
            self.parent.INFLUENCES['now'] = get_timestamp()
            return Random.get_random_number(self.parent.INFLUENCES, range=ra)
            ''
        def clear_surface():
            self.ids.image_wheel1.opacity = 0
            ''
        def show_popup(c):
            result_mapping = {
                1: ('Blue', 'Balance'),
                2: ('Red', 'Desire'),
                3: ('Yellow', 'Deception'),
                4: ('Green', 'Emotion'),
            }

            word = result_mapping[c][1]
            color = result_mapping[c][0]
            definition = self.parent.DB.get_table('definitions')[word]
            result_text = f'- {color} -\n- {word} -\n- {definition.capitalize()} -'

            self.ids.next_roll.opacity = 1
            self.parent.INFLUENCES['result_round_1'] = result_text
            self.parent.GAME_PROCESS['result_1'] = result_text.replace('\n', '')
            self.ids.result_label.text += result_text
        ''''''
        clear_surface()
        chaos = get_chaos((1, 4))
        show_popup(chaos)
        ''
    ''''''
    def clear(self):
        self.ids.result_label.text = ''
        self.ids.roll_dice_button.opacity = 1
        self.ids.roll_dice_button.disabled = False
        self.ids.next_roll.opacity = 0
        self.ids.image_wheel1.opacity = 1
        self.ids.image_wheel1.angle = 0
        ''


class GameScreenRound2(Screen):
    def on_enter(self, *args):
        self.pulse_animation = self.parent.animation_pulse()
        self.pulse_animation.start(self.ids['roll_dice_button'])
        ''
    ''''''
    def game_step1(self):
        def stop_pulse():
            button_object = self.ids['roll_dice_button']
            self.pulse_animation.stop(button_object)
            ''
        def start_rotation():
            image_object = self.ids['image_wheel2']
            animate = self.parent.animation_rotate()
            animate.repeat = True
            animate.start(image_object)
            animate.bind(on_complete=self.game_step2)
            self.parent.INFLUENCES['now'] = get_timestamp()
            chaos_time = Random.get_random_number(self.parent.INFLUENCES, range=(1, 12))
            Clock.schedule_once(lambda dt: animate.stop(image_object), (chaos_time * .1 + 3))
            self.ids.roll_dice_button.opacity = 0
            self.ids.roll_dice_button.disabled = True
        ''''''
        stop_pulse()
        start_rotation()
        ''
    def game_step2(self, *args):
        def get_chaos(ra):
            self.parent.INFLUENCES['now'] = get_timestamp()
            return Random.get_random_number(self.parent.INFLUENCES, range=ra)
            ''
        def clear_surface():
            self.ids.image_wheel2.opacity = 0
            ''
        def show_popup(c):
            result_mapping = {
                1: ("Contemplation", "sometimes you are full and have to remove some ideas, beliefs or confusion in order to accomplish the next task.You are currently thinking about how to do that."),
                2: ("Contemplation", "sometimes you have a project to do but don’t know how to begin.You are currently thinking about how to do that."),
                3: ("Doubt", "doubts are the apprehensive feelings you get when you have new experiences. Making new space or destroying old projects is a new experience."),
                4: ("Hope", "hope is expecting something to happen before it actually happens. Hope is sometimes eternal and actually has to be, sometimes."),
                5: ("Excess", "excess sometimes happens when you don’t make changes fast enough. You are not making changes in your life fast enough."),
                6: ("Nourishment", "nourishment, is what happens when what you expect - happens. Sometimes this happens."),
                7: ("Stagnation", "stagnation means that nothing appears to be happening – not so, you just can’t figure it out or are not noticing. Don’t worry; there are many things that happen to you that you can’t figure out."),
                8: ("Promotion", "promotion is when what you want to happen - is happening, and it is a good idea. Other people have noticed, and you are getting credit for being quite clever."),
                9: ("Decay", "the magic that was in stagnation, has worked, and everything is falling apart, which is a good idea. But this isn’t much fun, and there is a lot more to it than you thought."),
                10: ("Power", "you have built your dream, and everything is in place and working. You are in charge. Now, do something right."),
                11: ("Chaos", "the un-building process is complete, and everything has returned to its original state. You can do anything from here. Sometimes chaos is like fertilizer for new ideas."),
                12: ("Wonderful", "wonderful is as you wanted – almost, unfortunately, by the time you get here, it is time to do something else but stay here as long as you can – if you can.")
            }

            definition = result_mapping[c][1]
            word = result_mapping[c][0]
            result_text = f'- {c} -\n- {word} -\n- {definition.capitalize()} -'

            self.ids.next_roll.opacity = 1
            self.parent.INFLUENCES['result_round_2'] = result_text
            self.parent.GAME_PROCESS['result_2'] = result_text.replace('\n', '')
            self.ids.result_label.text += result_text
        ''''''
        clear_surface()
        chaos = get_chaos((1, 4))
        show_popup(chaos)
        ''
    ''''''
    def clear(self):
        self.ids.result_label.text = ''
        self.ids.roll_dice_button.opacity = 1
        self.ids.roll_dice_button.disabled = False
        self.ids.next_roll.opacity = 0
        self.ids.image_wheel2.opacity = 1
        self.ids.image_wheel2.angle = 0
        ''


class GameScreenRound3(Screen):
    def on_enter(self, *args):
        self.pulse_animation = self.parent.animation_pulse()
        self.pulse_animation.start(self.ids['roll_dice_button'])
        ''
    ''''''
    def game_step1(self):
        def stop_pulse():
            button_object = self.ids['roll_dice_button']
            self.pulse_animation.stop(button_object)
            ''
        def start_rotation():
            image_object = self.ids['image_wheel3']
            animate = self.parent.animation_rotate()
            animate.repeat = True
            animate.start(image_object)
            animate.bind(on_complete=self.game_step2)
            self.parent.INFLUENCES['now'] = get_timestamp()
            chaos_time = Random.get_random_number(self.parent.INFLUENCES, range=(1, 12))
            Clock.schedule_once(lambda dt: animate.stop(image_object), (chaos_time * .1 + 3))
            self.ids.roll_dice_button.opacity = 0
            self.ids.roll_dice_button.disabled = True
        ''''''
        stop_pulse()
        start_rotation()
        ''
    def game_step2(self, *args):
        def get_chaos(ra):
            self.parent.INFLUENCES['now'] = get_timestamp()
            return Random.get_random_number(self.parent.INFLUENCES, range=ra)
            ''
        def clear_surface():
            self.ids.image_wheel3.opacity = 0
            ''
        def show_popup(c):
            result_mapping = {
                1: ("The Best of all Conceivable Places", "This is the best place you can think of. There may be many possible better places. If you have a choice, this is normally a good one."),
                2: ("You are the boss", "This means that you are in control. It also means that if you make a mistake, everyone knows who did it, even you."),
                3: ("Mostly unfulfilled", "You have done everything you can think of, and it does not work, is not right, and you mostly wish you had never started."),
                4: ("Totally unrealistic", "You are being controlled by events that are completely out of your control - and you do not know how to get out."),
                5: ("Instinctive nature", "In order for your instincts to work, you have to disengage your analytical thinking mind. This is quite difficult to do, sometimes even impossible to do. "),
                6: ("Spiritual quest", "When all else fails, this is always an option. Sometimes this is the only option.")
            }

            word = result_mapping[c][0]
            definition = result_mapping[c][1]
            result_text = f'- {c} -\n- {word} -\n- {definition.capitalize()} -'

            self.ids.next_roll.opacity = 1
            self.parent.INFLUENCES['result_round_3'] = result_text
            self.parent.GAME_PROCESS['result_3'] = result_text.replace('\n', '')
            self.ids.result_label.text += result_text
        ''''''
        clear_surface()
        chaos = get_chaos((1, 4))
        show_popup(chaos)
        ''
    ''''''
    def clear(self):
        self.ids.result_label.text = ''
        self.ids.roll_dice_button.opacity = 1
        self.ids.roll_dice_button.disabled = False
        self.ids.next_roll.opacity = 0
        self.ids.image_wheel3.opacity = 1
        self.ids.image_wheel3.angle = 0
        ''


class GameScreenRound4(Screen):
    def on_enter(self, *args):
        self.pulse_animation = self.parent.animation_pulse()
        self.pulse_animation.start(self.ids['roll_dice_button'])
        ''
    ''''''
    def game_step1(self):
        def stop_pulse():
            button_object = self.ids['roll_dice_button']
            self.pulse_animation.stop(button_object)
            ''
        def start_rotation():
            image_object = self.ids['image_wheel4']
            animate = self.parent.animation_rotate()
            animate.repeat = True
            animate.start(image_object)
            animate.bind(on_complete=self.game_step2)
            self.parent.INFLUENCES['now'] = get_timestamp()
            chaos_time = Random.get_random_number(self.parent.INFLUENCES, range=(1, 12))
            Clock.schedule_once(lambda dt: animate.stop(image_object), (chaos_time * .1 + 3))
            self.ids.roll_dice_button.opacity = 0
            self.ids.roll_dice_button.disabled = True
        ''''''
        stop_pulse()
        start_rotation()
        ''
    def game_step2(self, *args):
        def get_chaos(ra):
            self.parent.INFLUENCES['now'] = get_timestamp()
            return Random.get_random_number(self.parent.INFLUENCES, range=ra)
            ''
        def clear_surface():
            self.ids.image_wheel4.opacity = 0
            ''
        def show_popup(c):
            result_mapping = {
                1: ("Appearances", "Appearances are the external view of others and ourselves. It is what we try to tidy up before anyone actually sees us. Remember, appearances are only skin-deep, and stupid goes clear to the bone."),
                2: ("Anxiety", "Anxiety is when you figure out that you haven’t figured it out. Very few people have, so there are many good reasons to be anxious. Being anxious about your anxieties is extra."),
                3: ("Hypocrisy", "Hypocrisy is when you say one thing and think another. Oddly enough, if everyone always told the Truth, we wouldn’t like it. Sometimes it is better not to say anything, which is passive-aggressive hypocrisy."),
                4: ("Attachments", "Attachments keep us connected to what we are doing. Attachments can be anything, and figuring them out is the difficult part. Not being attached to anything is a popular meditation unless you are attached to the meditation, then it is not."),
                5: ("Impatience", "Impatience is being more eager than skillful. Remember, it is not your fault you are perfect."),
                6: ("Fear", "Fear is False Evidence Appearing Real. This is a nice slogan unless it is not true. Then you might actually have something to be worried about."),
                7: ("Indecision", "Indecision is when your mind grinds to a halt. It might be helpful to remember that no decision is worse than a bad decision because you can fix or change a bad decision."),
                8: ("Judgements", "You have been told not to judge other people, which is itself a judgment, so don’t do that, either. "),
                9: ("Anger", "Sometimes, you have to be angry in order to accomplish a task. Sometimes it is the only way. It is important not to let anger actually make the decision."),
                10: ("Laziness", "Laziness is when you don’t want to do something that probably doesn’t need to be done anyway, and it is only a problem when someone notices."),
                11: ("Regret", "Regret is when you decide to do one thing and not something else. Remember the adage that the grass is always greener on the other side of the fence. Unfortunately, almost everything is on the other side of the fence."),
                12: ("Health", "Health can be physical health, emotional health, and the health of others. Sometimes you need to pay attention to these things because if you don’t - who might?")
            }

            word = result_mapping[c][0]
            definition = result_mapping[c][1]
            result_text = f'- {c} -\n- {word} -\n- {definition.capitalize()} -'

            self.ids.next_roll.opacity = 1
            self.parent.INFLUENCES['result_round_4'] = result_text
            self.parent.GAME_PROCESS['result_4'] = result_text.replace('\n', '')
            self.ids.result_label.text += result_text
        ''''''
        clear_surface()
        chaos = get_chaos((1, 4))
        show_popup(chaos)
        ''
    ''''''
    def clear(self):
        self.ids.result_label.text = ''
        self.ids.roll_dice_button.opacity = 1
        self.ids.roll_dice_button.disabled = False
        self.ids.next_roll.opacity = 0
        self.ids.image_wheel4.opacity = 1
        self.ids.image_wheel4.angle = 0
        ''


class FinalAnswerScreen(Screen):
    def finish_quote(self):
        self.ids.finish.opacity = 0
        self.parent.INFLUENCES['now'] = get_timestamp()
        result = Random.get_random_number(self.parent.INFLUENCES, range=(1, 12))

        result_mapping = {
            "1": "Noticing where you are is the hard part",
            "2": "What was the unasked question",
            "3": "The Truth and the childlike quality are in the same place",
            "4": "If you got here from there, you can get there from here",
            "5": "Looking in or looking out, both and neither often matter",
            "6": "Women and children are not the problem",
            "7": "Is hindsight…insight?",
            "8": "Sometimes, you’re out before you get out",
            "9": "We are all alone - together",
            "10": "How much can one lie cost you?",
            "11": "You cannot lie, not even to yourself",
            "12": "Think of something you’re on your own",
            "13": "You came here – you might as well be here",
            "14": "You have a center – someplace",
            "15": "You can’t hide",
            "16": "Just right is enough",
            "17": "Even small miracles remove doubt",
            "18": "That’s about the hardest way to get here, as you can find",
            "19": "If you believe my stuff, I’ll believe your stuff",
            "20": "Don’t worry - be happy",
            "21": "Everyone does the best they can",
            "22": "If I am only for myself, what am I?",
            "23": "If I am not for myself, who will be?",
            "24": "How can you participate and still nurture yourself?",
            "25": "Even the smallest good deed can be resented",
            "26": "Stupidity has no solution",
            "27": "Which side of the Wall are you on?",
            "28": "Vague is the best we can do",
            "29": "Figuring it out is the easy part",
            "30": "Sometimes, knowing the numbers does help",
            "31": "What does an answer look like?",
            "32": "When the obvious becomes obvious",
            "33": "Maybe you should try right behaver",
            "34": "The Truth is not hidden, just deeply unnoticed",
            "35": "If you don’t know, be vague",
            "36": "If it is here, it is not somewhere else",
            "37": "It’s all the Truth",
            "38": "There is always something - somewhere",
            "39": "The Truth catches on - eventually",
            "40": "It is only there if it is there",
            "41": "There is no answer without the question",
            "42": "Truths and falsehoods, both and neither, often matter",
            "43": "It’s all here somewhere",
            "44": "Vague is the best we can do",
            "45": "Figuring it out is the easy part",
            "46": "Relationships – none isn’t enough, and one is too much",
            "47": "Getting in is easy; being in is difficult",
            "48": "Ignorance is not bliss",
            "49": "There is almost no essential thing",
            "50": "We are smarter than you",
            "51": "Why would anyone put anything like this; anywhere?",
            "52": "You may get old but never be old",
            "53": "Life has a little bit of everything but not enough of anything",
            "54": "To the organized mind, death is but the next adventure",
            "55": "After figuring out what is mandatory, what is excluded becomes very interesting.",
            "56": "Deluded people are the problem.",
            "57": "Forgetfulness is what stupid people know.",
            "58": "Coming and going are often the same",
            "59": "Illusions are incomplete truths.",
            "60": "Here was not always where it was expected to be"
        }

        word = result_mapping[str(result)]
        result_text = f'- {word} -'

        self.parent.INFLUENCES['final_result'] = result_text
        self.ids.result_label.text += result_text
        self.parent.GAME_PROCESS['final_answer'] = result_text
        row = {
            get_timestamp(): self.parent.GAME_PROCESS
        }

        self.parent.DB.add_rows(table='journal', rows=row)
        self.ids.more.opacity = 1
        pprint(self.parent.GAME_PROCESS)

    def clear(self):
        self.ids.result_label.text = ''
        self.ids.finish.opacity = 1
        self.ids.more.opacity = 0


class JournalScreen(Screen):
    def on_enter(self):
        rows = self.parent.DB.get_table('journal')
        for row in rows:
            record_label = Label(text=f"date: {row}, Name: {row[1]}, Age: {row[2]}")


class WindowManager(ScreenManager):
    DB = DataBase()
    GAME_PROCESS = dict()
    INFLUENCES = dict()
    INFLUENCES['game_start'] = get_timestamp()

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


class TamboliaApp(App):
    def build(self):
        Window.clearcolor = (32 / 255, 67 / 255, 80 / 255, 1)


if __name__ == '__main__':
    TamboliaApp().run()

















"""



self.update_records()
menu_widget = Builder.load_string('ResultPopup')
self.ids.scroll_area.add_widget(menu_widget)


main_layout = ScrollView()

self.rows = self.query_database()
scroll_view = ScrollView()

# Create a box layout to hold the labels for each record
self.box_layout = self.ids.scroll_area

# Add labels for each record to the box layout
self.update_records()

# Add the box layout to the scroll view
scroll_view.add_widget(self.box_layout)

# Add the scroll view to the main layout
main_layout.add_widget(scroll_view)
self.ids.scroll_area.add_widget(scroll_view)

# Add buttons for CRUD operations
#main_layout.add_widget(Button(text='Add Record', on_press=self.show_add_dialog))
#main_layout.add_widget(Button(text='Edit Record', on_press=self.show_edit_dialog))
#main_layout.add_widget(Button(text='Delete Record', on_press=self.show_delete_dialog))
#main_layout.add_widget(Button(text='Close', on_press=self.stop))

return main_layout"""



"""

    def update_records(self):
        # Clear existing widgets in box_layout
        self.ids.scroll_area.clear_widgets()
        rows = self.parent.DB.get_table('journal')
        # Add labels for each record to the box layout
        for row in rows:
            row_text = f"Date: {row}, "
            popup = Builder.load_string('ResultPopup')
            for key in rows[row].keys():
                value = rows[row][key]
                row_text += f"{key}: {value}\n"

            record_label = Label(text=row_text)
            popup.add_widget(record_label)
            self.ids.scroll_area.add_widget(popup)

    def show_add_dialog(self, instance):
        # Create a pop-up dialog for adding a new record
        add_dialog = BoxLayout(orientation='vertical', spacing=10)
        name_input = TextInput()

        add_dialog.add_widget(Label(text='Name:'))



        add_dialog.add_widget(name_input)
        add_dialog.add_widget(Label(text='Age:'))
        age_input = TextInput(input_type='number')
        add_dialog.add_widget(age_input)

        add_dialog.add_widget(
            Button(text='Add', on_press=lambda instance: self.add_record(name_input.text, age_input.text)))
        add_dialog.add_widget(Button(text='Cancel', on_press=lambda instance: popup.dismiss()))

        popup = Popup(title='Add Record', content=add_dialog, size_hint=(None, None), size=(300, 200))
        popup.open()

    def show_edit_dialog(self, instance):
        # Create a pop-up dialog for editing an existing record
        edit_dialog = BoxLayout(orientation='vertical', spacing=10)
        edit_dialog.add_widget(Label(text='Record ID:'))
        id_input = TextInput(input_type='number')
        edit_dialog.add_widget(id_input)
        edit_dialog.add_widget(Label(text='New Name:'))
        name_input = TextInput()
        edit_dialog.add_widget(name_input)
        edit_dialog.add_widget(Label(text='New Age:'))
        age_input = TextInput(input_type='number')
        edit_dialog.add_widget(age_input)

        edit_dialog.add_widget(Button(text='Edit',
                                      on_press=lambda instance: self.edit_record(id_input.text, name_input.text,
                                                                                 age_input.text)))
        edit_dialog.add_widget(Button(text='Cancel', on_press=lambda instance: popup.dismiss()))

        popup = Popup(title='Edit Record', content=edit_dialog, size_hint=(None, None), size=(300, 200))
        popup.open()

    def show_delete_dialog(self, instance):
        # Create a pop-up dialog for deleting an existing record
        delete_dialog = BoxLayout(orientation='vertical', spacing=10)
        delete_dialog.add_widget(Label(text='Record ID:'))
        id_input = TextInput(input_type='number')
        delete_dialog.add_widget(id_input)

        delete_dialog.add_widget(Button(text='Delete', on_press=lambda instance: self.delete_record(id_input.text)))
        delete_dialog.add_widget(Button(text='Cancel', on_press=lambda instance: popup.dismiss()))

        popup = Popup(title='Delete Record', content=delete_dialog, size_hint=(None, None), size=(300, 150))
        popup.open()

    def add_record(self, name, age):
        # Connect to the SQLite database
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()

        # Insert a new record into the 'users' table
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        connection.commit()

        # Query all data from the 'users' table
        self.rows = self.query_database()

        # Update the displayed records
        self.update_records()

    def edit_record(self, record_id, name, age):
        # Connect to the SQLite database
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()

        # Update an existing record in the 'users' table
        cursor.execute("UPDATE users SET name=?, age=? WHERE id=?", (name, age, record_id))
        connection.commit()

        # Query all data from the 'users' table
        self.rows = self.query_database()

        # Update the displayed records
        self.update_records()

    def delete_record(self, record_id):
        # Connect to the SQLite database
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()

        # Delete an existing record from the 'users' table
        cursor.execute("DELETE FROM users WHERE id=?", (record_id,))
        connection.commit()

        # Query all data from the 'users' table
        self.rows = self.query_database()

        # Update the displayed records
        self.update_records()



"""