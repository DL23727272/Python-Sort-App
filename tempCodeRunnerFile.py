from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
import mysql.connector
from kivy.core.window import Window
Window.size = (368, 640)

KV = """
ScreenManager:
    SplashScreen:
    LoginScreen:
    MainScreen:
    SignUpScreen:

<SplashScreen>:
    name: 'splash'
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'
        size_hint: None, None
        size: dp(368), dp(140)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        Image:
            source: "logo.png"
            size_hint: None, None
            size: dp(180), dp(180)
            pos_hint: {'center_x': 0.5}
        
        MDLabel:
            text: "Welcome to Quick Sort App"
            font_style: 'H5'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]

<MainScreen>:
    name: 'main'
    MDBottomNavigation:
        selected_color_background: "orange"
        text_color_active: "lightgrey"

        MDBottomNavigationItem:
            name: 'inventory'
            text: 'Inventory'
            icon: 'warehouse'
            MDBoxLayout:
                orientation: 'vertical'
                padding: '10dp'
                spacing: '10dp'
                
                MDTextField:
                    id: item_name
                    hint_text: "Item Name"
                MDTextField:
                    id: item_quantity
                    hint_text: "Quantity"
                MDRaisedButton:
                    text: "Add Item"
                    on_press: app.add_item(app.username, item_name.text, item_quantity.text)
                MDTextField:
                    id: update_item_id
                    hint_text: "Item ID to Update"
                MDTextField:
                    id: new_quantity
                    hint_text: "New Quantity"
                MDRaisedButton:
                    text: "Update Item"
                    on_press: app.update_item(app.username, update_item_id.text, new_quantity.text)
                MDTextField:
                    id: delete_item_id
                    hint_text: "Item ID to Delete"
                MDRaisedButton:
                    text: "Delete Item"
                    on_press: app.delete_item(app.username, delete_item_id.text)

        MDBottomNavigationItem:
            name: 'screen2'
            text: 'Items'
            icon: 'note'
            MDBoxLayout:
                orientation: 'vertical'
                padding: '10dp'
                spacing: '10dp'
                
                ScrollView:
                    MDList:
                        id: inventory_content

        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'About'
            icon: 'information'

            MDLabel:
                text: 'INFORMATION ABOUT DEVS'
                halign: "center"
                pos_hint: {"center_x": .5, "center_y": .7}
                bold: True
                
            MDLabel:
                text: 'Meet the Team Behind [b]Marlyn Rose Defiesta[/b] and [b]Casselyn Rapanut[/b].'
                halign: 'center'
                pos_hint: {"center_x": .5, "center_y": .6}
                markup: True
            MDLabel:
                text: "Welcome to Quick Sort App! We're thrilled to have you here and excited to share more about the team that brought this app to life."
                halign: 'center'
                pos_hint: {"center_x": .5, "center_y": .5}

        MDBottomNavigationItem:
            name: 'screen 4'
            text: 'System Info'
            icon: 'application'

            MDLabel:
                text: 'System Info'
                halign: 'center'
                halign: "center"
                pos_hint: {"center_x": .5, "center_y": .7}
                bold: True
            MDLabel:
                text: "[b]Compatibility[/b] - This app is compatible with devices running Android Oreo+ and iOS."
                halign: 'center'
                pos_hint: {"center_x": .5, "center_y": .6}
                markup: True
            MDLabel:
                text: "[b]Storage[/b] - The app will require small to medium storage space for faster and efficient performance on smartphones."
                halign: 'center'
                pos_hint: {"center_x": .5, "center_y": .5}
                markup: True

        MDBottomNavigationItem:
            name: 'screen 5'
            text: 'System Help'
            icon: 'application-braces-outline'

            MDLabel:
                text: 'System Help'
                halign: 'center'
                halign: "center"
                pos_hint: {"center_x": .5, "center_y": .8}
                bold: True
            MDLabel:
                text: "User Interface This app feature a user-friendly interface for users to mamange their inventory through adding, updating, and deleting items easily. Online Access This app require an internet for the users to efficienlty use the features."
                halign: 'center'
                pos_hint: {"center_x": .5, "center_y": .6}
                markup: True
            MDLabel:
                text: "Terms of Service and Privacy Policy By accessing the app terms of Service and Privacy Policy for users to understand their right and responsibility in using the app."
                halign: 'center'
                pos_hint: {"center_x": .5, "center_y": .4}
                markup: True
            MDRaisedButton:
                text: "Logout"
                pos_hint: {"center_x": .5, "center_y": .2}
                on_press: app.logout()

<LoginScreen>:
    name: 'login'
    MDBottomNavigation:
        panel_color: "#EAE8E8"
        selected_color_background: "pink"
        text_color_active: "black"

        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Quick Sort App'
            icon: 'warehouse'

            Image:
                source: "logo.png"
                size_hint: None, None
                width: "80dp"
                height: "80dp"
                pos_hint: {'center_x': .5, 'center_y': .9}
            MDLabel:
                text: "Log in"
                source: "logo.png"
                color: "#484747"
                bold: True
                font_size: "48dp"
                halign: "center"
                pos_hint: {'center_y': .79}

            MDLabel:
                id: error_label  
                text: ""
                color: "#FF0000"
                bold: True
                font_size: "18dp"
                halign: "center"
                pos_hint: {'center_y': .72}
                
            MDTextField:
                id: username
                hint_text: "Username"
                icon_right: "account"
                helper_text: "Enter username"
                helper_text_mode: "on_focus"
                font_size: "20dp"
                size_hint_x: .85
                pos_hint: {'center_x': .5, 'center_y': .65}
                on_text: self.text = self.text.replace(" ", "")
                write_tab: False

            MDTextField:
                id: password
                hint_text: "Password"
                password: True
                icon_right: "eye-off"
                helper_text: "Enter password"
                helper_text_mode: "on_focus"
                font_size: "20dp"
                size_hint_x: .85
                pos_hint: {'center_x': .5, 'center_y': .5}
                on_text: self.text = self.text.replace(" ", "")
                write_tab: False
           
                    
            BoxLayout: 
                size_hint: .6, None
                height: "30dp"
                pos_hint: {'center_x': .5, 'center_y': .3}
                spacing: '15dp'
                
                MDRectangleFlatIconButton:
                    text: "Sign Up"
                    icon: "account-edit" 
                    font_size: "22dp"
                    size_hint_x: 1
                    md_bg_color: "lightblue"
                    on_press: app.root.current = 'signup'

            BoxLayout: 
                size_hint: .6, None
                height: "30dp"
                pos_hint: {'center_x': .5, 'center_y': .2}
                spacing: '15dp'

                MDRectangleFlatIconButton:
                    text: "Log In"
                    icon: "account-check" 
                    font_size: "22dp"
                    size_hint_x: 1
                    md_bg_color: "lightblue"
                    on_release: app.login(username.text, password.text)

<SignUpScreen>:
    name: 'signup'
    MDBottomNavigation:
        panel_color: "#EAE8E8"
        selected_color_background: "pink"
        text_color_active: "black"

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Quick Sort App'
            icon: 'warehouse'

            Image:
                source: "logo.png"
                size_hint: None, None
                width: "80dp"
                height: "80dp"
                pos_hint: {'center_x': .5, 'center_y': .9}
            MDLabel:
                text: "Sign up"
                source: "logo.png"
                color: "#484747"
                bold: True
                font_size: "48dp"
                halign: "center"
                pos_hint: {'center_y': .79}

            MDLabel:
                id: error_label  
                text: ""
                color: "#FF0000"
                bold: True
                font_size: "18dp"
                halign: "center"
                pos_hint: {'center_y': .72}
                
            MDTextField:
                id: username
                hint_text: "Username"
                icon_right: "account"
                helper_text: "Enter username"
                helper_text_mode: "on_focus"
                font_size: "20dp"
                size_hint_x: .85
                pos_hint: {'center_x': .5, 'center_y': .65}
                on_text: self.text = self.text.replace(" ", "")
                write_tab: False

            MDTextField:
                id: password
                hint_text: "Password"
                password: True
                icon_right: "eye-off"
                helper_text: "Enter password"
                helper_text_mode: "on_focus"
                font_size: "20dp"
                size_hint_x: .85
                pos_hint: {'center_x': .5, 'center_y': .5}
                on_text: self.text = self.text.replace(" ", "")
                write_tab: False
           
                    
            BoxLayout: 
                size_hint: .6, None
                height: "30dp"
                pos_hint: {'center_x': .5, 'center_y': .3}
                spacing: '15dp'
                
                MDRectangleFlatIconButton:
                    text: "Sign Up"
                    icon: "account-edit" 
                    font_size: "22dp"
                    size_hint_x: 1
                    md_bg_color: "lightblue"
                    on_press: app.signup(username.text, password.text)

            BoxLayout: 
                size_hint: .6, None
                height: "30dp"
                pos_hint: {'center_x': .5, 'center_y': .2}
                spacing: '15dp'

                MDRectangleFlatIconButton:
                    text: "Log In"
                    icon: "account-check" 
                    font_size: "22dp"
                    size_hint_x: 1
                    md_bg_color: "lightblue"
                    on_press: app.root.current = 'login'

"""



class SplashScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class QuickSortApp(MDApp):
    def build(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="inventory"
        )
        self.cursor = self.conn.cursor()
        self.sm = ScreenManager()
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(SignUpScreen(name='signup'))
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(self.show_login, 3)

    def show_login(self, dt):
        self.root.current = 'login'

    def login(self, username, password):
        if self.authenticate(username, password):
            self.username = username  
            self.root.current = 'main'
            self.refresh_inventory_content()
        else:
            print("Invalid credentials")

    def authenticate(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = self.cursor.fetchone()
        return user is not None

    def refresh_inventory_content(self):
        inventory_content = self.root.get_screen('main').ids.inventory_content
        inventory_content.clear_widgets()
        user_id = self.get_user_id(self.username)
        if user_id:
            self.cursor.execute("SELECT * FROM inventory WHERE user_id=%s", (user_id,))
            inventory_items = self.cursor.fetchall()
            for item in inventory_items:
                inventory_content.add_widget(
                    OneLineListItem(text=f"ID: {item[0]} - {item[2]} - Quantity: {item[3]}")
                )
        else:
            print("User not found")

    def add_item(self, username, name, quantity):
        user_id = self.get_user_id(username)
        if name and quantity and user_id:
            try:
                quantity = int(quantity)
                self.cursor.execute("INSERT INTO inventory (user_id, name, quantity) VALUES (%s, %s, %s)",
                                    (user_id, name, quantity))
                self.conn.commit()
                self.refresh_inventory_content()
            except ValueError:
                print("Invalid quantity input")
        else:
            print("Name, quantity, and user_id are required")

    def update_item(self, username, item_id, new_quantity):
        user_id = self.get_user_id(username)
        if item_id and new_quantity and user_id:
            try:
                item_id = int(item_id)
                new_quantity = int(new_quantity)
                self.cursor.execute("UPDATE inventory SET quantity=%s WHERE id=%s AND user_id=%s",
                                    (new_quantity, item_id, user_id))
                self.conn.commit()
                self.refresh_inventory_content()
            except ValueError:
                print("Invalid item ID or quantity input")
        else:
            print("Item ID, new quantity, and user_id are required")

    def delete_item(self, username, item_id):
        user_id = self.get_user_id(username)
        if item_id and user_id:
            try:
                item_id = int(item_id)
                self.cursor.execute("DELETE FROM inventory WHERE id=%s AND user_id=%s", (item_id, user_id))
                self.conn.commit()
                self.refresh_inventory_content()
            except ValueError:
                print("Invalid item ID input")
        else:
            print("Item ID and user_id are required")

    def get_user_id(self, username):
        self.cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user = self.cursor.fetchone()
        if user:
            return user[0]
        else:
            return None

    def signup(self, username, password):
        if username and password:
            self.cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            existing_user = self.cursor.fetchone()
            if existing_user:
                print("Username already taken")
            else:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                self.conn.commit()
                print("User registered successfully")
                self.root.current = 'login'
        else:
            print("Username and password are required")

    def logout(self):
        self.username = None
        self.root.current = 'login'

if __name__ == '__main__':
    QuickSortApp().run()
