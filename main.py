from kivy.lang					import Builder
from kivy.properties			import StringProperty, BooleanProperty
from kivy.uix.boxlayout			import BoxLayout
from kivy.uix.screenmanager 	import Screen
from kivymd.app					import MDApp
from kivymd.theming				import ThemableBehavior
from kivymd.uix.picker			import MDDatePicker, MDTimePicker, MDThemePicker
from kivy.uix.recycleview		import RecycleView
from kivy.properties			import ObjectProperty, StringProperty, ListProperty
from kivy.uix.popup             import Popup
from kivy.uix.label				import Label

import sqlite3
import os

import random
from kivy.app					import App
from kivy.uix.widget			import Widget
from kivy.core.window			import Window
from kivy.clock					import Clock
from kivy.metrics				import dp

dir_path = os.path.dirname(os.path.realpath(__file__))
count = False

Builder.load_string("""
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import Window kivy.core.window.Window
#:import IconLeftWidget kivymd.uix.list.IconLeftWidget
<SnakePart>:
	size: 50, 50
	canvas.before:
		Color:
			rgb: app.rand_m(), app.rand_m(), app.rand_m()
		Rectangle:
			size: self.size
			pos: self.pos
<GameScreen>:
	canvas.before:
		Color:
			rgb: 1, 1, 1
		Rectangle:
			size: self.size
			pos: self.pos
	Widget:
		size: 50, 50
		pos: 200, 200
		id: food
		canvas.before:
			Color:
				rgb: app.rand_m(), app.rand_m(), app.rand_m()
			Rectangle:
				size: self.size
				pos: self.pos
<ItemBackdropFrontLayer@TwoLineAvatarListItem>
	icon: "android"
	IconLeftWidget:
		icon: root.icon
<ItemBackdropBackLayer>
	size_hint_y: None
	height: self.minimum_height
	spacing: "10dp"
	canvas:
		Color:
			rgba:
				root.theme_cls.primary_dark if root.selected_item \
				else root.theme_cls.primary_color
		RoundedRectangle:
			pos: self.pos
			size: self.size
	# MDRaisedButton:
	MDIconButton:
		icon: root.icon
		text: root.text
		theme_text_color: "Custom"
		text_color: 1, 1, 1, .5 if not root.selected_item else 1, 1, 1, 1
	MDLabel:
		text: root.text
		color: 1, 1, 1, .5 if not root.selected_item else 1, 1, 1, 1
		halign: 'center'
<ItemBackdropBackLayerOfSecondScreen@BoxLayout>
	size_hint_y: None
	height: "40dp"
	spacing: "25dp"
	text: ""
	MDCheckbox:
		size_hint: None, None
		size: "30dp", "30dp"
		active: False or self.active
		pos_hint: {"center_y": .5}
		selected_color: 1, 1, 1, 1
	MDLabel:
		text: root.text
		color: 1, 1, 1, .7
<ItemRoundBackdropBackLayerOfSecondScreen@BoxLayout>
	size_hint_y: None
	height: "40dp"
	spacing: "25dp"
	text: ""
	MDCheckbox:
		group: "size"
		size_hint: None, None
		size: "30dp", "30dp"
		pos_hint: {"center_y": .5}
		selected_color: 1, 1, 1, 1
	MDLabel:
		text: root.text
		color: 1, 1, 1, .7
<MyBackdropFrontLayer@ScrollView>
	backdrop: None
	backlayer: None
	GridLayout:
		size_hint_y: None
		height: self.minimum_height
		cols: 1
		padding: "5dp"
		ItemBackdropFrontLayer:
			text: "Авторизация"
			secondary_text: "Логин и пароль учащегося"
			icon: "monitor-star"
			on_press:
				root.backlayer.current = "init screen"
				root.backdrop.open()
		ItemBackdropFrontLayer:
			text: "Информация о ученике"
			secondary_text: "ФИО,Курс,код специальности"
			icon: "arrange-send-backward"
			on_press:
				root.backlayer.current = "input data screen"
				root.backdrop.open()
		ItemBackdropFrontLayer:
			text: "Игра"
			secondary_text: "Не хотите ли расслабиться?"
			on_press:
				root.backlayer.current = "game screen"
				root.backdrop.open(-Window.height * 0.9)
		ItemBackdropFrontLayer:
			text: "Показать учеников"
			secondary_text: "Показать информацию об учениках"
			icon: "transfer-down"
			on_press:
				root.backlayer.current = "sql screen"
				root.backdrop.open()
<InputLoginScreen>:
    id: "init"
    login_data: login.text
    passw_data: passw.text
    ScrollView
        GridLayout:
            size_hint_y: None
            height: self.minimum_height
            cols: 1
            padding: "100dp"
            spacing: "30dp"
            MDTextField:
                id: login
                hint_text: "Логин"
                helper_text_mode: "on_focus"
                required: True
                max_text_length: 30
                color_mode: "accent"
            
            MDTextField:
                id: passw
                hint_text: "Пароль"
                helper_text_mode: "on_focus"
                required: True
                max_text_length: 30
                color_mode: "accent"
            FloatLayout:
                MDFloatingActionButton:
                    icon: "check"
                    opposite_colors: True
                    elevation_normal: 8
                    md_bg_color: app.theme_cls.accent_color
                    pos_hint: {'x':.43, 'bottom': .1}
                    on_release: root.clicked_button()
<InputDataScreen>:
	id: "data"
	name: "input data screen"
	name_data: learnt.text
	furname_data: eaten.text
	email_data: email.text
	ScrollView
		GridLayout:
			size_hint_y: None
			height: self.minimum_height
			cols: 1
			padding: "80dp"
			spacing: "30dp"
			MDTextField:
				id:	learnt
				hint_text: "ФИО"
				helper_text_mode: "on_focus"
				helper_text: "ФИО"
				required: True
				max_text_length: 60
				color_mode: "accent"
			MDTextField:
				id: eaten
				hint_text: "Курс"
				helper_text_mode: "on_focus"
				helper_text: "Курс"
				required: True
				max_text_length: 60
				color_mode: "accent"
			MDTextField:
                id: email
                hint_text: "Код специальности"
                helper_text_mode: "on_focus"
                required: True
                color_mode: "accent"
			FloatLayout:
			    MDChip:
                    label: 'Дата рождения'
                    icon: 'face'
                    color: 1, 1, 0, .5
                    selected_chip_color: 1, 1, 0, 1
                    callback: lambda x, y: app.show_date_picker()
                    pos_hint: {'x':.35, 'top':.4}
				MDFloatingActionButton:
					icon: "check"
					opposite_colors: True
					elevation_normal: 8
					md_bg_color: app.theme_cls.accent_color
					pos_hint: {'x':.43, 'bottom': .4}
					on_release: root.clicked_button()
<MyBackdropBackLayer@ScreenManager>
	transition: NoTransition()
    InputLoginScreen:
        name: "init screen"
	InputDataScreen:
	Screen:
		name: "game screen"
		GameScreen
	OutputDataScreen:
		name: "sql screen"
		rv_data: rv.data
		
		RV:
			id: rv
			viewclass: 'ItemBackdropBackLayer'
			RecycleBoxLayout:
				default_size: None, dp(56)
				default_size_hint: 1, None
				size_hint_y: None
				height: self.minimum_height
				orientation: 'vertical'
""")


