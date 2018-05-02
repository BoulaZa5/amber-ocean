import amber
import personal_docks
import seas
import ships
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty,NumericProperty
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.screenmanager import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import *
from kivy.uix.popup import *
from kivy.clock import *
from amber import *

Builder.load_file("frontend.kv")

user_id_for_login = ""
        
returned_id=""
###################  Login 
class LoginScreen(BoxLayout):
  # define the constructor and access the class method and attributes
  def __init__(self, users_manager, **kwargs):
    super(LoginScreen, self).__init__(**kwargs)
    #**kwargs allow you to pass a variable number of arguments to a function.
    self.users_manager = users_manager
    # BaxLayout Orientation is vertical
    self.orientation = 'vertical'

class Login(Widget):
  def submit_login(self):
    global user_id_for_login
    # save textinput to a variables
    logname = self.login_name.text
    logpass= self.login_password.text
    # test only
    #if logname == 'admin' and logpass == 'admin':
    #users_manager.current = 'home'
    for key, value in database.items():
        if value.master_email == logname:
            if value.check_password(logpass):
                    user_id_for_login = key
                    users_manager.current = 'home'
            else :
                popup = Popup(title='Test popup',
                content=Label(text='Wrong username or password'),
                size_hint=(None, None), size=self.size)
                popup.open()

###################  Registeration
class Registeration(Widget):
     gender = StringProperty(None)
     date = StringProperty(None)
     def ismale(self):
        gender = "male"# print (gender)
     def isfemale(self):
        gender = "female" # print (gender)

     def registerAccount(self):
          flag=0;
       # check input data
          if self.name.text == "":
            l=Label(text='Please enter Your Name',color=(1,0,0,1),markup=True)
            self.ids.error.add_widget(l)
            Clock.schedule_once(lambda dt: self.ids.error.remove_widget(l), 1)
          elif not self.year.text.isdigit() or not self.month.text.isdigit() or not  self.day.text.isdigit():
            l=Label(text='Please enter a valid Birthday',color=(1,0,0,1),markup=True)
            self.ids.error.add_widget(l)
            Clock.schedule_once(lambda dt: self.ids.error.remove_widget(l), 1)
          elif self.year.text.isdigit() and self.month.text.isdigit() and  self.day.text.isdigit():
             if  int(self.day.text) > 31 or int(self.day.text) < 0:
              l=Label(text='Please enter a valid Birth Day',color=(1,0,0,1),markup=True)
              self.ids.error.add_widget(l)
              Clock.schedule_once(lambda dt: self.ids.error.remove_widget(l), 1)
             elif  int(self.month.text) > 12 or int(self.day.text) < 0 :
              l=Label(text='Please enter a valid Birth Month',color=(1,0,0,1),markup=True)
              self.ids.error.add_widget(l)
              Clock.schedule_once(lambda dt: self.ids.error.remove_widget(l), 1)
             elif  int(self.year.text) > 2018 or int(self.year.text) < 1900:
              l=Label(text='Please enter a valid Birth Year',color=(1,0,0,1),markup=True)
              self.ids.error.add_widget(l)
              Clock.schedule_once(lambda dt: self.ids.error.remove_widget(l), 1)
             elif not '@' in self.email.text or self.email.text==""  :
              l=Label(text='Please enter a valid email',color=(1,0,0,1),markup=True)
              self.ids.error.add_widget(l)
              Clock.schedule_once(lambda dt: self.ids.error.remove_widget(l), 1)
             elif self.password.text=="" :
              l=Label(text='Please enter your Password',color=(1,0,0,1),markup=True)
              self.ids.error.add_widget(l)
              Clock.schedule_once(lambda dt: self.ids.error.remove_widget(l), 1)
             else:
              date = datetime.datetime(int(self.year.text), int(self.month.text), int(self.day.text))
        #check valid date
          
          #else:
              #popup = Popup(title='Test popup',
              #content=Label(text='Please enter a valid Birthday'),
              #size_hint=(None, None), size=self.size)
              #popup.open()
        #print(self.password.text+" "+self.email.text+" "+self.phone.text)
        #  if self.name.text == "" or self.gender==""or date==""or self.password.text=="" or self.email.text == "" or self.phone.text== "" :
        #         # label = Label(text='Please Write Your Name',color=(0,0,0,1))
                  #self.ids.error.add_widget(label)
         # else:
              #  returned_id = personal_docks.PersonalDock.RegisterAccount(self.name.text,self.gender,date,self.password.text,
              #                         self.email.text,self.phone.text)
             #   print(returned_id)
          
