import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

import game_logic


def repo_path(*parts):
    return os.path.join(os.path.dirname(__file__), *parts)


class HeroSelectScreen(Screen):
    def on_enter(self):
        self.ids.container.clear_widgets()
        heros = game_logic.load_yaml_dir('heros')
        for name in heros:
            btn = Button(text=name, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn, n=name: self.select_hero(n))
            self.ids.container.add_widget(btn)

    def select_hero(self, name):
        heros = game_logic.load_yaml_dir('heros')
        app = App.get_running_app()
        app.hero = heros[name]
        app.hero['name'] = name
        # initialize runtime fields expected by original game
        app.hero.setdefault('lives_left', 3)
        app.hero.setdefault('gold', 50)
        app.hero.setdefault('level', 1)
        app.hero.setdefault('xp', 0)
        self.manager.current = 'mainmenu'


class MainMenuScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        self.ids.status.clear_widgets()
        hero = app.hero
        if not hero:
            self.ids.status.add_widget(Label(text='No hero selected'))
            return
        for k, v in hero.items():
            self.ids.status.add_widget(Label(text=f"{k}: {v}"))


class MonsterGameApp(App):
    def build(self):
        sm = ScreenManager()
        # lightweight screens defined in kv-like style using ids
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.gridlayout import GridLayout

        select = HeroSelectScreen(name='select')
        # build child layout with an id container
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Select a hero', size_hint_y=None, height=30))
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        scroll.add_widget(grid)
        # attach as attribute so on_enter can access
        select.ids = {'container': grid}
        select.add_widget(layout)
        layout.add_widget(scroll)

        main = MainMenuScreen(name='mainmenu')
        mlayout = BoxLayout(orientation='vertical')
        status_box = BoxLayout(orientation='vertical')
        main.ids = {'status': status_box}
        mlayout.add_widget(Label(text='Main Menu', size_hint_y=None, height=30))
        mlayout.add_widget(status_box)
        btn_box = BoxLayout(size_hint_y=None, height=40)
        btn_box.add_widget(Button(text='Shop'))
        btn_box.add_widget(Button(text='Fight'))
        btn_box.add_widget(Button(text='Use Item'))
        mlayout.add_widget(btn_box)
        main.add_widget(mlayout)

        sm.add_widget(select)
        sm.add_widget(main)
        # start on hero selection
        sm.current = 'select'
        return sm


if __name__ == '__main__':
    MonsterGameApp().run()