Builder.load_string("""
<ExampleBackdrop>
	MDBackdrop:
		id: backdrop
		on_open: print("on_open")
		on_close: lambda x: self.ids['backlayer'].InputDataScreen.RV.update_list()
		left_action_items: [["menu", lambda x: self.open()]]
		title: app.title
		header_text: "Меню:"
		MDBackdropBackLayer:
			MyBackdropBackLayer:
				id: backlayer
		MDBackdropFrontLayer:
			MyBackdropFrontLayer:
				backdrop: backdrop
				backlayer: backlayer
""")

class Storage:
    def __init__(self):
        self.cnct = sqlite3.connect(dir_path + '/mydb.db')
        self.crs = self.cnct.cursor()
        self.create_table()
    def create_table(self): #Создаем таблицу
        self.crs = self.cnct.execute("CREATE TABLE IF NOT EXISTS 'mydb' (login text, password text, name text, furname text, email text, bday date)")
    def insert_into(self, login, passw): #Делаем ввод
        self.crs.execute("INSERT INTO mydb(login, password) VALUES (?,?)", (login, passw))
        self.cnct.commit()  
    def insert_into2(self, name, furname, email, bday, login): #Делаем ввод
        self.crs.execute("UPDATE mydb SET name=?, furname=?, email=?, bday=? WHERE login=?", (name, furname, email, bday, login))
        self.cnct.commit()  
    def chech_user(self, login): #Проверка юзера
        self.crs.execute("SELECT count(*) FROM mydb WHERE login = ?", (login,))
        self.data = self.crs.fetchone()
        return self.data
    def select_all(self): #выборка всего 
        self.crs.execute("SELECT * FROM mydb")
        return self.crs.fetchall()
    def login_user(self, login, passw):#проверка на логин и пароль
        self.crs.execute("SELECT count(*) FROM mydb WHERE login = ? and password = ?", (login, passw))
        self.cunt = self.crs.fetchone()
        return self.cunt
    def name_login(self, login): #выборка исени и фамилии
        self.crs.execute("SELECT name, furname FROM mydb WHERE login = ?", (login,))
        return self.crs.fetchall()
    def check_info(self, login):
        self.crs.execute("SELECT name, furname, email, bday FROM mydb WHERE login = ?", (login,))
        return self.crs.fetchall()
    def del_user(self, login, passw):#удаление юзера 
        self.crs.execute("DELETE FROM mydb WHERE login = ? and password = ?", (login, passw))
        self.cnct.commit()   
    def del_table(self):#удаление таблицы
        self.crs.execute("DROP TABLE 'mydb'")
    def __del__(self):
        self.cnct.close()


