from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from utils.RandomGenerator import Random
from utils.func import *
from pprint import pprint


class GameScreenStart(Screen):
    def start(self):
        self.parent.INFLUENCES['question'] = self.ids.text_input.text
        self.parent.GAME_PROCESS['question'] = self.ids.text_input.text
        self.ids.text_input.text = ''

    def clear(self):
        self.parent.clear_influences()
        self.parent.clear_game_process()


class BaseGameScreen(Screen):
    def __init__(self, round_number, wheel_id, result_mapping, **kwargs):
        super(BaseGameScreen, self).__init__(**kwargs)
        self.round_number = round_number
        self.wheel_id = wheel_id
        self.result_mapping = result_mapping
    ''''''
    def game_step1(self):
        image_object = self.ids[self.wheel_id]
        animate = self.parent.animation_rotate()
        animate.repeat = True
        animate.start(image_object)
        animate.bind(on_complete=self.game_step2)
        self.parent.INFLUENCES['now'] = get_timestamp()
        chaos_time = Random.get_random_number(self.parent.INFLUENCES, range=(1, 12))
        Clock.schedule_once(lambda dt: animate.stop(image_object), (chaos_time * .1))
        self.ids.roll_dice_button.opacity = 0
        self.ids.roll_dice_button.disabled = True
        ''
    def game_step2(self, *args):
        def get_chaos(ra):
            self.parent.INFLUENCES['now'] = get_timestamp()
            return Random.get_random_number(self.parent.INFLUENCES, range=ra)
            ''
        def clear_surface():
            self.ids[self.wheel_id].opacity = 0
            ''
        def show_popup(c):
            result = self.result_mapping[c]
            definition = self.parent.DB.get_table('definitions')[result]

            result_text = f'{result}\n\n{definition}'
            self.ids.next_roll.opacity = 1
            self.parent.INFLUENCES[f'result_{self.round_number}'] = result_text
            self.parent.GAME_PROCESS[f'result_{self.round_number}'] = result
            self.ids.result_label.text += result_text
            #pprint(self.ids.result_label.texture_size)
            ''
        ''''''
        clear_surface()
        chaos_range = len(self.result_mapping)
        chaos = get_chaos((1, chaos_range))
        show_popup(chaos)
    ''''''
    def clear(self):
        self.ids.result_label.text = ''
        self.ids.roll_dice_button.opacity = 1
        self.ids.roll_dice_button.disabled = False
        self.ids.next_roll.opacity = 0
        self.ids[self.wheel_id].opacity = 1
        self.ids[self.wheel_id].angle = 0
        ''


class GameScreenRound1(BaseGameScreen):
    def __init__(self, **kwargs):
        super(GameScreenRound1, self).__init__(round_number=1, wheel_id='image_wheel1', result_mapping={
            1: 'Balance',
            2: 'Desire',
            3: 'Deception',
            4: 'Emotion',
        }, **kwargs)


class GameScreenRound2(BaseGameScreen):
    def __init__(self, **kwargs):
        super(GameScreenRound2, self).__init__(round_number=2, wheel_id='image_wheel2', result_mapping={
            1: "Contemplation - black",
            2: "Contemplation - white",
            3: "Doubt",
            4: "Hope",
            5: "Excess",
            6: "Nourishment",
            7: "Stagnation",
            8: "Promotion",
            9: "Decay",
            10: "Power",
            11: "Chaos",
            12: "Wonderful",
        }, **kwargs)


class GameScreenRound3(BaseGameScreen):
    def __init__(self, **kwargs):
        super(GameScreenRound3, self).__init__(round_number=3, wheel_id='image_wheel3', result_mapping={
            1: "The Best of all Conceivable Places",
            2: "You’re the Boss",
            3: "Mostly Unfulfilled",
            4: "Totally Unrealistic",
            5: "Instinctive Nature",
            6: "Spiritual Quest",
        }, **kwargs)


class GameScreenRound4(BaseGameScreen):
    def __init__(self, **kwargs):
        super(GameScreenRound4, self).__init__(round_number=4, wheel_id='image_wheel4', result_mapping={
            1: "Appearances",
            2: "Anxiety",
            3: "Hypocrisy",
            4: "Attachments",
            5: "Impatience",
            6: "Fear",
            7: "Indecision",
            8: "Judgments",
            9: "Anger",
            10: "Laziness",
            11: "Regret",
            12: "Health",
            }, **kwargs)


class FinalAnswerScreen(Screen):
    def finish_quote(self):
        self.ids.finish.opacity = 0
        self.parent.INFLUENCES['now'] = get_timestamp()
        chaos = Random.get_random_number(self.parent.INFLUENCES, range=(1, 12))
        result_text = self.parent.DB.get_table('mindstoppers')[str(chaos)]

        self.parent.INFLUENCES['final_result'] = result_text
        self.ids.result_label.text += result_text
        self.parent.GAME_PROCESS['final_answer'] = result_text
        row = {get_timestamp(): self.parent.GAME_PROCESS}

        self.parent.DB.add_rows(table='journal', rows=row)
        self.ids.more.opacity = 1

    def clear(self):
        self.ids.result_label.text = ''
        self.ids.finish.opacity = 1
        self.ids.more.opacity = 0


