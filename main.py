from kivy.app					import App
from kivy.uix.button			import Button
from kivy.uix.boxlayout 		import BoxLayout
from kivy.uix.gridlayout		import GridLayout
from kivy.uix.textinput			import TextInput
from kivy.uix.screenmanager		import Screen, ScreenManager, SlideTransition
from kivy.uix.label				import Label
from kivy.uix.recycleview		import RecycleView
from kivy.metrics				import dp
from kivy.core.window			import Window
from kivy.lang                  import Builder
from kivy.properties            import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors         import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup             import Popup
import sqlite3
import os
#Библиотека
dir_path = os.path.dirname(os.path.realpath(__file__))
#Узнаем в какой папке мы находимся
cnct = sqlite3.connect(dir_path + '/nutrition.db')
crs = cnct.cursor()
#Создаем соединение
class MyDB:
    def create_table(self): #Создаем таблицу
        crs = cnct.execute("CREATE TABLE IF NOT EXISTS 'nutrition' (login text, password text, name text, furname text, email text, money int DEFAULT 0)")
    def insert_into(self, login, passw, name, furname, email): #Делаем ввод
        crs.execute("INSERT INTO nutrition(login, password, name, furname, email, money) VALUES (?,?,?,?,?,0)", (login, passw, name, furname, email))
        cnct.commit()       
    def chech_user(self, login, passw, name, furname, email): #Проверка юзера
        crs.execute("SELECT count(*) FROM nutrition WHERE login = ?", (login,))
        data = crs.fetchone()
        return data
    def select_all(self): #выборка всего 
        crs.execute("SELECT * FROM nutrition")
        return crs.fetchall()
    def login_user(self, login, passw):#проверка на логин и пароль
        crs.execute("SELECT count(*) FROM nutrition WHERE login = ? and password = ?", (login, passw))
        cunt = crs.fetchone()
        return cunt
    def name_login(self, login): #выборка исени и фамилии
        crs.execute("SELECT name, furname FROM nutrition WHERE login = ?", (login,))
        return crs.fetchall()
    def del_user(self, login, passw):#удаление юзера 
        crs.execute("DELETE FROM nutrition WHERE login = ? and password = ?", (login, passw))
        cnct.commit()   
    def del_table(self):#удаление таблицы
        crs.execute("DROP TABLE 'nutrition'")
    def __del__(self):
        cnct.close()

db = MyDB()#Присваивание  класса MyBd к db
db.create_table()
#Создание бд
class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    pass
#отобрадение пользователей
class SelectableButton(RecycleDataViewBehavior, Button):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(False)
#отобрадение пользователей как кнопки
class Menu(Screen):
    db = MyDB()

class Reg(Screen):#регистрация с проверкой условий
    db = MyDB()
    def do_reg(self, login, passw, name, furname, email):
        try:
            conn = db.chech_user(login, passw, name, furname, email)
            if len(login) >= 8:
                if len(passw) >= 8:
                    if conn == (0,):
                        db.insert_into(login, passw, name, furname, email)
                        nick = db.name_login(login)
                        for i in nick:
                            self.popup = Popup(title='Привет', content=Label(text='Пользователь добавлен: ' + i[0] + " " + i[1] + "!"), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
                            self.popup.open()
                    else:
                        self.popup = Popup(title='Ошибка', content=Label(text='Польльзователь с таким логином зарегистрирован'), auto_dismiss=True,size_hint=(None, None), size=(450, 100))
                        self.popup.open()
                else:
                    self.popup = Popup(title='Ошибка', content=Label(text='Пароль должен быть не менее 8 символов'), auto_dismiss=True,size_hint=(None, None), size=(400, 100))
                    self.popup.open()    
            else:
                self.popup = Popup(title='Ошибка', content=Label(text='Логин должен быть не менее 8 символов'), auto_dismiss=True,size_hint=(None, None), size=(400, 100))
                self.popup.open()
        except:
            self.popup = Popup(title='Ошибка', content=Label(text='База данных отсутствует!'), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
            self.popup.open()
#отображение окна входа
class Login(Screen):
    db = MyDB()
    def do_login(self, login, passw):
        try:
            conn = db.login_user(login, passw)
            if conn == (1,):
                nick = db.name_login(login)
                for i in nick:
                    self.popup = Popup(title='Привет', content=Label(text='Привет, ' + i[0] + " " + i[1] + "!"), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
                    self.popup.open()
            else:
                self.popup = Popup(title='Ошибка', content=Label(text='Неверный логин или пароль'), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
                self.popup.open()
        except:
            self.popup = Popup(title='Ошибка', content=Label(text='База данных отсутствует!'), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
            self.popup.open()
# Отоброжение окна с пользователями
class Users(Screen):
    db = MyDB()
    try:
        data_items = ListProperty([])
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if db.select_all() != []:
                self.get_users()
            else:
                self.label = Label(text="Пользователи отсутсвуют")
                self.add_widget(self.label)

        def get_users(self):
            for row in db.select_all():
                self.data_items.append(row[0])
                self.data_items.append(row[2])
                self.data_items.append(row[3])
                self.data_items.append(row[4])
                self.data_items.append(row[5])
    except:
        self.popup = Popup(title='Ошибка', content=Label(text='База данных отсутствует!'), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
        self.popup.open()
        
    def del_db(self):
        try:
            db.del_table()
            self.popup = Popup(title='Успешно', content=Label(text='База данных удалена!'), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
            self.popup.open()
        except:
            self.popup = Popup(title='Ошибка', content=Label(text='База данных отсутствует!'), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
            self.popup.open()
#удаление пользователей
class DelUser(Screen):
    db = MyDB()

    def del_user(self, login, passw):
        try:
            conn = db.login_user(login, passw)
            if conn == (1,):
                db.del_user(login, passw)
                self.popup = Popup(title='Успешно', content=Label(text='Пользователь удален'), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
                self.popup.open()
            else:
                self.popup = Popup(title='Ошибка', content=Label(text='Неверный логин или пароль'), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
                self.popup.open()
        except:
            self.popup = Popup(title='Ошибка', content=Label(text='База данных отсутствует!'), auto_dismiss=True,size_hint=(None, None), size=(300, 100))
            self.popup.open()

#помощь в переходе между экранами
class ScreenManager(ScreenManager):
    pass

with open(dir_path + "/main.kv", encoding='utf8') as f: #кодировка 
    buildKV = Builder.load_string(f.read())

class workDB(App):#запуск программы
    def build(self):
        return buildKV

if __name__ == "__main__":
    workDB().run()