class RV(RecycleView):
	def __init__(self, **kwargs):
		super(RV, self).__init__(**kwargs)
		self.DB = Storage()
		self.update_list()

	def update_list(self):
		self.data = [{'text': 'ФИО: ' + str(x[2]) + '\nКурс: ' + str(x[3]) + ', Код специальности: ' + str(x[4]) + ', День рождения: ' + str(x[5]), 'icon': 'account'} for x in self.DB.select_all()]


class SnakePart(Widget):
	pass


class GameScreen(Widget):
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.snake_parts = []
		self.step_size = 50
		self.moveX = 0
		self.moveY = 0
		self.new_game()
		Clock.schedule_interval(self.next_frame, .3)

	def new_game(self):
		for _ in range(len(self.snake_parts)):
			self.remove_widget(self.snake_parts.pop())

		self.moveX = 0
		self.moveY = self.step_size
		head = SnakePart()
		head.pos = (0, 0)
		self.snake_parts.append(head)
		self.add_widget(head)

	def on_touch_up(self, touch):
		dx = touch.x - touch.opos[0]
		dy = touch.y - touch.opos[1]
		if abs(dx) > abs(dy):
			self.moveY = 0
			self.moveX = self.step_size if dx > 0 else - self.step_size
		else:
			self.moveX = 0
			self.moveY = self.step_size if dy > 0 else - self.step_size

	def collides_widget(self, wid1, wid2):
		if wid1.right <= wid2.x:
			return False
		if wid1.x >= wid2.right:
			return False
		if wid1.top <= wid2.y:
			return False
		if wid1.y >= wid2.top:
			return False
		return True

	def next_frame(self, *args):
		food = self.ids.food

		new_part = SnakePart()
		new_part.x = self.snake_parts[0].x + self.moveX
		new_part.y = self.snake_parts[0].y + self.moveY

		self.snake_parts.insert(0, new_part)
		self.add_widget(new_part)

		if self.collides_widget(self.snake_parts[0], food):
			food.x = random.randint(0, Window.width - food.width)
			food.y = random.randint(0, Window.height - food.height)
		else:
			self.remove_widget(self.snake_parts.pop())

		for part in self.snake_parts[1:]:
			if self.collides_widget(self.snake_parts[0], part):
				self.new_game()

		if not self.collides_widget(self, self.snake_parts[0]):
			self.new_game()


class ExampleBackdrop(Screen):
	pass


class ItemBackdropBackLayer(ThemableBehavior, BoxLayout):
	icon = StringProperty("android")
	text = StringProperty()
	selected_item = BooleanProperty(False)

	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			for item in self.parent.children:
				if item.selected_item:
					item.selected_item = False
			self.selected_item = True
		return super().on_touch_down(touch)


