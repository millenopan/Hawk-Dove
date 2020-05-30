from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.logger import Logger

import random, statistics as stat, copy
import main


'''
    GUI.PY - Built using Kivy. First GUI I have ever made, so this is a very
    simple basic GUI that just has a few buttons and labels. I implemented this
    so that in the future I may come back to add in ways in which it becomes easier
    to experiment and adjust values of my simulations.
    Documentation for various tools of Kivy were very difficult to find online: It
    took a lot of time scavenging through links and Stack Exchange to figure out how
    to even make all this.

'''


Window.clearcolor = (0.25, 0.7, 0.85, 0.75)


class MenuScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text='DOVES AND HAWKS',font_size='30sp', color = [1, 1, 1, 1]))
        self.add_widget(Label())

        btn1 = Button(text='Simulate (500 Times)', background_color = [1, 1, 1, 0.75])
        self.add_widget(btn1)
        label1 = Label(text = '')
        self.add_widget(label1)

        exitbtn = Button(text='Exit', background_color = [1, 1, 1, 0.75])
        exitbtn.bind(on_release = Window.close)
        self.add_widget(exitbtn)
        label2 = Label(text = '')
        self.add_widget(label2)



        def callback(instance): ##stolen from my test.py script
            raw = [main.start() for _ in range(500)]
            day_results, winners = [], []
            for result in raw:
                day_results += [result[0]]
                winners += [result[1]]

            day_results = list(filter(lambda x: x < 100, day_results))
            day_results.sort()

            doves = len(list(filter(lambda x: x == 'Dove', winners)))
            hawks = len(list(filter(lambda x: x == 'Hawk', winners)))
            ##mutants = len(list(filter(lambda x: x == 'Mutant', winners)))
            humans = len(list(filter(lambda x: x == 'Human', winners)))
            mean = stat.mean(day_results)
            median = stat.median(day_results)
            popsd = stat.pstdev(day_results)


            label1.text = ('Days Ended: ' + str(len(day_results)) + '\n' +
                           'Doves Won: ' + str(doves) + '\n' +
                           'Hawks Won: ' + str(hawks) + '\n' +
                           ##'Mutants Won: ' + str(mutants) + '\n' +
                           'Humans Won: ' + str(humans))
            label2.text = ("Mean: " + str(mean) + '\n' +
                           "Median: " + str(median) + '\n' +
                           "SD: " + str(popsd) + '\n')

        btn1.bind(on_press=callback)



class MainApp(App):
    def build(self):
        return MenuScreen()
if __name__ == "__main__":
    MainApp().run()