class RegisterationScreen(Screen):
    pass


###################################                   
class Page(BoxLayout):

  class ContentManager(ScreenManager):
    class BackButton(Button):

      def __init__(self, screen_manager, **kwargs):
        super(Page.ContentManager.BackButton, self).__init__(**kwargs)
        self.screen_manager = screen_manager

      def on_release(self):
        try:
          prev_screen = self.screen_manager.previous()
          current_screen = self.screen_manager.current_screen
          self.screen_manager.transition.direction = 'right'
          self.screen_manager.current = prev_screen
          self.screen_manager.remove_widget(current_screen)
        except:
          pass

    class GroupButton(Button):

      def __init__(self, user_id, group_id, screen_manager, **kwargs):
        super(Page.ContentManager.GroupButton, self).__init__(**kwargs)
        self.user_id = user_id
        self.group_id = group_id
        self.text = amber.database[group_id].name
        self.screen_manager = screen_manager

      def on_release(self):
        new_group_screen = Screen(name=str(self.screen_manager.screens_added_counter))
        new_group_screen.add_widget(Page.GroupPage(user_id=self.user_id, group_id=self.group_id,
                               screen_manager=self.screen_manager))
        self.screen_manager.add_widget(new_group_screen)
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = new_group_screen.name

    class HomeButton(Button):

      def __init__(self, user_id, screen_manager, **kwargs):
        super(Page.ContentManager.HomeButton, self).__init__(**kwargs)
        self.user_id = user_id
        self.screen_manager = screen_manager

      def on_release(self):
        new_home_screen = Screen(name=str(self.screen_manager.screens_added_counter))
        new_home_screen.add_widget(Page.HomePage(user_id=self.user_id, screen_manager=self.screen_manager))
        self.screen_manager.add_widget(new_home_screen)
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = new_home_screen.name

    class ProfileButton(Button):

      def __init__(self, user_id, destination_id, screen_manager, **kwargs):
        super(Page.ContentManager.ProfileButton, self).__init__(**kwargs)
        self.user_id = user_id
        self.text = amber.database[destination_id].name
        self.destination_id = destination_id
        self.screen_manager = screen_manager

      def on_release(self):
        new_profile_screen = Screen(name=str(self.screen_manager.screens_added_counter))
        new_profile_screen.add_widget(Page.ProfilePage(user_id=self.user_id, destination_id=self.destination_id,
                                 screen_manager=self.screen_manager))
        self.screen_manager.add_widget(new_profile_screen)
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = new_profile_screen.name

    def __init__(self, user_id, **kwargs):
      super(Page.ContentManager, self).__init__(**kwargs)
      self.screens_added_counter = 0
      self.user_id = user_id

    def add_widget(self, screen):
      screen.name = str(self.screens_added_counter)
      super(Page.ContentManager, self).add_widget(screen)
      self.screens_added_counter = self.screens_added_counter + 1

    def back_button(self, **kwargs):
      return Page.ContentManager.BackButton(screen_manager=self, **kwargs)

    def group_button(self, **kwargs):
      return Page.ContentManager.GroupButton(user_id=self.user_id, screen_manager=self, **kwargs)

    def home_button(self, **kwargs):
      return Page.ContentManager.HomeButton(user_id=self.user_id, screen_manager=self, **kwargs)

    def post(self, **kwargs):
      return Page.Post(user_id=self.user_id, screen_manager=self, **kwargs)

    def profile_button(self, **kwargs):
      return Page.ContentManager.ProfileButton(user_id=self.user_id, screen_manager=self, **kwargs)

  class GroupPage(BoxLayout):

    class GroupSettings(BoxLayout):

      def save_settings(self, instance):
        if self.group.is_administrator(self.user_id):
          self.group.name = self.name_tb.text
          self.group.active = self.active.active
          if len(self.group.name) == 0:
            self.group.name = 'No Name'
          self.group.description = self.description_tb.text
          for member_id, member_data in self.members_status.items():
            admin, editor, member = member_data
            if (not admin.active) and (not editor.active) and (not member.active):
              if self.group.is_administrator(member_id):
                self.group.remove_administrator(member_id)
              elif self.group.is_editor(member_id):
                self.group.remove_editor(member_id)
              self.group.remove_member(member_id)
              amber.database[member_id].leave_sea(self.group.id)
            elif (admin.active and editor.active) or admin.active:
              if self.group.is_editor(member_id):
                self.group.remove_editor(member_id)
              if not self.group.is_administrator(member_id):
                self.group.add_administrator(member_id)
            elif editor.active:
              if not self.group.is_editor(member_id):
                self.group.add_editor(member_id)
              if self.group.is_administrator(member_id):
                self.group.remove_administrator(member_id)
            else:
              if self.group.is_editor(member_id):
                self.group.remove_editor(member_id)
              if self.group.is_administrator(member_id):
                self.group.remove_administrator(member_id)
          self.group.visibility_privacy = ''.join(self.visibility_btn.text.split()).lower()
          self.group.sailing_privacy = ''.join(self.sailing_btn.text.split()).lower()
          Page.ContentManager.BackButton(screen_manager=self.screen_manager).on_release()

      def __init__(self, user_id, group, screen_manager, **kwargs):
        super(Page.GroupPage.GroupSettings, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5
        self.user_id = user_id
        self.group = group
        self.screen_manager = screen_manager

        name_and_active = BoxLayout(orientation='horizontal', padding=10, spacing=5, size_hint_y=1)
        name_and_active.add_widget(Label(text='Group Name: ', size_hint_x=1))
        self.name_tb = TextInput(text=self.group.name, size_hint_x=2, multiline=False)
        name_and_active.add_widget(self.name_tb)
        name_and_active.add_widget(Label(text='Active Group: ', size_hint_x=1))
        self.active = CheckBox(active=True)
        name_and_active.add_widget(self.active)
        self.add_widget(name_and_active)

        description = BoxLayout(orientation='horizontal', padding=10, spacing=5, size_hint_y=2)
        description.add_widget(Label(text='Description: ', size_hint_x=1))
        self.description_tb = TextInput(text=self.group.description, size_hint_x=4)
        description.add_widget(self.description_tb)
        self.add_widget(description)

        members = BoxLayout(orientation='horizontal', padding=10, spacing=5, size_hint_y=0.5)
        members.add_widget(Label(text='Members'))
        members.add_widget(Label(text='Is Administrator'))
        members.add_widget(Label(text='Is Editor'))
        members.add_widget(Label(text='Is Member'))
        self.add_widget(members)
        scrollable_members = ScrollView(do_scroll_x=False, size_hint_y=5)
        all_members = BoxLayout(size_hint_y=None, height=len(self.group.members) * 35,
                    orientation='vertical', padding=10, spacing=5)
        self.members_status = {}
        for member in self.group.members:
          member_data = BoxLayout(size_hint_y=None, height=30, orientation='horizontal', padding=10, spacing=5)
          self.members_status[member] = (CheckBox(), CheckBox(), CheckBox(active=True))
          if member in self.group.administrators:
            self.members_status[member][0].active = True
          if member in self.group.editors:
            self.members_status[member][1].active = True
          member_data.add_widget(screen_manager.profile_button(destination_id=member))
          member_data.add_widget(self.members_status[member][0])
          member_data.add_widget(self.members_status[member][1])
          member_data.add_widget(self.members_status[member][2])
          all_members.add_widget(member_data)
        scrollable_members.add_widget(all_members)
        self.add_widget(scrollable_members)

        visibility = BoxLayout(orientation='horizontal', padding=10, spacing=5)
        visibility.add_widget(Label(text='Sea Visibility: ', size_hint_x=1))
        visibility_dp = DropDown()
        self.visibility_btn = Button(text='', size_hint_x=4)
        self.visibility_btn.bind(on_release=visibility_dp.open)
        visibility_dp.bind(on_select=lambda instance, x: setattr(self.visibility_btn, 'text', x))
        if self.group.visibility_privacy == "onlymembers":
          self.visibility_btn.text = "Only members"
        else:
          self.visibility_btn.text = "Everyone"
        btn = Button(text='Only members', size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: visibility_dp.select(btn.text))
        visibility_dp.add_widget(btn)
        btn = Button(text='Everyone', size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: visibility_dp.select(btn.text))
        visibility_dp.add_widget(btn)
        visibility.add_widget(self.visibility_btn)
        self.add_widget(visibility)

        sailing = BoxLayout(orientation='horizontal', padding=10, spacing=5)
        sailing.add_widget(Label(text='Sea Sailing Privacy: ', size_hint_x=1))
        sailing_dp = DropDown()
        self.sailing_btn = Button(text='', size_hint_x=4)
        self.sailing_btn.bind(on_release=sailing_dp.open)
        sailing_dp.bind(on_select=lambda instance, x: setattr(self.sailing_btn, 'text', x))
        if self.group.sailing_privacy == "onlyadministrators":
          self.sailing_btn.text = "Only administrators"
        elif self.group.sailing_privacy == "onlyeditors":
          self.sailing_btn.text = "Only editors"
        else:
          self.sailing_btn.text = "Everyone"
        btn = Button(text='Only administrators', size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: sailing_dp.select(btn.text))
        sailing_dp.add_widget(btn)
        btn = Button(text='Only editors', size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: sailing_dp.select(btn.text))
        sailing_dp.add_widget(btn)
        btn = Button(text='Everyone', size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: sailing_dp.select(btn.text))
        sailing_dp.add_widget(btn)
        sailing.add_widget(self.sailing_btn)
        self.add_widget(sailing)

        btn = Button(text='Save Settings')
        btn.bind(on_release=self.save_settings)
        self.add_widget(btn)

    class SettingsButton(Button):

      def __init__(self, user_id, group, screen_manager, **kwargs):
        super(Page.GroupPage.SettingsButton, self).__init__(**kwargs)
        self.text = 'Settings'
        self.user_id = user_id
        self.group = group
        self.screen_manager = screen_manager

      def on_release(self):
        if self.group.is_administrator(self.user_id):
          settings_page = Screen(name='group_settings')
          settings_page.add_widget(Page.GroupPage.GroupSettings(user_id=self.user_id, group=self.group,
                                      screen_manager=self.screen_manager))
          self.screen_manager.add_widget(settings_page)
          self.screen_manager.current = settings_page.name

    class JoinOrLeaveButton(Button):

      def __init__(self, user_id, group, **kwargs):
        super(Page.GroupPage.JoinOrLeaveButton, self).__init__(**kwargs)
        self.user = amber.database[user_id]
        self.group = group
        if group.is_member(user_id):
          self.text = 'Leave'
        else:
          self.text = 'Join'

      def on_release(self):
        if self.group.is_member(self.user.id):
          if self.group.is_administrator(self.user.id):
            self.group.remove_administrator(self.user.id)
          elif self.group.is_editor(self.user.id):
            self.group.remove_editor(self.user.id)
          self.group.remove_member(self.user.id)
          self.user.leave_sea(self.group.id)
        else:
          self.group.add_member(self.user.id)
          self.user.join_sea(self.group.id)

    class TopBar(BoxLayout):

      def __init__(self, user_id, group, screen_manager, **kwargs):
        super(Page.GroupPage.TopBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = 10
        self.spacing = 5
        self.add_widget(Label(text=group.name, size_hint_x=1))
        if group.is_administrator(user_id):
          self.add_widget(Page.GroupPage.SettingsButton(user_id=user_id, group=group, screen_manager=screen_manager,
                                  size_hint_x=3))
        else:
          self.add_widget(Label(size_hint_x=3))
        self.add_widget(Page.GroupPage.JoinOrLeaveButton(user_id=user_id, group=group))

    class GroupUsers(ScrollView):

      def __init__(self, group, screen_manager, **kwargs):
        super(Page.GroupPage.GroupUsers, self).__init__(**kwargs)
        self.do_scroll_x = False
        self.size_hint_x = 0
        self.users = BoxLayout(size_hint_y=None, orientation='vertical', padding=10, spacing=5)
        self.users.bind(minimum_height=self.users.setter('height'))
        for member in group.members:
          self.size_hint_x = 1
          if group.is_administrator(member):
            self.users.add_widget(screen_manager.profile_button(destination_id=member,
                                      background_color=(1, 0, 0, 1), size_hint_y=None))
          elif group.is_editor(member):
            self.users.add_widget(screen_manager.profile_button(destination_id=member,
                                      background_color=(1, 1, 0, 1), size_hint_y=None))
          else:
            self.users.add_widget(screen_manager.profile_button(destination_id=member, size_hint_y=None))
        self.add_widget(self.users)

    class SuggestedUsers(ScrollView):

      def __init__(self, user, screen_manager, **kwargs):
        super(Page.GroupPage.SuggestedUsers, self).__init__(**kwargs)
        self.do_scroll_x = False
        self.size_hint_x = 0
        self.users = BoxLayout(size_hint_y=None, orientation='vertical', padding=10, spacing=5)
        self.users.bind(minimum_height=self.users.setter('height'))
        for user in user.docks_you_may_know():
          self.size_hint_x = 1
          self.users.add_widget(screen_manager.profile_button(destination_id=user, size_hint_y=None))
        self.add_widget(self.users)

    class SuggestedGroups(ScrollView):

      def __init__(self, user, screen_manager, **kwargs):
        super(Page.GroupPage.SuggestedGroups, self).__init__(**kwargs)
        self.do_scroll_x = False
        self.size_hint_x = 0
        self.groups = BoxLayout(size_hint_y=None, orientation='vertical', padding=10, spacing=5)
        self.groups.bind(minimum_height=self.groups.setter('height'))
        for group in user.seas_you_might_join():
          self.size_hint_x = 1
          self.groups.add_widget(screen_manager.group_button(group_id=group, size_hint_y=None))
        self.add_widget(self.groups)

    class GroupPosts(ScrollView):

      def __init__(self, group, screen_manager, **kwargs):
        super(Page.GroupPage.GroupPosts, self).__init__(**kwargs)
        self.do_scroll_x = False
        self.screen_manager = screen_manager
        self.group = group
        self.posts = BoxLayout(size_hint_y=None, orientation='vertical', padding=10, spacing=5)
        self.posts.bind(minimum_height=self.posts.setter('height'))
        # self.posts_generator = group.generate_ships
        for post in group.sailed_ships:
          self.size_hint_x = 1
          self.posts.add_widget(self.screen_manager.post(post_id=post, destination_id=self.group.id))
        self.add_widget(self.posts)

    def __init__(self, user_id, group_id, screen_manager, **kwargs):
      super(Page.GroupPage, self).__init__(**kwargs)
      self.user = amber.database[user_id]
      self.group = amber.database[group_id]
      if (self.group.visibility_privacy == seas.SeaVisibilityPrivacy.Only_Members and user_id in self.group.members) or self.group.visibility_privacy == seas.SeaVisibilityPrivacy.Everyone:
        self.screen_manager = screen_manager
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5
        self.add_widget(Page.GroupPage.TopBar(user_id=user_id, group=self.group, screen_manager=screen_manager))
        grp_page = BoxLayout(orientation='horizontal', padding=10, spacing=5, size_hint_y=7)
        grp_page.add_widget(Page.GroupPage.GroupPosts(group=self.group, screen_manager=screen_manager,
                                size_hint_x=7))
        grp_page.add_widget(Page.GroupPage.GroupUsers(group=self.group, screen_manager=screen_manager))
        grp_page.add_widget(Page.GroupPage.SuggestedUsers(user=self.user, screen_manager=screen_manager))
        grp_page.add_widget(Page.GroupPage.SuggestedGroups(user=self.user, screen_manager=screen_manager))
        self.add_widget(grp_page)
      else:
        self.size_hint = (0, 0)


  class HomePage(BoxLayout):

    def __init__(self, user_id, screen_manager, **kwargs):
      super(Page.HomePage, self).__init__(**kwargs)
      self.user_id = user_id
      self.screen_manager = screen_manager
      user = amber.database[self.user_id]
      ##### Groups
      group_number = len(list(user.seas))
      group_label = Label(text='Groups',color=(0,0,0,1))
      self.ids.groups_l.add_widget(group_label)
      for i in range(group_number):
          button = Button(text="Group " + i[0]
                          ,background_color=(0,0, 1, 0.6)
                          ,size_hint_y= None
			  ,height= 30)
          self.ids.groups.add_widget(button)

      ##### Friends
      friend_number =len(list(user.friends))
      Friends_label = Label(text='Freinds',color=(0,0,0,1),size_hint_y=10)
      self.ids.friends_l.add_widget(Friends_label)
      for i in range(friend_number):
          button = Button(text="Friend " + i[0]
                          ,background_color=(0,1, 0, 0.6)
			  ,height= 30)
          self.ids.friends.add_widget(button)

      ##### Followees
      Followee_number = len(list(user.followees))
      Followess_label = Label(text='Followees',color=(0,0,0,1))
      self.ids.followees.add_widget(Followess_label)
      for i in range(friend_number):
          button = Button(text="Followee " + str(i),background_color=(1,0, 0, 0.6))
          self.ids.followees.add_widget(button)

      ##### Ships
      Ships_number = len(list(user.newsfeed_ships()))
      Ships_label = Label(text='Ships',color=(0,0,0,1))
      self.ids.ships.add_widget(Ships_label)
      for i in range(Ships_number):
          button = Button(text="Ship " + str(i)
                          ,background_color=(0,1, 1, 0.6)
			  ,height= 30)
          self.ids.ships.add_widget(button)
      ##### Suugested Friends
      sugg_friend_number=len(list(user.docks_you_may_know()))
      sugg_friend_label = Label(text='Suggested Friends',color=(0,0,0,1))
      self.ids.sugg_friend.add_widget(sugg_friend_label)
      for i in range(sugg_friend_number):
          button = Button(text="Friend " + i[0]
                          ,background_color=(1,1, 0, 0.6)
			  ,height= 30)
          self.ids.sugg_friend.add_widget(button)
      ##### Suugested Groups
      sugg_groups_number=len(list(user.seas_you_might_join()))
      sugg_group_label = Label(text='Suggested Groups',color=(0,0,0,1))
      self.ids.sugg_group.add_widget(sugg_group_label)
      for i in range(sugg_groups_number):
          button = Button(text="Group " + i[0]
                          ,background_color=(1,0, 1, 0.6)
			  ,height= 30)
          self.ids.sugg_group.add_widget(button)
  class Post(BoxLayout):

    def __init__(self, user_id, post_id, destination_id, screen_manager, **kwargs):
      super(Page.Post, self).__init__(**kwargs)
      self.user_id = user_id
      self.post_id = post_id
      self.destination_id = destination_id
      self.screen_manager = screen_manager
      self.add_widget(Label(text='Post'))

  class ProfilePage(BoxLayout):

    def __init__(self, user_id, destination_id, screen_manager, **kwargs):
      super(Page.ProfilePage, self).__init__(**kwargs)
      self.user_id = user_id
      self.destination_id = destination_id
      self.screen_manager = screen_manager
      self.add_widget(Label(text='Profile'))

  def __init__(self, users_manager, user_id, **kwargs):
    super(Page, self).__init__(**kwargs)
    self.orientation = 'vertical'
    self.padding = 10
    self.spacing = 5
    self.top_bar = BoxLayout(size_hint_y=1, orientation='horizontal', padding=10, spacing=5)
    self.content = Page.ContentManager(size_hint_y=9, user_id=user_id)
    self.content.home_button().on_release()

    self.top_bar.add_widget(self.content.back_button(text="Back"))
    self.top_bar.add_widget(self.content.home_button(text="Home"))
    self.top_bar.add_widget(self.content.profile_button(destination_id=user_id, text=amber.database[user_id].name))
    self.top_bar.add_widget(Page.ContentManager.BackButton(size_hint_x=0.3, screen_manager=users_manager,
                                 text='Logout', background_color=(1.0, 0.0, 0.0, 1.0)))

    self.add_widget(self.top_bar)
    self.add_widget(self.content)

################### Screen Manager ######################
users_manager = ScreenManager(transition=SwapTransition())

login = Screen(name='login')
login.add_widget(LoginScreen(users_manager=users_manager))
users_manager.add_widget(login)

home = Screen(name='home')
users_manager.add_widget(home)

users_manager.add_widget(RegisterationScreen(name='Registeration'))
######################### Main App
class AmberOcean(App):

  """
  Test App
  """

  def __init__(self, user_id, **kwargs):
    super(AmberOcean, self).__init__(**kwargs)
    self.user_id = user_id

  def build(self):
    home.add_widget(Page(users_manager=users_manager, user_id=self.user_id))

    #users_manager.current = users_manager.next()

    return users_manager

  def on_pause(self):
    return True


if __name__ == "__main__":
  import datetime
  boula = personal_docks.PersonalDock.RegisterAccount(name="Boula", gender=personal_docks.Gender.Male,
                            birthday=datetime.datetime(1996, 9, 28),
                            password="123", email='email@yahoo.com',
                            phone_number='01222222222')
  AmberOcean(user_id=boula).run()