class InputDataScreen(Screen):
    name_data = StringProperty()
    furname_data = StringProperty()
    email_data = StringProperty()

    def __init__(self, *args, **kwargs):
        super(InputDataScreen, self).__init__(*args, **kwargs)
        self.DB = Storage()

    def clicked_button(self):
        if count == True:
            if len(self.name_data) != 0 or len(self.furname_data) != 0 or len(self.email_data) != 0 or len(datar) != 0:
                self.DB.insert_into2(str(self.name_data), str(self.furname_data), str(self.email_data), str(datar), str(login_userf))
            else:
                self.popup = Popup(title='Ошибка', content=Label(text='Заполните все поля'), size_hint=(None, None), size=(450, 100))
                self.popup.open()
        else:
            self.popup = Popup(title='Ошибка', content=Label(text='Для начала надо войти'), size_hint=(None, None), size=(450, 100))
            self.popup.open()

class InputLoginScreen(Screen):
    login_data = StringProperty()
    passw_data = StringProperty()

    login_userf = str(login_data)

    def __init__(self, *args, **kwargs):
        super(InputLoginScreen, self).__init__(*args, **kwargs)
        self.DB = Storage()

    def clicked_button(self):
        global login_userf, count
        if len(self.login_data) >= 6:
            conn = self.DB.chech_user(self.login_data)
            if len(self.passw_data) >= 6:
                login_userf = str(self.login_data)
                if conn == (0,):
                    self.DB.insert_into(self.login_data, self.passw_data)
                    count = True
                elif conn == (1,):
                    comm = self.DB.login_user(self.login_data, self.passw_data)
                    if comm == (1,):
                        count = True
                        for info in self.DB.check_info(self.login_data):
                            if info[0] != None:
                                self.popup = Popup(title='Привет', content=Label(text='Добро пожаловать, ' + info[0]), size_hint=(None, None), size=(450, 100))
                                self.popup.open()
                            elif info[0] == None and info[1] == None and info[1] == None and info[1] == None:
                                self.popup = Popup(title='Привет', content=Label(text='Добро пожаловать, заполините данные'), size_hint=(None, None), size=(450, 100))
                                self.popup.open()
                            else:
                                self.popup = Popup(title='Привет', content=Label(text='Добро пожаловать'), size_hint=(None, None), size=(450, 100))
                                self.popup.open()
                    else:
                        self.popup = Popup(title='Ошибка', content=Label(text='Неверный пароль'), size_hint=(None, None), size=(450, 100))
                        self.popup.open()
            else:
                self.popup = Popup(title='Ошибка', content=Label(text='Пароль должен быть не менее 8 символов'), size_hint=(None, None), size=(450, 100))
                self.popup.open()
        else:
            self.popup = Popup(title='Ошибка', content=Label(text='Логин должен быть не менее 8 символов'), size_hint=(None, None), size=(450, 100))
            self.popup.open()
		

class OutputDataScreen(Screen):
	rv_data = ListProperty()

	def __init__(self, *args, **kwargs):
		super(OutputDataScreen, self).__init__(*args, **kwargs)
		self.DB = Storage()


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "workDB"
        # self.theme_cls.primary_palette = "Amber"
        self.theme_cls.primary_palette = "Indigo"
        super().__init__(**kwargs)

    def callback(self, instance):
        print(instance)

    def rand_m(self):
        return random.random()

    def show_date_picker(self):
        picker = MDDatePicker(callback=self.got_date)
        picker.open()

    def got_date(self, date):
        global datar
        datar = date
        print(datar)

    def show_time(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        print(time)

    def show_themepicker(self):
        MDThemePicker().open()

    def build(self):
        # self.theme_cls.primary_palette = 'Green'
        self.theme_cls.accent_palette = 'Yellow'
        # ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        self.theme_cls.theme_style = 'Dark'
        self.root = ExampleBackdrop()


if __name__ == "__main__":
	MainApp().run()

# create = Storage()
# print(*[str(x[0]) + str(x[1]) for x in create.select_all()], sep='\n')
# for i in range(1, 18):
# 	create.insert_into('string_name_dish' + str(i), 'init')

# create.del_table()