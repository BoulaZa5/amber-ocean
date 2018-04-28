from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivymd.theming import ThemeManager
# from kivymd.navigationdrawer import NavigationDrawer
from navigationdrawer import NavigationDrawer


main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar

BoxLayout:
    orientation: 'vertical'
    Toolbar:
        id: toolbar
        title: 'Welcome'
        background_color: app.theme_cls.primary_dark
        left_action_items: [['menu', lambda x: app.nav_drawer.toggle()]]
        
    Label:

<Navigator>:
    NavigationDrawerIconButton:
        icon: 'face'
        text: 'Kuldeep Singh'
    NavigationDrawerIconButton:
        icon: 'email'
        text: 'kuldeepbb.grewal@gmail.com'
       # on_release: app.root.ids.scr_mngr.current = 'bottomsheet'
    NavigationDrawerIconButton:
        icon: 'accounts-alt'
        text: 'Friends'


'''


class Navigator(NavigationDrawer):
    image_source = StringProperty('images/me.jpg')
    title = StringProperty('Navigation')


class NavigateApp(App):
    theme_cls = ThemeManager()
    nav_drawer = ObjectProperty()

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        self.nav_drawer = Navigator()
       
        return main_widget

NavigateApp().run()