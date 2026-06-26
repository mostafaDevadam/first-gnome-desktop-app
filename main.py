import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, Adw, Gio, GLib, Gdk, Notify

Notify.init('com.example.myapp')

import sys
import urllib.request
import threading
import json
import os

print("start py")

# dark, i18n, search, cache
# save users, posts, comments in json files in init/background
# search in: local, storage, users, posts, todos
# auth: register,login -> save in json file
# settings: save in json file


class Jasmin():
      
      def __init__(self, name, right_sidebar, center_stack):
          self.name = name
          self.right_sidebar = right_sidebar
          self.center_stack = center_stack

      def get_name(self):
          return self.name
      
      def set_name(self, name):
          print(f"set_name: {name}")
          self.name = name


      def build_test_view(self):
            #
            local_wrapper = Adw.ToolbarView()

            local_action_bar = Gtk.HeaderBar()
            local_action_bar.set_show_title_buttons(False) 
            local_title = Gtk.Label(label="test Manager")
            local_title.add_css_class("heading")
            local_action_bar.set_title_widget(local_title)

            local_wrapper.add_top_bar(local_action_bar)


            scroll_win = Gtk.ScrolledWindow()
            scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

            content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            content_box.set_margin_top(24)
            content_box.set_margin_bottom(24)
            content_box.set_margin_start(24)
            content_box.set_margin_end(24)

            local_items_group = Adw.PreferencesGroup()
            local_items_group.set_title("test ui")


            # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
            content_box.append(local_items_group)
            scroll_win.set_child(content_box)
            local_wrapper.set_content(scroll_win)
            
            # Mount layout to stack structure immediately 
            self.center_stack.add_named(local_wrapper, "local_test_view")


            docs = []   


            def test_fetch():
                print("test_fetch")
                import time
                time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
                
                file_path = os.path.join(GLib.get_current_dir(), "test.json")

                if not os.path.exists(file_path):
                    print("no json file")
                    return False
                
                print("json file exists!")

                def card_clicked(row):
                    print(f"card_clicked: {row.payload}")

                    item = row.payload

                    #
                    while child := self.right_sidebar.get_first_child():
                        self.right_sidebar.remove(child)
                    #
                    self.right_sidebar.set_margin_top(16)
                    self.right_sidebar.set_margin_start(12)
                    self.right_sidebar.set_margin_end(12)
                    self.right_sidebar.set_margin_bottom(16)
                    #
                    title_label = Gtk.Label(label=item.get("title"))
                    title_label.add_css_class("title-1") # built-in font bold
                    title_label.set_margin_bottom(12)
                    title_label.set_halign(Gtk.Align.START)
                    self.right_sidebar.append(title_label)
                    #
                    body_label = Gtk.Label(label=item.get("author"))
                    body_label.add_css_class("dim-label") # built-in font bold
                    body_label.set_margin_bottom(24)
                    body_label.set_halign(Gtk.Align.START)
                    body_label.set_wrap(True)
                    self.right_sidebar.append(body_label)
                    #sidebar_group = Adw.PreferencesGroup()
                    #sidebar_group.set_title("User Information")

                
                    # inject the completed data card into right-sidebar
                    #self.right_sidebar.append(sidebar_group)
                    #
                    #sidebar_group.set_margin_start(8)
                    #sidebar_group.set_margin_end(8)

                try:
                    success, content = GLib.file_get_contents(file_path)

                    if success:
                        if isinstance(content, bytes):
                            content = content.decode("utf-8")
                            
                        data = json.loads(content)
                        print(f"data size: {len(data)}")
                        
                        for item in data:
                            print(f"item: {item}")
                            docs.append(item)
                            card = Adw.ActionRow()
                            card.set_title(item.get("title", "test"))
                            card.set_subtitle(item.get("author", "test"))
                            card.set_activatable(True)
                            card.payload = item
                            card.connect("activated", card_clicked)
                            card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                            local_items_group.add(card)
                        
                        # --- ACTION TAKEN HERE ---
                        # Now that docs is populated, safely trigger your UI updates or prints:
                        print(f"len docs inside callback: {len(docs)}")

                        local_items_group.queue_resize()
                        
                        

                    else:
                        print("GLib failed to read file contents successfully.")
                except Exception as e:
                    print(f"ERROR: {e}")

                return False # Stop the GLib idle loop from repeating this function
            
            # Queue the function to run as soon as the main loop is ready
            GLib.idle_add(test_fetch)

            


            #content_box.append(local_items_group)
            #scroll_win.set_child(content_box)
            #local_wrapper.set_content(scroll_win)


            #
            #self.center_stack.add_named(local_wrapper, "local_test_view")
           

class HandleJsonFile():

    def read_json_file(self, populate_ui_cards, folder_name, json_file_name):
        #
        docs = []
        import time
        time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
        
        file_path = os.path.join(GLib.get_current_dir(), f"./{folder_name}/{json_file_name}.json")

        if not os.path.exists(file_path):
            print("no json file")
            return False
        
        print("json file exists!")
        #
        
        #
        try:
            success, content = GLib.file_get_contents(file_path)

            if success:
                if isinstance(content, bytes):
                    content = content.decode("utf-8")
                    
                data = json.loads(content)
                #docs = data
                print(f"data size: {len(data)}")
                GLib.idle_add(populate_ui_cards, data)
                return
            else:
                print("GLib failed to read file contents successfully.")
                return []


        except Exception as e:
            print(f"ERROR: {e}")
            return []
        
        return False

    def load_data_from_json_file(self, folder_name, json_file_name):
        file_path = os.path.join(GLib.get_current_dir(), f"./{folder_name}/{json_file_name}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    
                    return json.load(f)
              
            except Exception as e:
                print(f"Error reading data file: {e}")
        return []

    def save_data_to_json_file(self, arr, folder_name, json_file_name):
        file_path = os.path.join(GLib.get_current_dir(), f"./{folder_name}/{json_file_name}.json")

        try:
            with open(file_path, "w") as f:
                json.dump(arr, f, indent=4)
        except Exception as e:
            print(f"Error saving data file: {e}")

# i18n


class I18n():
        
    def __init__(self):
                # 1. Define your active language track string
                self.current_lang = "en"  # Switch this to "en", "ar", etc.

                # 2. Build your translation mapping dictionary right inside code memory
                self.translations = {
                                "en": {
                                    "posts": "Posts",
                                    "posts_mgmt": "Posts Management",
                                    "add_new": "Add New One",
                                    "enter_name": "Enter name...",
                                    "no_items": "No items recorded yet.",
                                    "tab_home": "Home",
                                    "tab_settings": "Settings",
                                    "tab_profile" : "Profile",
                                    "item_test": "Test",
                                    "item_local": "Local",
                                    "item_storage": "Storage",
                                    "item_users": "Users",
                                    "item_posts": "Posts",   # Pure English value mapping
                                    "item_todos": "Todos",
                                    "item_shell": "Shell Terminal",
                                    "shell_manager": "System Shell Workspace",
                                    "shell_run_btn": "Execute",
                                    "shell_placeholder": "Type shell command here...",
                                    "gnome_app": "My Gnome App",
                                    "search_placeholder": "Search records...",
                                    "local_manager": "Local List Manager",
                                    "btn_add": "Add",
                                    "popover_add_title": "Add New One",
                                    "input_name_ph": "Enter name...",
                                    "input_desc_ph": "Enter description",
                                    "btn_submit": "Submit",
                                    "group_title": "Stored Local Entries",
                                    "empty_list_text": "No items recorded yet. click 'Add' above to build a list.",
                                    "group_disk_title": "Stored Data in Disk with Entries",
                                    "disk_manager": "Disk List Manager",
                                    "login_title": "Login",
                                    "email": "Email",
                                    "password": "Password",
                                    "enter_email": "Enter Email",
                                    "enter_password": "Enter Password",
                                    "login_success_msg": "Login successful! Welcome back.",
                                    "logout_title": "Logout",
                                    "login_failure_msg": "Login failed: Email and password fields cannot be empty.",
                                    #"register_title": "Register",
                                    "register_success_msg": "Register successful! Welcome.",
                                    "register_failure_msg": "Register failed: Email and password fields cannot be empty.",
                                    "setting_general_item": "General",
                                    "setting_account_item": "Account",
                                    "setting_notifications_item": "Notifications",
                                    "setting_display_item": "display",
                                    "setting_colors_item": "Colors" ,
                                    "setting_keyboard_item": "Keyboard",
                                    "register_title": "Create Account",
                                    "username": "Username",
                                    "enter_username": "Enter Username",
                                    "btn_register": "Register",
                                    "switch_to_register": "Don't have an account? Sign Up",
                                    "switch_to_login": "Already have an account? Sign In",
                                    


                              
                              
                              
                               },
                                "ar": {  # Matches your custom 'self.current_lang = "ar"' target
                                    "posts": "المنشورات",
                                    "posts_mgmt": "إدارة المنشورات",
                                    "add_new": "إضافة عنصر جديد",
                                    "enter_name": "أدخل الاسم...",
                                    "no_items": "لم يتم تسجيل أي عناصر بعد.",
                                    "tab_home": "الرئيسية",
                                    "tab_settings": "الاعدادات",
                                    "tab_profile" : "حسابي", #"الملف الشخصي",
                                    "item_test": "تجربة",
                                    "item_local": "محلي",
                                    "item_storage": "التخزين",
                                    "item_users": "المستخدمين",
                                    "item_posts": "المنشورات", # Pure Arabic value mapping
                                    "item_todos": "المهام",
                                    "item_shell": "الشل",
                                    "item_text" : "محطة الشل",
                                    "shell_manager": "مساحة عمل الشل نظام",
                                    "shell_run_btn": "تنفيذ",
                                    "shell_placeholder": "اكتب أمر الشل هنا...",
                                    "gnome_app": "تطبيق جينوم ",
                                    "search_placeholder": "البحث في السجلات...",  
                                    "local_manager": "مدير القائمة المحلية",
                                    "btn_add": "إضافة",
                                    "popover_add_title": "إضافة عنصر جديد",
                                    "input_name_ph": "أدخل الاسم...",
                                    "input_desc_ph": "أدخل الوصف",
                                    "btn_submit": "إرسال",
                                    "group_title": "العناصر المحلية المحفوظة",
                                    "empty_list_text": "لم يتم تسجيل أي عناصر بعد. انقر فوق 'إضافة' أعلاه لإنشاء قائمة.",
                                    "group_disk_title": "البيانات المحفوظة في القرص مع العناصر",
                                    "disk_manager": "مدير قائمة القرص",
                                    "login_title": "دخول",
                                    #"register_title": "تسجيل",
                                    "email": "Email",
                                    "password": "Password",
                                    "enter_email": "ادخل البريد الالكترونى",
                                    "enter_password": "ادخل كلمة السر",
                                    "login_success_msg": "تم تسجيل الدخول بنجاح! مرحبًا بعودتك.",
                                    "logout_title": "خروج",
                                    "login_failure_msg": "فشل تسجيل الدخول: لا يمكن ترك حقول البريد الإلكتروني وكلمة المرور فارغة.",
                                    "setting_general_item": "عام",
                                    "setting_account_item": "الحساب",
                                    "setting_notifications_item": "الإشعارات",
                                    "setting_display_item": "العرض",
                                    "setting_colors_item": "الألوان",
                                    "setting_keyboard_item": "لوحة المفاتيح",
                                    "register_title": "إنشاء حساب",
                                    "username": "اسم المستخدم",
                                    "enter_username": "أدخل اسم المستخدم",
                                    "btn_register": "تسجيل",
                                    "switch_to_register": "ليس لديك حساب؟ سجل الآن",
                                    "switch_to_login": "لديك حساب بالفعل؟ تسجيل الدخول",



                               
                               
                               
                               
                               
                               
                                }
                }



    def _(self, key):
        """ Inline key translator lookup utility """
        # Pull string based on active language, default back to English if missing
        lang_dict = self.translations.get(self.current_lang, self.translations["en"])
        
        # Return the translated text or return the raw key string if not found
        return lang_dict.get(key, self.translations["en"].get(key, key))



# app

class MyApp(Adw.Application):

    state = ""
    def __init__(self):
        print("MyApp init")
        super().__init__(
            application_id="com.example.myapp", 
            flags=Gio.ApplicationFlags.FLAGS_NONE
            )
        #
        self.handle_json_file = HandleJsonFile()
        
        
        #
        self.right_sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.center_stack = Gtk.Stack()
        self.jam = Jasmin("jasmin", self.right_sidebar, self.center_stack)
        
        #os.system("sudo systemctl restart NetworkManager")
        #self.connect('activate', self.on_activate)
        self.local_items_storage = []
        self.local_items_group = Adw.PreferencesGroup()
        #self.state = ""
        #
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file_path = os.path.join(curr_dir, "./storage/local_data.json")
        #self.disk_items_storage = self.load_data_from_disk()
        self.disk_items_storage = self.handle_json_file.load_data_from_json_file("storage", "local_data")
            
        self.disk_items_group = Adw.PreferencesGroup()
        #
        self.test_items_group = Adw.PreferencesGroup()
        self.test_items = []
        #
        self.local_users_group = Adw.PreferencesGroup()
        self.local_users_items = []
        #
        self.local_posts_group = Adw.PreferencesGroup()
        self.local_posts_items = []
        #
        self.local_todos_group = Adw.PreferencesGroup()
        self.local_todos_items = []
        # locale
        Gtk.Widget.set_default_direction(Gtk.TextDirection.LTR)
        self.current_lang = "en"
        self.i18n = I18n()
        self.registered_widgets = []
        #lang_action = Gio.SimpleAction.new("change-language", GLib.VariantType.new("s"))
        

        """quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_clicked)
        self.add_action(quit_action)"""

        #

        
        #
        #self.list_box = Gtk.ListBox()
        #self.tab1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        #
        self.nav_rows = {}
        self.nav_settings_rows = {}
        #
        self.isLogin = False
        self.logout_btn = Gtk.Button(label=self.i18n._('logout_title'))
        #self.logout_action = Gio.SimpleAction.new("logout", None)
        #
        self.menu = Gio.Menu.new()
        #

        
    def register_widget(self, widget, prop, key):
        self.registered_widgets.append((widget, prop, key))
        self.update_widget_text(widget, prop, key)

    def update_widget_text(self, widget, prop, key):
        """ Translates ans sets text dynamically"""
        translated_text = self.i18n._(key)
        #
        if prop == "text" and hasattr(widget, "set_text"):
           widget.set_text(translated_text)
        elif prop == "label" and hasattr(widget, "set_label"):
            widget.set_label(translated_text)
        elif prop == "title" and  hasattr(widget, "set_title"):
            widget.set_title(translated_text)
        elif prop == "placeholder" and hasattr(widget, "set_placeholder_text"):
            widget.set_placeholder_text(translated_text)

    def change_app_language(self, lang_code):
        self.current_lang = lang_code
        self.i18n.current_lang = lang_code
        #
       
        # 
        if lang_code == "ar":
            Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)
            #self.win.set_direction(Gtk.TextDirection.RTL)
            if hasattr(self, 'win') and self.win:
                self.win.set_direction(Gtk.TextDirection.RTL)
                self.win.queue_allocate()
            if hasattr(self, 'info_label') and self.info_label:
                self.info_label.set_text("Current Layout: RTL")
            #
            self.view_switcher.set_policy(Adw.ViewSwitcherPolicy.NARROW)
            self.view_switcher.remove_css_class("view-switcher-ltr")
            self.view_switcher.add_css_class("view-switcher-rtl")
        else:
             Gtk.Widget.set_default_direction(Gtk.TextDirection.LTR)
             if hasattr(self, 'win') and self.win:
                self.win.set_direction(Gtk.TextDirection.LTR)
                self.win.queue_allocate()
             if hasattr(self, 'info_label') and self.info_label:
                self.info_label.set_text("Current Layout: LTR")
            #
             self.view_switcher.set_policy(Adw.ViewSwitcherPolicy.NARROW)
             self.view_switcher.remove_css_class("view-switcher-rtl")
             self.view_switcher.add_css_class("view-switcher-ltr")
        
        #
        if hasattr(self, 'win') and self.win:
           self.win.set_title(self.i18n._("gnome_app")) 
        #
        for widget, prop, key in self.registered_widgets:
            self.update_widget_text(widget, prop, key)
        #
        self.refresh_row_dictionaries()
        #


    def refresh_row_dictionaries(self):
        for row_attr in ["nav_rows", "nav_settings_rows"]:
            if hasattr(self, row_attr):
                row_dict = getattr(self, row_attr)
                if row_dict:
                    for key, row_widget in row_dict.items():
                        if hasattr(row_widget, "set_title"):
                            row_widget.set_title(self.i18n._(key))
    
    def on_language_action_activated(self, action, parameter):
        print("on_language_action_activated")
        #
        lang_code = parameter.get_string()
        print(f"lang_code: {lang_code}")
        action.set_state(GLib.Variant.new_string(lang_code))
        #action.set_state(parameter)
        self.change_app_language(lang_code)
        #
    
    def on_toggle_locale_direction_clicked(self, button):
        new_lang = "ar" if self.i18n.current_lang == "en" else "en"
        self.change_app_language(new_lang)
    

    def load_data_from_disk(self):
        if os.path.exists(self.data_file_path):
            try:
                with open(self.data_file_path, "r") as f:
                    
                    return json.load(f)
              
            except Exception as e:
                print(f"Error reading data file: {e}")
        return []
    
    def save_data_to_disk(self):
        self.handle_json_file.save_data_to_json_file(self.disk_items_storage, "storage", "local_data")
        """try:
            with open(self.data_file_path, "w") as f:
                json.dump(self.disk_items_storage, f, indent=4)
        except Exception as e:
            print(f"Error saving data file: {e}")"""

    def sidebar_items(self):
        return  [
            ("Test", "folder-download-symbolic"),
            ("Local", "folder-download-symbolic"),
            ("Storage", "drive-harddisk-symbolic"),
            ("Users", "avatar-default-symbolic"),
            (self.i18n._('posts'), "mail-send-receive-symbolic"),
            ("Todos", "checkbox-checked-symbolic")
        ]

    def rebuild_list_box(self):
        home_items = [
            ("Test", "folder-download-symbolic"),
            ("Local", "folder-download-symbolic"),
            ("Storage", "drive-harddisk-symbolic"),
            ("Users", "avatar-default-symbolic"),
            (self.i18n._('posts'), "mail-send-receive-symbolic"),
            ("Todos", "checkbox-checked-symbolic")
        ]
        list_box = Gtk.ListBox()

        for title, icon_name in home_items:
            row = Adw.ActionRow()
            row.set_title(title)
            row.set_activatable(True)

            #row.set_margin_start(8)
            #row.set_margin_end(8)

            prefix_icon = Gtk.Image.new_from_icon_name(icon_name)
            row.add_prefix(prefix_icon)

            suffix_arrow = Gtk.Image.new_from_icon_name("go-next-symbolic")
            row.add_suffix(suffix_arrow)

            row.connect("activated", self.on_home_item_clicked)

            list_box.append(row)
        return list_box
        #self.tab1_box.append(list_box)
         


    def do_activate(self):
        # this is called g_application_activate() -> app.run()

        # locale
        #self.i18n.current_lang = "ar"
        #Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)
        #self.current_lang = "ar"
        
        #
        self.init_direction_lang()

        print(f"i18n: {self.i18n._("posts")}")

        # dark-mode
        self.style_manager = Adw.StyleManager.get_default()
        self.style_manager.set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)

        # window
        #win = Adw.ApplicationWindow(application=app)
        self.win = Adw.ApplicationWindow(application=self)
        self.win.set_title(f"{self.i18n._('gnome_app')}")
        self.win.set_default_size(600, 400)

        #
        self.apply_custom_styles()

        #
        self.refresh_row_dictionaries()
        #

        

        # create toolbar
        toolbar_view = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        # add css-class to header-bar
        header_bar.add_css_class("custom-topbar")
        # add header_bar in toolbar
        toolbar_view.add_top_bar(header_bar)

        # menu: language-switcher 
        menu_lang = Gio.Menu.new()
        menu_lang.append("English", "app.lang::en")
        menu_lang.append("العربية (Arabic)", "app.lang::ar")
    

        
        """quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_clicked)
        self.add_action(quit_action)"""
        # English item
        """en_item = Gio.MenuItem.new("English", "app.lang::en")
        en_item.set_attribute_value("icon", GLib.Variant.new_string("en-US"))
        menu_lang.append_item(en_item)
        
        # Arabic item
        ar_item = Gio.MenuItem.new("العربية (Arabic)", "app.lang::ar")
        ar_item.set_attribute_value("icon", GLib.Variant.new_string("ar-SA"))
        menu_lang.append_item(ar_item)"""

        # Create action
        lang_action = Gio.SimpleAction.new_stateful(
            "lang",
            GLib.VariantType.new("s"),
            GLib.Variant.new_string("en")
        )
        lang_action.connect("activate", self.on_language_action_activated)
        self.add_action(lang_action)

        lang_menu_button = Gtk.MenuButton()
        lang_menu_button.set_icon_name("preferences-desktop-locale-symbolic")
        lang_menu_button.set_menu_model(menu_lang)
        header_bar.pack_end(lang_menu_button)

        # toggle button for switch locale: text-direction
        """toggle_btn = Gtk.Button.new_from_icon_name("object-flip-horizontal-symbolic")
        toggle_btn.set_tooltip_text("Toggle RTL/LTR")
        toggle_btn.connect("clicked", self.on_toggle_direction_clicked)
        # add toggle_btn in header-bar
        header_bar.pack_start(toggle_btn)"""

        # theme-buttton
        self.theme_btn = Gtk.Button()
        self.theme_btn.set_icon_name("weather-clear-symbolic")
        self.theme_btn.connect("clicked", self.on_toggle_theme_clicked)
        header_bar.pack_start(self.theme_btn)

        # logout-button
        #self.logout_btn = Gtk.Button(label=self.i18n._('logout_title'))
        self.logout_btn.connect("clicked", self.on_logout_button_clicked)
        #if self.isLogin:
        self.logout_btn.set_visible(False)
        header_bar.pack_start(self.logout_btn)

        # menu in header_bar
        """self.menu = Gio.Menu.new()
        self.menu.append("About", "app.about")
        self.menu.append("Quit", "app.quit")
        self.menu.append("Restart", "app.restart")"""
        #self.menu.append("Logout", "app.logout")
        #self.logout_action.set_enabled(False)

        GLib.idle_add(self.rebuild_menu)
        self.setup_actions()


        # menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_menu_model(self.menu)
        menu_button.set_icon_name("open-menu-symbolic")

        # add in header_bar
        header_bar.pack_end(menu_button)



        # actions for menu clicks
        #self.setup_actions()


        

        #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(100)
        box.set_margin_bottom(24)
        box.set_margin_start(24)
        box.set_margin_end(24)
        # info_label
        #self.info_label = Gtk.Label(label = "Current Layout: LTR")
        


        # label
        label = Gtk.Label(label="Hallo, Gnome")
        label.set_markup("<span size='x-large'>Welcome to Gnome Desktop App</span>")
        # button
        button = Gtk.Button(label="Click!")
        button.connect('clicked', lambda b: print("Button is clicked!"))

        #
        #box.append(self.info_label)
        box.append(label)
        box.append(button)

        # left-sidebar
        left_sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        left_sidebar.add_css_class("sidebar-panel")
        left_sidebar.set_size_request(200, -1)
        left_label = Gtk.Label(label="Left Sidebar")
        left_label.set_margin_top(12)
        #left_sidebar.append(left_label)

        # tabs in left-sidebar
        view_stack = Adw.ViewStack()
        view_stack.set_vexpand(True)
        view_stack.set_margin_start(8)
        view_stack.set_margin_end(8)

        tab1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        tab1_box.set_margin_top(12)
        #tab1_box.append(Gtk.Label(label="Tab1"))

        self.home_page_wrapper = view_stack.add_titled(tab1_box, "home", self.i18n._("tab_home"))
        self.home_page_wrapper.set_icon_name("user-home-symbolic") 
        self.register_widget(self.home_page_wrapper, 'title', 'tab_home')

        # Left items list box configuration
        self.list_box = Gtk.ListBox()
        self.list_box.add_css_class("boxed-list")

        home_items = [
            
            ("item_test", "folder-download-symbolic"),
            ("item_local", "folder-download-symbolic"),
            ("item_storage", "drive-harddisk-symbolic"),
            ("item_users", "avatar-default-symbolic"),
            ("item_posts", "mail-send-receive-symbolic"), # FIX: Changed from function call to abstract key string
            ("item_todos", "checkbox-checked-symbolic"),
            ("item_shell", "utilities-terminal-symbolic"),
        ]

        # Tracking dictionary to easily find rows during translation refresh cycles
        

        for key, icon_name in home_items:
            row = Adw.ActionRow()
            
            # Initial text mapping on initialization canvas
            row.set_title(self.i18n._(key))
            #row.set_title(key)
            row.set_activatable(True)

            # Store the translation key identifier tag property on the row instance
            row.nav_item_key_id = key

            prefix_icon = Gtk.Image.new_from_icon_name(icon_name)
            row.add_prefix(prefix_icon)

            suffix_arrow = Gtk.Image.new_from_icon_name("go-next-symbolic")
            row.add_suffix(suffix_arrow)

            row.connect("activated", self.on_home_item_clicked)

            self.list_box.append(row)
            
            # Save a link to this row matching its translation tracking key
            self.nav_rows[key] = row

        

        """for title, icon_name in home_items:
            row = Adw.ActionRow()
            row.set_title(title)
            row.set_activatable(True)

            #row.set_margin_start(8)
            #row.set_margin_end(8)

            prefix_icon = Gtk.Image.new_from_icon_name(icon_name)
            row.add_prefix(prefix_icon)

            suffix_arrow = Gtk.Image.new_from_icon_name("go-next-symbolic")
            row.add_suffix(suffix_arrow)

            row.connect("activated", self.on_home_item_clicked)

            list_box.append(row)"""



        tab1_box.append(self.list_box)
        
        # tab2
        tab2_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        tab2_box.set_margin_top(12)
        #tab2_box.append(Gtk.Label(label="tab2"))

        #page2 = view_stack.add_titled(tab2_box, "settings", "Settings")
        #page2.set_icon_name("emblem-system-symbolic")
        self.page2_wrapper = view_stack.add_titled(tab2_box, "settings", self.i18n._("tab_settings"))
        self.page2_wrapper.set_icon_name("emblem-system-symbolic") 
        self.register_widget(self.page2_wrapper, 'title', 'tab_settings')


        #
        self.list2_box = Gtk.ListBox()
        self.list2_box.add_css_class("boxed-list")

       

        settings_items = [
            ("setting_general_item", "preferences-system-symbolic"),       # Clean gear/sliders icon
            ("setting_account_item", "avatar-default-symbolic"),           # Crisp user profile silhouette
            ("setting_notifications_item", "preferences-system-notifications-symbolic"), # Bell icon
            ("setting_display_item", "video-display-symbolic"),            # Monitor/screen icon
            ("setting_colors_item", "preferences-desktop-wallpaper-symbolic"), # Color palette/dropper icon
            ("setting_keyboard_item", "input-keyboard-symbolic")
        ]

        # Tracking dictionary to easily find rows during translation refresh cycles
        

        for key, icon_name in settings_items:
            row = Adw.ActionRow()
            
            # Initial text mapping on initialization canvas
            row.set_title(self.i18n._(key))
            #row.set_title(key)
            row.set_activatable(True)

            # Store the translation key identifier tag property on the row instance
            row.nav_item_key_id = key

            prefix_icon = Gtk.Image.new_from_icon_name(icon_name)
            row.add_prefix(prefix_icon)

            suffix_arrow = Gtk.Image.new_from_icon_name("go-next-symbolic")
            row.add_suffix(suffix_arrow)

            row.connect("activated", self.on_settings_item_clicked)

            self.list2_box.append(row)
            
            # Save a link to this row matching its translation tracking key
            self.nav_settings_rows[key] = row

        tab2_box.append(self.list2_box)


        #tab3
        tab3_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        tab3_box.set_margin_top(12)
        #tab3_box.append(Gtk.Label(label="tab3"))

        #page3 = view_stack.add_titled(tab3_box, "profile", "Profile")
        #page3.set_icon_name("avatar-default-symbolic")
        self.page3_wrapper = view_stack.add_titled(tab3_box, "profile", self.i18n._("tab_profile"))
        self.page3_wrapper.set_icon_name("avatar-default-symbolic") 
        self.register_widget(self.page3_wrapper, 'title', 'tab_profile')


        # view_switcher
        self.view_switcher = Adw.ViewSwitcher()
        self.view_switcher.set_stack(view_stack)
        
        self.view_switcher.set_margin_top(6)
        #view_switcher.set_margin_start(6)
        #view_switcher.set_margin_end(6)
        #view_switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        self.view_switcher.add_css_class("custom-view-switcher-bg")
        self.view_switcher.add_css_class("view-switcher-ltr")
        self.view_switcher.set_policy(Adw.ViewSwitcherPolicy.NARROW)


        # view_switcher_bar
        # bottom viewSwitcherBar
        view_switcher_bar = Adw.ViewSwitcherBar()
        #view_switcher_bar.set_stack(view_stack)
        #view_switcher_bar.set_reveal(True)

        # add in left_sidebar
        left_sidebar.append(self.view_switcher)
        left_sidebar.append(view_stack)
        #left_sidebar.append(view_switcher_bar)
        # search-bar
        search_bar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        search_bar_box.set_margin_top(12)
        search_bar_box.set_margin_bottom(12)
        search_bar_box.set_margin_start(16)
        search_bar_box.set_margin_end(16)

        self.sidebar_search_entry = Gtk.SearchEntry()
        self.sidebar_search_entry.set_hexpand(True)
        self.sidebar_search_entry.set_placeholder_text(self.i18n._("search_placeholder"))
        self.sidebar_search_entry.connect("search-changed", self.on_sidebar_search_changed)
        self.register_widget(self.sidebar_search_entry, 'placeholder', 'search_placeholder')

        search_bar_box.append(self.sidebar_search_entry)

        left_sidebar.append(search_bar_box)
        
        
        # main content
        #center_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        #center_content.set_margin_top(24)
        #center_content.set_margin_bottom(24)
        #center_content.set_margin_start(24)
        #center_content.set_margin_end(24)
        #center_content.set_hexpand(True)
        self.center_stack = Gtk.Stack()
        self.center_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.center_stack.set_hexpand(True)
        self.center_stack.set_vexpand(True)

        # View A: welcome_box
        welcome_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        welcome_box.set_valign(Gtk.Align.CENTER)
        self.info_label = Gtk.Label(label="Current layout: LTR")
        welcome_box.append(self.info_label)
        self.center_stack.add_named(welcome_box, "welcome_view")


        # View B: loading_box
        loading_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        loading_box.set_valign(Gtk.Align.CENTER)
        spinner = Gtk.Spinner()
        spinner.start()
        spinner.set_size_request(40, 40)
        loading_box.append(spinner)
        loading_label = Gtk.Label(label="Fetching live user cards...")
        loading_box.append(loading_label)
        self.center_stack.add_named(loading_box, "loading_view")


        # scroll
        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        # CRITICAL FIXES: Force the scrollable area to expand to fill the screen space
        scroll_win.set_vexpand(True)
        scroll_win.set_hexpand(True)

        """self.users_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.users_container.set_margin_top(24)
        self.users_container.set_margin_bottom(24)
        self.users_container.set_margin_start(24)
        self.users_container.set_margin_end(24)

        # CRITICAL FIXES: Force the inner container box to expand inside the scroll view
        self.users_container.set_vexpand(True)
        self.users_container.set_hexpand(True)

        # Build the layout tree relationship cleanly
        scroll_win.set_child(self.users_container)
        self.center_stack.add_named(scroll_win, "users_view")"""
        #self.center_stack.add_child(self.users_view_scroll)

        #

        """self.test_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.test_container.set_margin_top(24)
        self.test_container.set_margin_bottom(24)
        self.test_container.set_margin_start(24)
        self.test_container.set_margin_end(24)

        scroll_win.set_child(self.test_container)
        self.center_stack.add_named(scroll_win, "test_view")"""
        self.build_test_view()
        self.build_test_users_view()
        self.jam.build_test_view()
        self.build_test_posts_view2()
        self.build_test_todos_view()

        # test jasmin
        j = self.jam.get_name()
        print(f"jam: {j}")


        # View E: Local
        self.build_local_tabs_view()

        # View F: storage in disk
        self.build_disk_tabs_view()

        # View : Shell
        self.build_shell_view()


        # View S: Posts
        """self.posts_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.posts_container.set_margin_top(24)
        self.posts_container.set_margin_bottom(24)
        self.posts_container.set_margin_start(24)
        self.posts_container.set_margin_end(24)

        scroll_win.set_child(self.posts_container)
        self.center_stack.add_named(scroll_win, "posts_view")"""
        #

        






        # set default view state
        self.center_stack.set_visible_child_name("welcome_view")



        #self.info_label = Gtk.Label(label="Current Layout: LTR")
        #self.info_label.set_vexpand(True)
        #center_content.append(self.info_label)
        
         
         
        # right-sidebar 
        self.right_sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        #self.right_sidebar.add_css_class("sidebar-panel")
        #self.right_sidebar.set_size_request(340, -1)
        self.right_sidebar.set_hexpand(True)
        self.right_sidebar.set_vexpand(True)
        #self.right_label = Gtk.Label(label="Right")
        #self.right_label.set_margin_top(12)
        #right_sidebar.append(right_label)
        #self.right_sidebar.add_css_class("bg-green")



        #
        inner_split_view = Adw.OverlaySplitView()
        inner_split_view.set_sidebar(left_sidebar)
        inner_split_view.set_content(self.center_stack)
        inner_split_view.set_sidebar_position(Gtk.PackType.START)
        inner_split_view.set_min_sidebar_width(200)

        #
        self.outer_split_view = Adw.OverlaySplitView()
        self.outer_split_view.set_sidebar(self.right_sidebar)
        self.outer_split_view.set_content(inner_split_view)
        self.outer_split_view.set_sidebar_position(Gtk.PackType.END)
        #
        self.outer_split_view.set_min_sidebar_width(340) # 280 or 200 or 320
        # or
        self.outer_split_view.set_max_sidebar_width(360)




        # register
        register_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        register_box.set_valign(Gtk.Align.CENTER)
        register_box.set_halign(Gtk.Align.CENTER)
        register_box.set_size_request(300, -1)
        # register form layout
        register_title = Gtk.Label(label=self.i18n._("register_title") if hasattr(self, 'i18n') else "Welcome")
        register_title.add_css_class("title-1")
        register_title.set_margin_bottom(12)
        self.register_widget(register_title, "label", "register_title")
        register_box.append(register_title)
        # register form input email
        self.input_register_email = Gtk.Entry() #(placeholder_text=self.i18n._("enter_email"))
        self.input_register_email.set_input_purpose(Gtk.InputPurpose.EMAIL)
        self.register_widget(self.input_register_email, "placeholder", "enter_email")
        register_box.append(self.input_register_email)

        # register form input password
        self.input_register_pass = Gtk.Entry(placeholder_text=self.i18n._("enter_password"))
        self.input_register_pass.set_visibility(False)
        self.input_register_pass.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        self.register_widget(self.input_register_pass, "placeholder", "enter_password")
        register_box.append(self.input_register_pass)

        # register button
        self.register_btn = Gtk.Button() #(label="login_title")
        self.register_widget(self.register_btn, "label", "btn_register")
        self.register_btn.add_css_class("suggested-action")
        #self.register_btn.add_css_class("register_btn")
        self.register_btn.set_margin_top(8)
        self.register_btn.connect("clicked", self.on_register_button_clicked)
        register_box.append(self.register_btn)
        # link to switch to login screen layout
        to_login_btn = Gtk.Button()
        to_login_btn.set_has_frame(False)
        to_login_btn.set_margin_top(4)
        self.register_widget(to_login_btn, "label", "switch_to_login")
        to_login_btn.connect("clicked", lambda x: self.auth_nav_stack.set_visible_child_name("login_screen_layout"))
        register_box.append(to_login_btn)


       


        # login
        login_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        login_box.set_valign(Gtk.Align.CENTER)
        login_box.set_halign(Gtk.Align.CENTER)
        login_box.set_size_request(300, -1)
        # login form layout
        login_title = Gtk.Label(label=self.i18n._("login_title") if hasattr(self, 'i18n') else "Welcome Back")
        login_title.add_css_class("title-1")
        login_title.set_margin_bottom(12)
        self.register_widget(login_title, "label", "login_title")
        login_box.append(login_title)
        # login form input email
        self.input_login_email = Gtk.Entry() #(placeholder_text=self.i18n._("enter_email"))
        self.input_login_email.set_input_purpose(Gtk.InputPurpose.EMAIL)
        self.register_widget(self.input_login_email, "placeholder", "enter_email")
        login_box.append(self.input_login_email)

        # login form input password
        self.input_login_pass = Gtk.Entry(placeholder_text=self.i18n._("enter_password"))
        self.input_login_pass.set_visibility(False)
        self.input_login_pass.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        self.register_widget(self.input_login_pass, "placeholder", "enter_password")
        login_box.append(self.input_login_pass)

        # login button
        #self.login_btn = Gtk.Button(label=self.i18n._("login_title"))
        self.login_btn = Gtk.Button() #(label="login_title")
        self.register_widget(self.login_btn, "label", "login_title")
        self.login_btn.add_css_class("suggested-action")
        #self.login_btn.add_css_class("login_btn")
        self.login_btn.set_margin_top(8)
        self.login_btn.connect("clicked", self.on_login_button_clicked)
        login_box.append(self.login_btn)
        
        # link to switch to register screen layout
        to_register_btn = Gtk.Button()
        to_register_btn.set_has_frame(False)
        to_register_btn.set_margin_top(4)
        self.register_widget(to_register_btn, "label", "switch_to_register")
        to_register_btn.connect("clicked", lambda x: self.auth_nav_stack.set_visible_child_name("register_screen_layout"))
        login_box.append(to_register_btn)

        # stacks
        # 1. auth stack
        self.auth_nav_stack = Gtk.Stack()
        self.auth_nav_stack.add_named(login_box, "login_screen_layout")
        self.auth_nav_stack.add_named(register_box, "register_screen_layout")
        # active layout in auth stack is login_screen_layout
        self.auth_nav_stack.set_visible_child_name("register_screen_layout")




        # 2. root nav stack
        self.root_navigation_stack = Gtk.Stack()
        self.root_navigation_stack.set_transition_type(Gtk.StackTransitionType.NONE)
        #self.root_navigation_stack.add_named(login_box, "login_screen_layout")
        self.root_navigation_stack.add_named(self.auth_nav_stack, "auth_layout")
        self.root_navigation_stack.add_named(self.outer_split_view, "main_layout")
        #self.root_navigation_stack.set_visible_child_name("login_screen_layout")


        #
        self.toast_overlay = Adw.ToastOverlay()
        self.toast_overlay.set_child(self.root_navigation_stack)
       
        



        #
        toolbar_view.set_content(self.toast_overlay)
        #toolbar_view.set_content(self.root_navigation_stack)
        self.win.set_content(toolbar_view)
        #win.set_content(box)
        
        self.win.present()


    def on_login_button_clicked(self, button):
        email = self.input_login_email.get_text().strip()
        password = self.input_login_pass.get_text().strip()

        if not email or not password:
            print("Authentication Failure Email or Password is incorrect")
            self.isLogin = False
            self.logout_btn.set_visible(False)
            failure_msg = self.i18n._("login_failure_msg") if hasattr(self, 'i18n') else "Login failed: Email and password fields cannot be empty."
            failure_toast = Adw.Toast.new(failure_msg)
            failure_toast.set_timeout(3)
            self.toast_overlay.add_toast(failure_toast)
            return
        #
        self.isLogin = True
        self.logout_btn.set_visible(True)
        #self.logout_action.set_enabled(True)
        self.root_navigation_stack.set_visible_child_name("main_layout")

        self.input_login_email.set_text("")
        self.input_login_pass.set_text("")
        #
        print("Layout interface canvas unlocked.")
        #
        success_message = self.i18n._("login_success_msg") if hasattr(self, 'i18n') else "Login successul! Welcome back."
        toast = Adw.Toast.new(success_message)
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)
        #
        #self.menu.append("Logout", "app.logout")
        #self.rebuild_menu()
        GLib.idle_add(self.rebuild_menu)
        #
        self.fire_notify("Mein Gnome Login", 
                         "Login in success for Mein Gnome App!")

    def on_register_button_clicked(self, button):
        email = self.input_register_email.get_text().strip()
        password = self.input_register_pass.get_text().strip()

        if not email or not password:
            print("Authentication Register Failure Email or Password is incorrect")
            #self.isLogin = False
            #self.logout_btn.set_visible(False)
            failure_msg = self.i18n._("register_failure_msg") if hasattr(self, 'i18n') else "Register failed: Email and password fields cannot be empty."
            failure_toast = Adw.Toast.new(failure_msg)
            failure_toast.set_timeout(3)
            self.toast_overlay.add_toast(failure_toast)
            return
        #
        #
        #self.isLogin = True
        #self.logout_btn.set_visible(True)
        #self.logout_action.set_enabled(True)
        self.root_navigation_stack.set_visible_child_name("login_screen_layout")

        self.input_register_email.set_text("")
        self.input_register_pass.set_text("")
        #
        print("Layout interface canvas unlocked.")
        #
        success_message = self.i18n._("register_success_msg") if hasattr(self, 'i18n') else "Register successul! Welcome."
        toast = Adw.Toast.new(success_message)
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)
        #
        #self.menu.append("Logout", "app.logout")
        #self.rebuild_menu()
        #GLib.idle_add(self.rebuild_menu)

            
    def on_logout_button_clicked(self, button):
        self.isLogin = False
        
        #
        if hasattr(self, 'root_navigation_stack'):
            self.root_navigation_stack.set_visible_child_name("auth_layout")
            #self.auth_nav_stack.set_visible_child_name("login_screen_layout")
            print("Session cleared. Interface state locked back to login")
        self.logout_btn.set_visible(False)
        GLib.idle_add(self.rebuild_menu)
        self.fire_notify("Gnome App","Logout is success!")


    




    
    # handle css
    def apply_custom_styles(self):
        css_data = b"""
                    .custom-topbar {
                background-color: #1a3a5f;
                color: #ffffff;
            }

            .custom-topbar windowcontrols button {
                color: #ffffff;
            }

            .sidebar-panel {
                background-color: #e0e0e0;
                border-left: 1px solid #cccccc;
                border-right: 1px solid #cccccc;
            }

            .custom-view-switcher-bg {
                background-color: #d0e1f9;
                border-bottom: 1px solid #b0c4de;
                transition: all 200ms ease;
                /*padding: 6px 0px;*/
                /*border-bottom: 1px solid #b0c4de;*/
            }

            .view-switcher-rtl {
               padding: 6px;
            }

            .view-switcher-rtl label{
               font-size: 11px;
               font-weight: bold;
               wrap: true;
               text-wrap: wrap;
               text-align: center;
            }

            .view-switcher-ltr {
               padding: 6px 0px;
            }

            splitview>box:last-child {
                background-color: #cfd8dc;
                border-left: 1px solid #b0bec5;

            }

            .dim-label {
                opacity: 0.7;
            }

            .bg-green {
                background-color: green;
            }

            .user-card {
                background-color: green;
            }

            toastoverlay > widget {
                valign: start;
                margin-top: 12px;
            }

            .boxed-list {
                margin-bottom: 12px;
            }

            /* Target the text view widget class and its inner C-level text canvas node natively */
            .monospace textview,
            .monospace textview text {
                /* FIX: Changed letter 'l' to number '1' to create a valid dark charcoal color */
                /*background-color: #1e1e1e;*/
                
                /* Clean cream-white typography style for terminal visibility */
               /* color: #dfdbd2;*/
            }

            .monospace textview text {
              /* background-color: #1e1e1e;*/
            }

            .monospace  {
                background-color: #1e1e1e;
                color: #ff5555; /*#dfdbd2;*/
            }

            .prompt {
              padding: 5px;
               /*border: 2px solid red;*/
                border-radius: 15px;
            }

            .login_btn {
                /*background-color: #fd0000;*/
            }




        

        """
        # create css provider
        
        #css_provider.load_from_data(css_data)

        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_file_path = os.path.join(current_dir, "style.css")

        css_provider = Gtk.CssProvider()

        try:
            #css_provider.load_from_data(css_file_path)  
            css_provider.load_from_data(css_data)
            #
            # attach css provider globally
            display = Gdk.Display.get_default()
            if display:
                Gtk.StyleContext.add_provider_for_display(
                    display,
                    css_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
            print(f"css file loaded successfully: {css_file_path} {css_provider}")

        except Exception as e:
            print(f"Error loading css file from disk: {e}")



    def on_sidebar_search_changed(self, entry):
        print("on_sidebar_search_changed")

        search_query = entry.get_text().strip().lower()
        print(f"Active search query: {search_query}")

        active_view_name = self.center_stack.get_visible_child_name()

        print(f"active view name: {active_view_name}")

        if active_view_name == "local_view":
            print(f"local data: {self.local_items_group.get_title()}")
            print(f"local_items_storage: {self.local_items_storage}")
            #self.filter_visible_rows(search_query)
            self.filter_local_items_storage(search_query)

           
        elif active_view_name == "disk_view":
             print("disk_view")
             print(f"disk data: {self.disk_items_group.get_title()}")
             print(f"disk_items_storage: {self.disk_items_storage}")
             self.filter_disk_items_storage(search_query)
        

        elif active_view_name == "local_test_users_view":
            print("local_test_users_view")
            print(f"local_users_items: {self.local_users_items}")
            self.filter_users(search_query)

        elif active_view_name == "local_test_posts_view":
            print("local_test_posts_view")
            print(f"local_posts_items: {self.local_posts_items}")
            self.filter_posts(search_query)

        elif active_view_name == "local_test_todos_view":
            print("local_test_todos_view")
            print(f"local_todos_items: {self.local_todos_items}")
            self.filter_todos(search_query)

        elif active_view_name == "local_test_view":
            print("local_test_view")
            print(f"test_items: {self.test_items}")
            self.filter_test_items(search_query)




            
    def filter_local_items_storage(self, query):
            if not self.local_items_storage:
                print("Cannot search because no data!")
                return
            filtered_data = []
            for item in self.local_items_storage:
                name = item.get("name", "").lower()
                description = item.get("description", "").lower()
                #
                if query in name or query in description:
                    filtered_data.append(item)

            
            if not filtered_data:
                return False
            
            self.display_local_filtered_results(filtered_data)
            
           

            print(f"Memory filter match loop complete, Rendering {len(filtered_data)} matches")

        
    def filter_disk_items_storage(self, query):
            if not self.disk_items_storage:
                print("Cannot search because no data!")
                return
            filtered_data = []
            for item in self.disk_items_storage:
                name = item.get("name", "").lower()
                description = item.get("description", "").lower()
                #
                if query in name or query in description:
                    filtered_data.append(item)

            
            if not filtered_data:
                return False
            
            self.display_disk_filtered_results(filtered_data)
            
           

            print(f"Memory filter match loop complete, Rendering {len(filtered_data)} matches")


    def filter_test_items(self, query):
            if not self.test_items:
                print("Cannot search because no data!")
                return
            filtered_data = []
            for item in self.test_items:
                title = item.get("title", "").lower()
                author = item.get("author", "").lower()
                year = str(item.get("year", 0))
                #
                if query in title or query in author or query in year:
                    filtered_data.append(item)

            
            if not filtered_data:
                return False
            
            self.display_test_filtered_results(filtered_data)
            
           

            print(f"Memory filter match loop complete, Rendering {len(filtered_data)} matches")

    def filter_users(self, query):
            if not self.local_users_items:
                print("Cannot search because no data!")
                return
            filtered_data = []
            for item in self.local_users_items:
                name = item.get("name", "").lower()
                email = item.get("email", "").lower()
                #year = str(item.get("year", 0))
                #
                if query in name or query in email:
                    filtered_data.append(item)

            
            if not filtered_data:
                return False
            
            self.display_users_filtered_results(filtered_data)
            
           

            print(f"Memory filter match loop complete, Rendering {len(filtered_data)} matches")


    def filter_posts(self, query):
            if not self.local_posts_items:
                print("Cannot search because no data!")
                return
            filtered_data = []
            for item in self.local_posts_items:
                title = item.get("title", "").lower()
                body = item.get("body", "").lower()
                #
                if query in title or query in body:
                    filtered_data.append(item)

            
            if not filtered_data:
                return False
            
            self.display_posts_filtered_results(filtered_data)
            
           

            print(f"Memory filter match loop complete, Rendering {len(filtered_data)} matches")

    def filter_todos(self, query):
            if not self.local_todos_items:
                print("Cannot search because no data!")
                return
            filtered_data = []
            for item in self.local_todos_items:
                title = item.get("title", "").lower()
                
                #
                if query in title :
                    filtered_data.append(item)

            
            if not filtered_data:
                return False
            
            self.display_todos_filtered_results(filtered_data)
            
           

            print(f"Memory filter match loop complete, Rendering {len(filtered_data)} matches")




    def display_local_filtered_results(self, filtered_data):
            """ Force-clears the actual UI widget tree directly to wipe old data completely """
            print(f"Executing total interface refresh for {len(filtered_data)} matching records...")

            # =========================================================================
            # 1. BULLETPROOF CLEAR: Clear out EVERYTHING attached inside content_box
            # =========================================================================
            # This climbs out of your group to the parent container box, and completely 
            # flushes every single layout element on screen so duplication is impossible.
            if hasattr(self, 'local_items_group') and self.local_items_group.get_parent():
                content_box = self.local_items_group.get_parent()
                
                # Gather all children in the parent box (including any hidden/duplicate groups)
                box_children = []
                child = content_box.get_first_child()
                while child:
                    box_children.append(child)
                    child = child.get_next_sibling()
                    
                # Wipe the slate entirely blank
                for box_child in box_children:
                    content_box.remove(box_child)
                    
                # Recreate a fresh, clean preferences group container on the empty box canvas
                self.local_items_group = Adw.PreferencesGroup()
                self.local_items_group.set_title("Stored Local Entries")
                content_box.append(self.local_items_group)

            # -------------------------------------------------------------------------
            # Case A: Search yielded no matches or storage is empty
            # -------------------------------------------------------------------------
            if not filtered_data:
                # Re-create empty placeholder label text dynamically
                self.empty_list_lbl = Gtk.Label(label="No recorded items match your search criteria.")
                self.empty_list_lbl.add_css_class("dim-label")
                self.local_items_group.add(self.empty_list_lbl)
                self.center_stack.set_visible_child_name("local_view")
                return

            # -------------------------------------------------------------------------
            # Case B: Matches found, draw brand-new ActionRow cards on the clean layout
            # -------------------------------------------------------------------------
            for item in filtered_data:
                row = Adw.ActionRow()
                row.set_title(item.get("name", "Unknown Entry"))
                row.set_subtitle(item.get("description", "No Description Available"))
                row.set_margin_bottom(8)
                
                row.user_data_payload = item

                # Include a clean package icon indicator to the left
                card_icon = Gtk.Image.new_from_icon_name("package-x-generic-symbolic")
                row.add_prefix(card_icon)
                
                # Append card row item straight to your freshly cleared group field
                self.local_items_group.add(row)

            # Force layout refresh and switch focus state
            self.local_items_group.set_visible(True)
            
            def force_stack_transition():
                self.center_stack.set_visible_child_name("local_view")
                return False

            GLib.idle_add(force_stack_transition)
      
    def display_disk_filtered_results(self, filtered_data):
            """ Force-clears the actual UI widget tree directly to wipe old data completely """
            print(f"Executing total interface refresh for {len(filtered_data)} matching records...")

            # =========================================================================
            # 1. BULLETPROOF CLEAR: Clear out EVERYTHING attached inside content_box
            # =========================================================================
            # This climbs out of your group to the parent container box, and completely 
            # flushes every single layout element on screen so duplication is impossible.
            if hasattr(self, 'disk_items_group') and self.disk_items_group.get_parent():
                content_box = self.disk_items_group.get_parent()
                
                # Gather all children in the parent box (including any hidden/duplicate groups)
                box_children = []
                child = content_box.get_first_child()
                while child:
                    box_children.append(child)
                    child = child.get_next_sibling()
                    
                # Wipe the slate entirely blank
                for box_child in box_children:
                    content_box.remove(box_child)
                    
                # Recreate a fresh, clean preferences group container on the empty box canvas
                self.disk_items_group = Adw.PreferencesGroup()
                self.disk_items_group.set_title("Stored Disk Entries")
                content_box.append(self.disk_items_group)

            # -------------------------------------------------------------------------
            # Case A: Search yielded no matches or storage is empty
            # -------------------------------------------------------------------------
            if not filtered_data:
                # Re-create empty placeholder label text dynamically
                self.empty_list_lbl = Gtk.Label(label="No recorded items match your search criteria.")
                self.empty_list_lbl.add_css_class("dim-label")
                self.disk_items_group.add(self.empty_list_lbl)
                self.center_stack.set_visible_child_name("disk_view")
                return

            # -------------------------------------------------------------------------
            # Case B: Matches found, draw brand-new ActionRow cards on the clean layout
            # -------------------------------------------------------------------------
            for item in filtered_data:
                row = Adw.ActionRow()
                row.set_title(item.get("name", "Unknown Entry"))
                row.set_subtitle(item.get("description", "No Description Available"))
                row.set_margin_bottom(8)
                
                row.user_data_payload = item

                # Include a clean package icon indicator to the left
                card_icon = Gtk.Image.new_from_icon_name("package-x-generic-symbolic")
                row.add_prefix(card_icon)
                
                # Append card row item straight to your freshly cleared group field
                self.disk_items_group.add(row)

            # Force layout refresh and switch focus state
            self.disk_items_group.set_visible(True)
            
            def force_stack_transition():
                self.center_stack.set_visible_child_name("disk_view")
                return False

            GLib.idle_add(force_stack_transition)

    def display_test_filtered_results(self, filtered_data):
            """ Force-clears the actual UI widget tree directly to wipe old data completely """
            print(f"Executing total interface refresh for {len(filtered_data)} matching records...")

            # =========================================================================
            # 1. BULLETPROOF CLEAR: Clear out EVERYTHING attached inside content_box
            # =========================================================================
            # This climbs out of your group to the parent container box, and completely 
            # flushes every single layout element on screen so duplication is impossible.
            if hasattr(self, 'test_items_group') and self.test_items_group.get_parent():
                content_box = self.test_items_group.get_parent()
                
                # Gather all children in the parent box (including any hidden/duplicate groups)
                box_children = []
                child = content_box.get_first_child()
                while child:
                    box_children.append(child)
                    child = child.get_next_sibling()
                    
                # Wipe the slate entirely blank
                for box_child in box_children:
                    content_box.remove(box_child)
                    
                # Recreate a fresh, clean preferences group container on the empty box canvas
                self.test_items_group = Adw.PreferencesGroup()
                self.test_items_group.set_title("Test Entries")
                content_box.append(self.test_items_group)

            # -------------------------------------------------------------------------
            # Case A: Search yielded no matches or storage is empty
            # -------------------------------------------------------------------------
            if not filtered_data:
                # Re-create empty placeholder label text dynamically
                self.empty_list_lbl = Gtk.Label(label="No recorded items match your search criteria.")
                self.empty_list_lbl.add_css_class("dim-label")
                self.test_items_group.add(self.empty_list_lbl)
                self.center_stack.set_visible_child_name("disk_view")
                return

            # -------------------------------------------------------------------------
            # Case B: Matches found, draw brand-new ActionRow cards on the clean layout
            # -------------------------------------------------------------------------
            for item in filtered_data:
                row = Adw.ActionRow()
                row.set_title(item.get("title", "Unknown Title"))
                row.set_subtitle(item.get("author", "No Author Available"))
                row.set_subtitle(str(item.get("year", "0000")))
                row.set_margin_bottom(8)
                
                row.user_data_payload = item

                # Include a clean package icon indicator to the left
                card_icon = Gtk.Image.new_from_icon_name("package-x-generic-symbolic")
                row.add_prefix(card_icon)
                
                # Append card row item straight to your freshly cleared group field
                self.test_items_group.add(row)

            # Force layout refresh and switch focus state
            self.test_items_group.set_visible(True)
            
            def force_stack_transition():
                self.center_stack.set_visible_child_name("local_test_view")
                return False

            GLib.idle_add(force_stack_transition)

    def display_users_filtered_results(self, filtered_data):
            """ Force-clears the actual UI widget tree directly to wipe old data completely """
            print(f"Executing total interface refresh for {len(filtered_data)} matching records...")

            # =========================================================================
            # 1. BULLETPROOF CLEAR: Clear out EVERYTHING attached inside content_box
            # =========================================================================
            # This climbs out of your group to the parent container box, and completely 
            # flushes every single layout element on screen so duplication is impossible.
            if hasattr(self, 'local_users_group') and self.local_users_group.get_parent():
                content_box = self.local_users_group.get_parent()
                
                # Gather all children in the parent box (including any hidden/duplicate groups)
                box_children = []
                child = content_box.get_first_child()
                while child:
                    box_children.append(child)
                    child = child.get_next_sibling()
                    
                # Wipe the slate entirely blank
                for box_child in box_children:
                    content_box.remove(box_child)
                    
                # Recreate a fresh, clean preferences group container on the empty box canvas
                self.local_users_group = Adw.PreferencesGroup()
                self.local_users_group.set_title("Test Entries")
                content_box.append(self.local_users_group)

            # -------------------------------------------------------------------------
            # Case A: Search yielded no matches or storage is empty
            # -------------------------------------------------------------------------
            if not filtered_data:
                # Re-create empty placeholder label text dynamically
                self.empty_list_lbl = Gtk.Label(label="No recorded items match your search criteria.")
                self.empty_list_lbl.add_css_class("dim-label")
                self.local_users_group.add(self.empty_list_lbl)
                self.center_stack.set_visible_child_name("local_test_users_view")
                return

            # -------------------------------------------------------------------------
            # Case B: Matches found, draw brand-new ActionRow cards on the clean layout
            # -------------------------------------------------------------------------

            def card_clicked(row):
                print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                #
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("name"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.right_sidebar.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("email"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                self.right_sidebar.append(body_label)
                #
                sidebar_group = Adw.PreferencesGroup()
                sidebar_group.set_title("User Information")

                #
                username_row = Adw.ActionRow(title="Username", subtitle=item.get("username", "N/A"))
                sidebar_group.add(username_row)
                #
                web_row = Adw.ActionRow(title="Website", subtitle=item.get("website", "N/A"))
                sidebar_group.add(web_row)
                #
                company_name = item.get("company", {}).get("name", "N/A")
                company_row = Adw.ActionRow(title="Company", subtitle=company_name)
                sidebar_group.add(company_row)

                #
                city_name = item.get("address", {}).get("city", "N/A")
                city_row = Adw.ActionRow(title="City", subtitle=city_name)
                sidebar_group.add(city_row)

                # inject the completed data card into right-sidebar
                self.right_sidebar.append(sidebar_group)
                #
                sidebar_group.set_margin_start(8)
                sidebar_group.set_margin_end(8)


            for item in filtered_data:
                row = Adw.ActionRow()
                row.set_title(item.get("name", "Unknown Name"))
                row.set_subtitle(item.get("email", "No Author Email"))
                #row.set_subtitle(str(item.get("year", "0000")))
                row.set_margin_bottom(8)
                
                row.payload = item

                row.set_activatable(True)
                row.payload = item
                row.connect("activated", self.user_card_clicked)


                

                # Include a clean package icon indicator to the left
                card_icon = Gtk.Image.new_from_icon_name("package-x-generic-symbolic")
                row.add_prefix(card_icon)
                
                # Append card row item straight to your freshly cleared group field
                self.local_users_group.add(row)

            # Force layout refresh and switch focus state
            self.local_users_group.set_visible(True)
            
            def force_stack_transition():
                self.center_stack.set_visible_child_name("local_test_users_view")
                return False

            GLib.idle_add(force_stack_transition)

    def display_posts_filtered_results(self, filtered_data):
            """ Force-clears the actual UI widget tree directly to wipe old data completely """
            print(f"Executing total interface refresh for {len(filtered_data)} matching records...")

            # =========================================================================
            # 1. BULLETPROOF CLEAR: Clear out EVERYTHING attached inside content_box
            # =========================================================================
            # This climbs out of your group to the parent container box, and completely 
            # flushes every single layout element on screen so duplication is impossible.
            if hasattr(self, 'local_posts_group') and self.local_posts_group.get_parent():
                content_box = self.local_posts_group.get_parent()
                
                # Gather all children in the parent box (including any hidden/duplicate groups)
                box_children = []
                child = content_box.get_first_child()
                while child:
                    box_children.append(child)
                    child = child.get_next_sibling()
                    
                # Wipe the slate entirely blank
                for box_child in box_children:
                    content_box.remove(box_child)
                    
                # Recreate a fresh, clean preferences group container on the empty box canvas
                self.local_posts_group = Adw.PreferencesGroup()
                self.local_posts_group.set_title("Posts Entries")
                content_box.append(self.local_posts_group)

            # -------------------------------------------------------------------------
            # Case A: Search yielded no matches or storage is empty
            # -------------------------------------------------------------------------
            if not filtered_data:
                # Re-create empty placeholder label text dynamically
                self.empty_list_lbl = Gtk.Label(label="No recorded items match your search criteria.")
                self.empty_list_lbl.add_css_class("dim-label")
                self.local_posts_group.add(self.empty_list_lbl)
                self.center_stack.set_visible_child_name("local_test_users_view")
                return

            # -------------------------------------------------------------------------
            # Case B: Matches found, draw brand-new ActionRow cards on the clean layout
            # -------------------------------------------------------------------------

           # Context-isolated click row callback handler
            def card_clicked(row):
                print(f"card_clicked: {row.payload}")
                item = row.payload

                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                
                main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
                main_box.set_margin_start(8)
                main_box.set_margin_end(8)
                main_box.set_vexpand(True)

                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") 
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                title_label.set_wrap(True)
                main_box.append(title_label)
                
                body_label = Gtk.Label(label=item.get("body"))
                body_label.add_css_class("dim-label") 
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                main_box.append(body_label)
                
                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_margin_bottom(12)
                main_box.append(separator)
                
                comments_label = Gtk.Label(label="Comments")
                comments_label.add_css_class("heading")
                comments_label.set_halign(Gtk.Align.START)
                comments_label.set_margin_bottom(8)
                main_box.append(comments_label)

                self.build_test_comments_by_postId_view(main_box, item.get("id"))

                self.right_sidebar.append(main_box)
                self.right_sidebar.set_vexpand(True)
                self.right_sidebar.set_hexpand(False)

            # Thread-safe function to build individual rows onto the UI loop
            # Thread-safe function to build individual rows onto the UI loop
            def populate_ui_cards(posts_data):
                print("Populating UI cards cleanly...")

                # =========================================================================
                # 1. BULLETPROOF CLEAR: Clear out EVERYTHING attached inside content_box
                # =========================================================================
                # This climbs out of your group to the parent container box, and completely 
                # flushes every single layout element on screen so duplication or warnings are impossible.
                if hasattr(self, 'local_posts_group') and self.local_posts_group.get_parent():
                    content_box = self.local_posts_group.get_parent()
                    
                    # Gather all children in the parent box safely
                    box_children = []
                    child = content_box.get_first_child()
                    while child:
                        box_children.append(child)
                        child = child.get_next_sibling()
                        
                    # Wipe the slate entirely blank
                    for box_child in box_children:
                        content_box.remove(box_child)
                        
                    # Recreate a fresh, clean preferences group container on the empty box canvas
                    self.local_posts_group = Adw.PreferencesGroup()
                    self.local_posts_group.set_title("Posts#")
                    content_box.append(self.local_posts_group)

                # -------------------------------------------------------------------------
                # 2. POPULATE CARDS: Draw brand-new ActionRow cards on the clean layout
                # -------------------------------------------------------------------------
                for item in posts_data:
                    self.local_posts_items.append(item)
                    card = Adw.ActionRow()
                    card.set_title(item.get("title", "test"))
                    card.set_subtitle(item.get("body", "test"))
                    card.set_activatable(True)
                    
                    # Bind item payload context directly to row object
                    card.payload = item
                    card.connect("activated", card_clicked)
                    
                    card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                    self.local_posts_group.add(card)
                
                # Force layout refresh and switch focus state
                self.local_posts_group.set_visible(True)
                self.local_posts_group.queue_resize()
                return False



            populate_ui_cards(filtered_data)

            """for item in filtered_data:
                row = Adw.ActionRow()
                row.set_title(item.get("title", "Unknown Title"))
                row.set_subtitle(item.get("body", "No Author Body"))
                #row.set_subtitle(str(item.get("year", "0000")))
                row.set_margin_bottom(8)
                
                row.payload = item

                row.set_activatable(True)
                row.payload = item
                #row.connect("activated", self.post_card_clicked)


                

                # Include a clean package icon indicator to the left
                card_icon = Gtk.Image.new_from_icon_name("package-x-generic-symbolic")
                row.add_prefix(card_icon)
                
                # Append card row item straight to your freshly cleared group field
                self.local_posts_group.add(row)"""

            # Force layout refresh and switch focus state
            self.local_posts_group.set_visible(True)
            
            def force_stack_transition():
                self.center_stack.set_visible_child_name("local_test_posts_view")
                return False

            GLib.idle_add(force_stack_transition)

    def display_todos_filtered_results(self, filtered_data):
            """ Force-clears the actual UI widget tree directly to wipe old data completely """
            print(f"Executing total interface refresh for {len(filtered_data)} matching records...")

            # =========================================================================
            # 1. BULLETPROOF CLEAR: Clear out EVERYTHING attached inside content_box
            # =========================================================================
            # This climbs out of your group to the parent container box, and completely 
            # flushes every single layout element on screen so duplication is impossible.
            if hasattr(self, 'local_todos_group') and self.local_todos_group.get_parent():
                content_box = self.local_todos_group.get_parent()
                
                # Gather all children in the parent box (including any hidden/duplicate groups)
                box_children = []
                child = content_box.get_first_child()
                while child:
                    box_children.append(child)
                    child = child.get_next_sibling()
                    
                # Wipe the slate entirely blank
                for box_child in box_children:
                    content_box.remove(box_child)
                    
                # Recreate a fresh, clean preferences group container on the empty box canvas
                self.local_todos_group = Adw.PreferencesGroup()
                self.local_todos_group.set_title("Todos Entries")
                content_box.append(self.local_todos_group)

            # -------------------------------------------------------------------------
            # Case A: Search yielded no matches or storage is empty
            # -------------------------------------------------------------------------
            if not filtered_data:
                # Re-create empty placeholder label text dynamically
                self.empty_list_lbl = Gtk.Label(label="No recorded items match your search criteria.")
                self.empty_list_lbl.add_css_class("dim-label")
                self.local_todos_group.add(self.empty_list_lbl)
                self.center_stack.set_visible_child_name("local_test_todos_view")
                return

            # -------------------------------------------------------------------------
            # Case B: Matches found, draw brand-new ActionRow cards on the clean layout
            # -------------------------------------------------------------------------

            def card_clicked(row):
                print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                #
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.right_sidebar.append(title_label)
                #


            for item in filtered_data:
                row = Adw.ActionRow()
                row.set_title(item.get("title", "Unknown Title"))
                #row.set_subtitle(item.get("author", "No Author Available"))
                #row.set_subtitle(str(item.get("year", "0000")))
                row.set_margin_bottom(8)
                
                row.payload = item
                row.set_activatable(True)
                row.connect("activated", card_clicked)

                # Include a clean package icon indicator to the left
                card_icon = Gtk.Image.new_from_icon_name("package-x-generic-symbolic")
                row.add_prefix(card_icon)
                
                # Append card row item straight to your freshly cleared group field
                self.local_todos_group.add(row)

            # Force layout refresh and switch focus state
            self.local_todos_group.set_visible(True)
            
            def force_stack_transition():
                self.center_stack.set_visible_child_name("local_test_todos_view")
                return False

            GLib.idle_add(force_stack_transition)

    # cards clicked


    def user_card_clicked(self, row):
                print(f"user_card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                #
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("name"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.right_sidebar.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("email"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                self.right_sidebar.append(body_label)
                #
                sidebar_group = Adw.PreferencesGroup()
                sidebar_group.set_title("User Information")

                #
                username_row = Adw.ActionRow(title="Username", subtitle=item.get("username", "N/A"))
                sidebar_group.add(username_row)
                #
                web_row = Adw.ActionRow(title="Website", subtitle=item.get("website", "N/A"))
                sidebar_group.add(web_row)
                #
                company_name = item.get("company", {}).get("name", "N/A")
                company_row = Adw.ActionRow(title="Company", subtitle=company_name)
                sidebar_group.add(company_row)

                #
                city_name = item.get("address", {}).get("city", "N/A")
                city_row = Adw.ActionRow(title="City", subtitle=city_name)
                sidebar_group.add(city_row)

                # inject the completed data card into right-sidebar
                self.right_sidebar.append(sidebar_group)
                #
                sidebar_group.set_margin_start(8)
                sidebar_group.set_margin_end(8)

    def post_card_clicked(self, row):
                print(f"post_card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                #
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                #
                # Create a container for all content (to maintain proper layout)
                main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
                main_box.set_margin_start(8)
                main_box.set_margin_end(8)
                main_box.set_vexpand(True)  # Allow the main box to expand vertically

                #
                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                #self.right_sidebar.append(title_label)
                main_box.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("body"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                #self.right_sidebar.append(body_label)
                main_box.append(body_label)
                # Add a separator
                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_margin_bottom(12)
                main_box.append(separator)
                # Add comments section with scrolling
                comments_label = Gtk.Label(label="Comments")
                comments_label.add_css_class("heading")
                comments_label.set_halign(Gtk.Align.START)
                comments_label.set_margin_bottom(8)
                main_box.append(comments_label)

                # calling fetch comments
                self.build_test_comments_by_postId_view(main_box, item.get("id"))

                # Add everything to the sidebar
                self.right_sidebar.append(main_box)
                self.right_sidebar.set_vexpand(True)
                self.right_sidebar.set_hexpand(False)  # Keep horizontal expansion off


    # builds

    #
    def build_test_view(self):
        #
        print(f"state#: {self.state}")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False) 
        local_title = Gtk.Label(label="test Manager")
        local_title.add_css_class("heading")
        local_action_bar.set_title_widget(local_title)

        local_wrapper.add_top_bar(local_action_bar)


        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)

        #self.test_items_group = Adw.PreferencesGroup()
        self.test_items_group.set_title("test ui")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(self.test_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.center_stack.add_named(local_wrapper, "local_test_view")

        #handle = self.handle_json_file()


        #docs = []   


        def test_fetch():
            print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            
            """file_path = os.path.join(GLib.get_current_dir(), "./data/test.json")

            if not os.path.exists(file_path):
                print("no json file")
                return False
            
            print("json file exists!")"""

            def card_clicked(row):
                print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                #
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.right_sidebar.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("author"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                self.right_sidebar.append(body_label)
                #
                print(f"item year: {item.get("year")}")
                year_label = Gtk.Label(label=str(item.get("year", 0)))
                year_label.add_css_class("dim-label") # built-in font bold
                year_label.set_margin_bottom(24)
                year_label.set_halign(Gtk.Align.START)
                year_label.set_wrap(True)
                self.right_sidebar.append(year_label)
                #sidebar_group = Adw.PreferencesGroup()
                #sidebar_group.set_title("User Information")

               
                # inject the completed data card into right-sidebar
                #self.right_sidebar.append(sidebar_group)
                #
                #sidebar_group.set_margin_start(8)
                #sidebar_group.set_margin_end(8)



            def populate_ui_cards(test_data):
                for item in test_data:
                        #print(f"item: {item}")
                        #docs.append(item)
                        self.test_items.append(item)
                        card = Adw.ActionRow()
                        card.set_title(item.get("title", "test"))
                        card.set_subtitle(item.get("author", "test"))
                        card.set_subtitle(str(item.get("year", 0)))
                        card.set_activatable(True)
                        card.payload = item
                        card.connect("activated", card_clicked)
                        card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                        self.test_items_group.add(card)
                    
                    # --- ACTION TAKEN HERE ---
                    # Now that docs is populated, safely trigger your UI updates or prints:
                    #print(f"len docs inside callback: {len(docs)}")

                self.test_items_group.queue_resize()
            

            #self.read_json_file(populate_ui_cards, "data", "test")
            self.handle_json_file.read_json_file(populate_ui_cards, "data", "test")
            #print(f"read_json: {data}")
            #
            
            

            """try:
                success, content = GLib.file_get_contents(file_path)

                if success:
                    if isinstance(content, bytes):
                        content = content.decode("utf-8")
                        
                    data = json.loads(content)
                    print(f"data size: {len(data)}")
                    
                    for item in data:
                        print(f"item: {item}")
                        #docs.append(item)
                        self.test_items.append(item)
                        card = Adw.ActionRow()
                        card.set_title(item.get("title", "test"))
                        card.set_subtitle(item.get("author", "test"))
                        card.set_subtitle(str(item.get("year", 0)))
                        card.set_activatable(True)
                        card.payload = item
                        card.connect("activated", card_clicked)
                        card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                        self.test_items_group.add(card)
                    
                    # --- ACTION TAKEN HERE ---
                    # Now that docs is populated, safely trigger your UI updates or prints:
                    #print(f"len docs inside callback: {len(docs)}")

                    self.test_items_group.queue_resize()
                    
                    

                else:
                    print("GLib failed to read file contents successfully.")
            except Exception as e:
                print(f"ERROR: {e}")"""

            return False # Stop the GLib idle loop from repeating this function
        
        # Queue the function to run as soon as the main loop is ready
        GLib.idle_add(test_fetch)

        


        #content_box.append(local_items_group)
        #scroll_win.set_child(content_box)
        #local_wrapper.set_content(scroll_win)


        #
        #self.center_stack.add_named(local_wrapper, "local_test_view")



    def build_test_users_view(self):
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False) 
        local_title = Gtk.Label(label="Users Management")
        local_title.add_css_class("heading")
        local_action_bar.set_title_widget(local_title)

        local_wrapper.add_top_bar(local_action_bar)


        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)

        #self.local_users_group = Adw.PreferencesGroup()
        self.local_users_group.set_title("Users")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(self.local_users_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.center_stack.add_named(local_wrapper, "local_test_users_view")


        docs = []   


        def test_fetch():
            print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            
            """file_path = os.path.join(GLib.get_current_dir(), "./data/users.json")

            if not os.path.exists(file_path):
                print("no json file")
                return False
            
            print("json file exists!")"""

            def card_clicked(row):
                #print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                #
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("name"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.right_sidebar.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("email"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                self.right_sidebar.append(body_label)
                #
                sidebar_group = Adw.PreferencesGroup()
                sidebar_group.set_title("User Information")

                #
                username_row = Adw.ActionRow(title="Username", subtitle=item.get("username", "N/A"))
                sidebar_group.add(username_row)
                #
                web_row = Adw.ActionRow(title="Website", subtitle=item.get("website", "N/A"))
                sidebar_group.add(web_row)
                #
                company_name = item.get("company", {}).get("name", "N/A")
                company_row = Adw.ActionRow(title="Company", subtitle=company_name)
                sidebar_group.add(company_row)

                #
                city_name = item.get("address", {}).get("city", "N/A")
                city_row = Adw.ActionRow(title="City", subtitle=city_name)
                sidebar_group.add(city_row)

                # inject the completed data card into right-sidebar
                self.right_sidebar.append(sidebar_group)
                #
                sidebar_group.set_margin_start(8)
                sidebar_group.set_margin_end(8)

            def populate_ui_cards(data):
                for item in data:
                        #print(f"item: {item}")
                        #docs.append(item)
                        self.local_users_items.append(item)
                        card = Adw.ActionRow()
                        card.set_title(item.get("name", "test"))
                        card.set_subtitle(item.get("email", "test"))
                        card.set_activatable(True)
                        card.payload = item
                        card.connect("activated", self.user_card_clicked)
                        card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                        self.local_users_group.add(card)
                        #
                    
                    

                self.local_users_group.queue_resize()


            #self.read_json_file(populate_ui_cards, "data", "users")
            self.handle_json_file.read_json_file(populate_ui_cards, "data", "users")

            """try:
                success, content = GLib.file_get_contents(file_path)

                if success:
                    if isinstance(content, bytes):
                        content = content.decode("utf-8")
                        
                    data = json.loads(content)
                    print(f"data size: {len(data)}")
                    
                    for item in data:
                        print(f"item: {item}")
                        #docs.append(item)
                        self.local_users_items.append(item)
                        card = Adw.ActionRow()
                        card.set_title(item.get("name", "test"))
                        card.set_subtitle(item.get("email", "test"))
                        card.set_activatable(True)
                        card.payload = item
                        card.connect("activated", self.user_card_clicked)
                        card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                        self.local_users_group.add(card)
                    
                    # --- ACTION TAKEN HERE ---
                    # Now that docs is populated, safely trigger your UI updates or prints:
                    #print(f"len docs inside callback: {len(docs)}")

                    self.local_users_group.queue_resize()
                    
                    

                else:
                    print("GLib failed to read file contents successfully.")
            except Exception as e:
                print(f"ERROR: {e}")"""

            return False # Stop the GLib idle loop from repeating this function
        
        # Queue the function to run as soon as the main loop is ready
        GLib.idle_add(test_fetch)

    def build_test_posts_view(self):
        #
        print("build_test_posts_view----------------------------------")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False) 
        local_title = Gtk.Label(label="Posts Management#")
        local_title.add_css_class("heading")
        local_action_bar.set_title_widget(local_title)

        local_wrapper.add_top_bar(local_action_bar)


        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)

        local_posts_group = Adw.PreferencesGroup()
        local_posts_group.set_title("Posts#")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(local_posts_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.center_stack.add_named(local_wrapper, "local_test_posts_view")

        card = Adw.ActionRow()
        card.set_title("test")
        card.set_subtitle("test")
        card.set_activatable(True)
        #card.payload = item
        #card.connect("activated", card_clicked)
        card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
        local_posts_group.add(card)
        

        def test_fetch():
            print("test_fetch posts#")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add

            """file_path = os.path.join(GLib.get_current_dir(), "./data/posts.json")

            if not os.path.exists(file_path):
                print("no json file")
                return False
            
            print("json file exists posts!")"""

            def card_clicked(row):
                #print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                #
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                #
                # Create a container for all content (to maintain proper layout)
                main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
                main_box.set_margin_start(8)
                main_box.set_margin_end(8)
                main_box.set_vexpand(True)  # Allow the main box to expand vertically

                #
                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                #self.right_sidebar.append(title_label)
                main_box.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("body"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                #self.right_sidebar.append(body_label)
                main_box.append(body_label)
                # Add a separator
                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_margin_bottom(12)
                main_box.append(separator)
                # Add comments section with scrolling
                comments_label = Gtk.Label(label="Comments")
                comments_label.add_css_class("heading")
                comments_label.set_halign(Gtk.Align.START)
                comments_label.set_margin_bottom(8)
                main_box.append(comments_label)

                # calling fetch comments
                self.build_test_comments_by_postId_view(main_box, item.get("id"))

                # Add everything to the sidebar
                self.right_sidebar.append(main_box)
                self.right_sidebar.set_vexpand(True)
                self.right_sidebar.set_hexpand(False)  # Keep horizontal expansion off

            def populate_ui_cards(data):
                for item in data:
                        #print(f"item post#: {item}")
                        print("------------------------")
                        #docs.append(item)
                        #self.local_posts_items(item)
                        card = Adw.ActionRow()
                        card.set_title(item.get("title", "test"))
                        card.set_subtitle(item.get("body", "test"))
                        #card.set_activatable(True)
                        #card.payload = item
                        #card.connect("activated", card_clicked)
                        card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                        local_posts_group.add(card)
                    
                   
                #
                local_posts_group.queue_resize()

            self.read_json_file(populate_ui_cards, "data", "posts")
                

            """try:
                success, content = GLib.file_get_contents(file_path)

                if success:
                    if isinstance(content, bytes):
                        content = content.decode("utf-8")
                        
                    data = json.loads(content)
                    print(f"data size posts#: {len(data)}")
                    print(f"data posts#: {data(0)}")

                    for item in data:
                        print(f"#item post>>>>>># {item}")
                    
                    for item in data:
                        print(f"item post#: {item}")
                        print("------------------------")
                        #docs.append(item)
                        #self.local_posts_items(item)
                        card = Adw.ActionRow()
                        card.set_title(item.get("title", "test"))
                        card.set_subtitle(item.get("body", "test"))
                        #card.set_activatable(True)
                        #card.payload = item
                        #card.connect("activated", card_clicked)
                        card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                        local_posts_group.add(card)
                    
                    # --- ACTION TAKEN HERE ---
                    # Now that docs is populated, safely trigger your UI updates or prints:
                    #print(f"len docs inside callback: {len(docs)}")

                    local_posts_group.queue_resize()
                    
                    

                else:
                    print("GLib failed to read file contents successfully.")
            except Exception as e:
                print(f"ERROR: {e}")"""

            return False # Stop the GLib idle loop from repeating this function
        
        # Queue the function to run as soon as the main loop is ready
        GLib.idle_add(test_fetch)


    def build_test_posts_view2(self):
        print("build_test_posts_view2----------------------------------")
        
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False) 
        local_title = Gtk.Label(label="Posts Management#")
        local_title.add_css_class("heading")
        local_action_bar.set_title_widget(local_title)

        local_wrapper.add_top_bar(local_action_bar)

        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)

        # Make local_posts_group an instance variable so UI callbacks can access it reliably
        self.local_posts_group = Adw.PreferencesGroup()
        self.local_posts_group.set_title("Posts#")

        content_box.append(self.local_posts_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        self.center_stack.add_named(local_wrapper, "local_test_posts_view")

        # Context-isolated click row callback handler
        def card_clicked(row):
            print(f"card_clicked: {row.payload}")
            item = row.payload

            while child := self.right_sidebar.get_first_child():
                self.right_sidebar.remove(child)
            
            self.right_sidebar.set_margin_top(16)
            self.right_sidebar.set_margin_start(12)
            self.right_sidebar.set_margin_end(12)
            self.right_sidebar.set_margin_bottom(16)
            
            main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            main_box.set_margin_start(8)
            main_box.set_margin_end(8)
            main_box.set_vexpand(True)

            title_label = Gtk.Label(label=item.get("title"))
            title_label.add_css_class("title-1") 
            title_label.set_margin_bottom(12)
            title_label.set_halign(Gtk.Align.START)
            title_label.set_wrap(True)
            main_box.append(title_label)
            
            body_label = Gtk.Label(label=item.get("body"))
            body_label.add_css_class("dim-label") 
            body_label.set_margin_bottom(24)
            body_label.set_halign(Gtk.Align.START)
            body_label.set_wrap(True)
            main_box.append(body_label)
            
            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            separator.set_margin_bottom(12)
            main_box.append(separator)
            
            comments_label = Gtk.Label(label="Comments")
            comments_label.add_css_class("heading")
            comments_label.set_halign(Gtk.Align.START)
            comments_label.set_margin_bottom(8)
            main_box.append(comments_label)

            self.build_test_comments_by_postId_view(main_box, item.get("id"))

            self.right_sidebar.append(main_box)
            self.right_sidebar.set_vexpand(True)
            self.right_sidebar.set_hexpand(False)

        # Thread-safe function to build individual rows onto the UI loop
        # Thread-safe function to build individual rows onto the UI loop
        def populate_ui_cards(posts_data):
            print("Populating UI cards cleanly...")

            # =========================================================================
            # 1. BULLETPROOF CLEAR: Clear out EVERYTHING attached inside content_box
            # =========================================================================
            # This climbs out of your group to the parent container box, and completely 
            # flushes every single layout element on screen so duplication or warnings are impossible.
            if hasattr(self, 'local_posts_group') and self.local_posts_group.get_parent():
                content_box = self.local_posts_group.get_parent()
                
                # Gather all children in the parent box safely
                box_children = []
                child = content_box.get_first_child()
                while child:
                    box_children.append(child)
                    child = child.get_next_sibling()
                    
                # Wipe the slate entirely blank
                for box_child in box_children:
                    content_box.remove(box_child)
                    
                # Recreate a fresh, clean preferences group container on the empty box canvas
                self.local_posts_group = Adw.PreferencesGroup()
                self.local_posts_group.set_title("Posts#")
                content_box.append(self.local_posts_group)

            # -------------------------------------------------------------------------
            # 2. POPULATE CARDS: Draw brand-new ActionRow cards on the clean layout
            # -------------------------------------------------------------------------
            for item in posts_data:
                self.local_posts_items.append(item)
                card = Adw.ActionRow()
                card.set_title(item.get("title", "test"))
                card.set_subtitle(item.get("body", "test"))
                card.set_activatable(True)
                
                # Bind item payload context directly to row object
                card.payload = item
                card.connect("activated", card_clicked)
                
                card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                self.local_posts_group.add(card)
            
            # Force layout refresh and switch focus state
            self.local_posts_group.set_visible(True)
            self.local_posts_group.queue_resize()
            return False

        # Background processing worker thread function
        def test_fetch_worker():
            print("test_fetch worker running in thread background...")
            import threading
            import time
            
            # Safe non-blocking delay inside thread
            time.sleep(0.1)  
            
            """file_path = os.path.join(GLib.get_current_dir(), "./data/posts.json")

            if not os.path.exists(file_path):
                print("no json file found")
                return"""

            #
            #self.read_json_file(populate_ui_cards, "data", "posts")
            self.handle_json_file.read_json_file(populate_ui_cards, "data", "posts")
            


            

        # Fire off the data fetch routine inside a detached background worker thread
        worker_thread = threading.Thread(target=test_fetch_worker, daemon=True)
        worker_thread.start()


    def build_test_comments_by_postId_view(self, parent_container, postId):
       print(f"build_test_comments_by_postId_view : {postId}")
       #
       def test_fetch():
            print("test_fetch")
            import time


            #for child in self.right_sidebar.observe_children():
                    #self.right_sidebar.remove(child)

            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            
            """file_path = os.path.join(GLib.get_current_dir(), "./data/comments.json")

            if not os.path.exists(file_path):
                print("no json file")
                return False
            
            print("json file exists!")"""

           

             # Create a preferences group for comments
            comments_group = Adw.PreferencesGroup()
            comments_group.set_margin_start(8)
            comments_group.set_margin_end(8)
            comments_group.set_margin_bottom(16)
            
            # Create scrolled window for comments
            scroll_win = Gtk.ScrolledWindow()
            scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            scroll_win.set_min_content_height(200)  # Give it a minimum height
            scroll_win.set_vexpand(True)  # Allow it to expand
            scroll_win.set_child(comments_group)
            
            # Add a frame around the comments section (optional)
            # frame = Adw.PreferencesGroup()
            # frame.add(scroll_win)
            
            # Add the scrolled window to the parent container
            parent_container.append(scroll_win)
            #
            def populate_ui_cards(data):
                    comment_count = 0
                    
                    for item in data:
                        pid = item.get("postId")
                        #id = item.get("id")
                        if pid == postId:
                            card = Adw.ActionRow()
                            card.set_title(item.get("name", "test"))
                            card.set_subtitle(item.get("body", "test"))
                            card.set_activatable(False)
                            #card.payload = item
                            #card.connect("activated", card_clicked)
                            card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                            card.set_margin_bottom(5)
                            #local_items_group.add(card)
                            #sidebar_group.add(card)
                            comments_group.add(card)
                            #sidebar_group.add(card)
                    
                    
                     # If no comments found, show a message
                    if comment_count == 0:
                        empty_label = Gtk.Label(label="No comments for this post")
                        empty_label.add_css_class("dim-label")
                        empty_label.set_margin_top(12)
                        empty_label.set_margin_bottom(12)
                        comments_group.add(empty_label)
                    
                    comments_group.queue_resize()

            #
            self.handle_json_file.read_json_file(populate_ui_cards, "data", "comments")
            


            

            return False # Stop the GLib idle loop from repeating this function
       
       test_fetch()


       def build_test_view(self):
        #
        print(f"state#: {self.state}")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False) 
        local_title = Gtk.Label(label="test Manager")
        local_title.add_css_class("heading")
        local_action_bar.set_title_widget(local_title)

        local_wrapper.add_top_bar(local_action_bar)


        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)

        local_items_group = Adw.PreferencesGroup()
        local_items_group.set_title("test ui")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(local_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.center_stack.add_named(local_wrapper, "local_test_view")


        docs = []   


        def test_fetch():
            print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            
            file_path = os.path.join(GLib.get_current_dir(), "./data/test.json")

            if not os.path.exists(file_path):
                print("no json file")
                return False
            
            print("json file exists!")

            def card_clicked(row):
                #print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                #
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.right_sidebar.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("author"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                self.right_sidebar.append(body_label)
                #sidebar_group = Adw.PreferencesGroup()
                #sidebar_group.set_title("User Information")

               
                # inject the completed data card into right-sidebar
                #self.right_sidebar.append(sidebar_group)
                #
                #sidebar_group.set_margin_start(8)
                #sidebar_group.set_margin_end(8)

            try:
                success, content = GLib.file_get_contents(file_path)

                if success:
                    if isinstance(content, bytes):
                        content = content.decode("utf-8")
                        
                    data = json.loads(content)
                    #print(f"data size: {len(data)}")
                    
                    for item in data:
                        print(f"item: {item}")
                        docs.append(item)
                        card = Adw.ActionRow()
                        card.set_title(item.get("title", "test"))
                        card.set_subtitle(item.get("author", "test"))
                        card.set_activatable(True)
                        card.payload = item
                        card.connect("activated", card_clicked)
                        card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                        local_items_group.add(card)
                    
                    # --- ACTION TAKEN HERE ---
                    # Now that docs is populated, safely trigger your UI updates or prints:
                    #print(f"len docs inside callback: {len(docs)}")

                    local_items_group.queue_resize()
                    
                    

                else:
                    print("GLib failed to read file contents successfully.")
            except Exception as e:
                print(f"ERROR: {e}")

            return False # Stop the GLib idle loop from repeating this function
        
        # Queue the function to run as soon as the main loop is ready
        GLib.idle_add(test_fetch)

        


        #content_box.append(local_items_group)
        #scroll_win.set_child(content_box)
        #local_wrapper.set_content(scroll_win)


        #
        #self.center_stack.add_named(local_wrapper, "local_test_view")


    def build_test_todos_view(self):
        #
        print(f"state#: {self.state}")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False) 
        local_title = Gtk.Label(label="Todos Manager")
        local_title.add_css_class("heading")
        local_action_bar.set_title_widget(local_title)

        local_wrapper.add_top_bar(local_action_bar)


        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)

        self.local_todos_group = Adw.PreferencesGroup()
        self.local_todos_group .set_title("test ui")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(self.local_todos_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.center_stack.add_named(local_wrapper, "local_test_todos_view")


        


        def test_fetch():
            print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            
            """file_path = os.path.join(GLib.get_current_dir(), "./data/todos.json")

            if not os.path.exists(file_path):
                print("no json file")
                return False
            
            print("json file exists!")"""

            def card_clicked(row):
                print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.right_sidebar.get_first_child():
                    self.right_sidebar.remove(child)
                #
                self.right_sidebar.set_margin_top(16)
                self.right_sidebar.set_margin_start(12)
                self.right_sidebar.set_margin_end(12)
                self.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.right_sidebar.append(title_label)
                #
                
            def populate_ui_cards(data):
                for item in data:
                        print(f"item: {item}")
                        self.local_todos_items.append(item)
                        card = Adw.ActionRow()
                        card.set_title(item.get("title", "test"))
                        #card.set_subtitle(item.get("author", "test"))
                        card.set_activatable(True)
                        card.payload = item
                        card.connect("activated", card_clicked)
                        card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                        self.local_todos_group.add(card)
                    
                    
                    

                self.local_todos_group.queue_resize()

            #self.read_json_file(populate_ui_cards, "data", "todos")
            self.handle_json_file.read_json_file(populate_ui_cards, "data", "todos")
            #
            return False # Stop the GLib idle loop from repeating this function
        
        # Queue the function to run as soon as the main loop is ready
        GLib.idle_add(test_fetch)


    def build_shell_view(self):
        shell_wrapper = Adw.ToolbarView()
        #
        shell_action_bar = Gtk.HeaderBar()
        shell_action_bar.set_show_title_buttons(False)
        #
        self.shell_title = Gtk.Label(label=self.i18n._("shell_manager"))
        self.shell_title.add_css_class("heading")
        shell_action_bar.set_title_widget(self.shell_title)
        shell_wrapper.add_top_bar(shell_action_bar)
        #
        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        #
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content_box.set_margin_top(16)
        content_box.set_margin_bottom(16)
        content_box.set_margin_start(16)
        content_box.set_margin_end(16)
        #
        self.terminal_scroller = Gtk.ScrolledWindow()
        self.terminal_scroller.set_vexpand(True)
        self.terminal_scroller.set_hexpand(True)
        self.terminal_scroller.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        self.terminal_view = Gtk.TextView()
        self.terminal_view.set_editable(False)
        self.terminal_view.set_cursor_visible(False)
        self.terminal_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.terminal_view.add_css_class("monospace")

        self.terminal_scroller.set_child(self.terminal_view)
        content_box.append(self.terminal_scroller)


        #
        input_row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        #
        prompt_lbl = Gtk.Label(label="user@app:~$")
        prompt_lbl.add_css_class("dim-label")
        prompt_lbl.add_css_class("monospace")
        prompt_lbl.add_css_class("prompt")
        
        #
        #self.shell_entry = Gtk.Entry(placeholder_text=self.i18n._("shell_placeholder"))
        self.shell_entry = Gtk.Entry()
        self.shell_entry.set_placeholder_text(self.i18n._("shell_placeholder"))
        self.shell_entry.set_hexpand(True)
        self.shell_entry.add_css_class("monospace")
        self.shell_entry.connect("activate", self.on_execute_shell_command)
        #
        self.shell_run_btn = Gtk.Button(label=self.i18n._("shell_run_btn"))
        self.shell_run_btn.add_css_class("suggested-action")
        #self.shell_run_btn.connect("clicked", self.on_execute_shell_command)
        #
        input_row_box.append(prompt_lbl)
        input_row_box.append(self.shell_entry)
        input_row_box.append(self.shell_run_btn)
        content_box.append(input_row_box)
        #
        #pref_group = Adw.PreferencesGroup()
        #pref_group.set_title("Terminal Logs")
        #
        self.shell_log_row = Adw.ActionRow()
        self.shell_log_row.set_title("Console Output Ready...")
        self.shell_log_row.set_subtitle("System shell runtime operational pipelines are initialized.")
        #
        #pref_group.add(self.shell_log_row)
        #content_box.append(pref_group)
        content_box.append(input_row_box)
        #
        scroll_win.set_child(content_box)
        shell_wrapper.set_content(scroll_win)
        #
        self.center_stack.add_named(shell_wrapper, "shell_console_view")



    def on_execute_shell_command(self, button):
        print("on_execute_shell_command")
        #
        cmd = self.shell_entry.get_text()
        cmd_text = cmd.strip()
        if not cmd_text:
            print("Validation Warning!")
            return
        #
        print(f"CMD: '{cmd_text}'")
        print("CMD > ", cmd_text)
        print(cmd_text)
        buffer = self.terminal_view.get_buffer()
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, f"user@app:~$ {cmd_text}\n")
        self.shell_entry.set_text("")
        self.shell_run_btn.set_sensitive(False)
        #
        import threading
        worker_thread = threading.Thread(
            target=self.on_execute_shell_process_worker,
            args=(cmd_text,),
            daemon=True
        )
        worker_thread.start()

    def append_text_to_terminal(self, log_stream):
        

        buffer = self.terminal_view.get_buffer()
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, f"{log_stream}\n")
        mark = buffer.create_mark(None, buffer.get_end_iter(), False)
        self.terminal_view.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)
       
        if hasattr(self, 'shell_run_btn'):
            self.shell_run_btn.set_sensitive(True)

        return False


    def on_execute_shell_process_worker(self, cmd_text):
        import subprocess

        if cmd_text.lower() == "clear":
            GLib.idle.add(lambda: self.terminal_view.get_buffer().set_text(""))
            GLib.idle_add(lambda: self.shell_run_btn.set_sensitive(True))
            return
        try:
            result = subprocess.run(
                cmd_text,
                shell=True,
                text=True,
                capture_output=True,
                timeout=10.0
            )
            if result.returncode == 0:
                output_text = result.stdout
                if not output_text:
                    output_text = "[Command executed success with no output]"
            else:
                output_text = f"Error (Status {result.returncode}):\n{result.stderr}"

        except subprocess.TimeoutExpired:
             output_text = "Error: Command exceeded the maximum 10-second"

        except Exception as e:
               print(f"Failure: {e}")
        #
        GLib.idle_add(self.append_text_to_terminal, output_text)


    
    def build_local_tabs_view(self):
        #
        print(f"state#: {self.state}")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False)

        #
        self.local_title = Gtk.Label(label=self.i18n._("local_manager"))
        self.local_title.add_css_class("heading")
        local_action_bar.set_title_widget(self.local_title)
        #
        self.add_item_btn = Gtk.Button(label=self.i18n._("btn_add"))
        self.add_item_btn.add_css_class("suggested-action")
        local_action_bar.pack_end(self.add_item_btn)
        # build the form as popover
        self.form_popover = Gtk.Popover()
        self.form_popover.set_parent(self.add_item_btn)
        self.form_popover.set_has_arrow(True)
        # layout inside form popover box
        form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        form_box.set_margin_top(12)
        form_box.set_margin_bottom(12)
        form_box.set_margin_start(12)
        form_box.set_margin_end(12)
        form_box.set_size_request(240, -1)
        #
        popover_title = Gtk.Label(label=self.i18n._("popover_add_title"))
        popover_title.add_css_class("title-3")
        popover_title.set_halign(Gtk.Align.START)
        form_box.append(popover_title)
        # inputs
        self.input_name = Gtk.Entry(placeholder_text=self.i18n._("input_name_ph"))
        form_box.append(self.input_name)

        self.input_desc = Gtk.Entry(placeholder_text=self.i18n._("input_desc_ph"))
        form_box.append(self.input_desc)

        # submit button
        submit_btn = Gtk.Button(label=self.i18n._("btn_submit"))
        submit_btn.add_css_class("suggested-action")
        submit_btn.connect("clicked", self.on_form_submitted2)
        form_box.append(submit_btn)

        self.form_popover.set_child(form_box)
        # click on add button to open form_popover
        self.add_item_btn.connect("clicked", lambda btn: self.form_popover.popup())
       
        local_wrapper.add_top_bar(local_action_bar)

        #
        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)

        #
        #self.local_items_group = Adw.PreferencesGroup()
        self.local_items_group.set_title(self.i18n._("group_title"))

        #
        

        #
        self.empty_list_lbl = Gtk.Label(label=self.i18n._("empty_list_text"))
        self.empty_list_lbl.add_css_class("dim-label")
        self.local_items_group.add(self.empty_list_lbl)
        # attach list data in ui
        content_box.append(self.local_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)


        #
        self.center_stack.add_named(local_wrapper, "local_view")


        



    def build_disk_tabs_view(self):
        #
        print(f"state#: {self.state}")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False)

        #
        self.local_disk_title = Gtk.Label(label=self.i18n._("disk_manager")) # Disk List Manager
        self.local_disk_title.add_css_class("heading")
        local_action_bar.set_title_widget(self.local_disk_title)
        #
        self.add_disk_item_btn = Gtk.Button(label=self.i18n._("btn_add"))
        self.add_disk_item_btn.add_css_class("suggested-action")
        local_action_bar.pack_end(self.add_disk_item_btn)
        # build the form as popover
        self.form_disk_popover = Gtk.Popover()
        self.form_disk_popover.set_parent(self.add_disk_item_btn)
        self.form_disk_popover.set_has_arrow(True)
        # layout inside form popover box
        form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        form_box.set_margin_top(12)
        form_box.set_margin_bottom(12)
        form_box.set_margin_start(12)
        form_box.set_margin_end(12)
        form_box.set_size_request(240, -1)
        #
        self.popover_disk_title = Gtk.Label(label=self.i18n._("popover_add_title"))
        self.popover_disk_title.add_css_class("title-3")
        self.popover_disk_title.set_halign(Gtk.Align.START)
        form_box.append(self.popover_disk_title)
        # inputs
        self.input_disk_name = Gtk.Entry(placeholder_text=self.i18n._("input_name_ph"))
        form_box.append(self.input_disk_name)

        self.input_disk_desc = Gtk.Entry(placeholder_text=self.i18n._("input_desc_ph"))
        form_box.append(self.input_disk_desc)

        # submit button
        self.submit_disk_btn = Gtk.Button(label=self.i18n._("btn_submit"))
        self.submit_disk_btn.add_css_class("suggested-action")
        self.submit_disk_btn.connect("clicked", self.on_form_disk_submitted2)
        form_box.append(self.submit_disk_btn)

        self.form_disk_popover.set_child(form_box)
        # click on add button to open form_popover
        self.add_disk_item_btn.connect("clicked", lambda btn: self.form_disk_popover.popup())
       
        local_wrapper.add_top_bar(local_action_bar)

        #
        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)

        #
        #self.disk_items_group = Adw.PreferencesGroup()
        self.disk_items_group.set_title(self.i18n._("group_disk_title")) # Stored Data in Disk with Entries

        #
        

        #
        if not self.disk_items_storage:
          self.empty_disk_list_lbl = Gtk.Label(label=self.i18n._("empty_list_text"))
          self.empty_disk_list_lbl.add_css_class("dim-label")
          self.disk_items_group.add(self.empty_disk_list_lbl)
        else:
            print(f"len disk data: {len(self.disk_items_storage)}")
            
            for item in self.disk_items_storage:
                row = Adw.ActionRow()
                row.set_title(item["name"])
                row.set_subtitle(item["description"])
                row.add_prefix(Gtk.Image.new_from_icon_name(""))
                self.disk_items_group.add(row)


        # attach list data in ui
        content_box.append(self.disk_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)


        #
        self.center_stack.add_named(local_wrapper, "disk_view")


        
    def on_form_submitted2(self, button):
        name_text = self.input_name.get_text().strip()
        desc_text = self.input_desc.get_text().strip()

        # Input Validation Check
        if not name_text:
            print("Validation Warning: Name field cannot be empty.")
            return
        
        # Build the structured item object payload
        new_entry = {"name": name_text, "description": desc_text}
        print(f"Form submission payload: {new_entry}")

        # Initialize array safely if it hasn't been instantiated yet
        if not hasattr(self, 'local_items_storage') or self.local_items_storage is None:
            self.local_items_storage = []
            
        # Append the new data row to your single local tracking array
        self.local_items_storage.append(new_entry)

        # =========================================================================
        # REUSE RENDER ENGINE: Let the display helper update rows and clear placeholders
        # =========================================================================
        # Passing self.local_items_storage handles clearing out empty state labels,
        # appends your brand-new row card, and registers it with the search bar query system.
        self.display_local_filtered_results(self.local_items_storage)

        # FORM RESET: Flush the input lines and hide the popup widget cleanly
        self.input_name.set_text("")
        self.input_desc.set_text("")
        self.form_popover.popdown()

        return False
    
    def on_form_disk_submitted2(self, button):
        name_text = self.input_disk_name.get_text().strip()
        desc_text = self.input_disk_desc.get_text().strip()

        # Input Validation Check
        if not name_text:
            print("Validation Warning: Name field cannot be empty.")
            return
        
        # Build the structured item object payload
        new_entry = {"name": name_text, "description": desc_text}
        print(f"Form submission payload: {new_entry}")

        # Initialize array safely if it hasn't been instantiated yet
        if not hasattr(self, 'disk_items_storage') or self.disk_items_storage is None:
            self.disk_items_storage = []
            
        # Append the new data row to your single local tracking array
        self.disk_items_storage.append(new_entry)
        #
        #save
        self.save_data_to_disk()

        # =========================================================================
        # REUSE RENDER ENGINE: Let the display helper update rows and clear placeholders
        # =========================================================================
        # Passing self.local_items_storage handles clearing out empty state labels,
        # appends your brand-new row card, and registers it with the search bar query system.
        self.display_disk_filtered_results(self.disk_items_storage)

        # FORM RESET: Flush the input lines and hide the popup widget cleanly
        self.input_disk_name.set_text("")
        self.input_disk_desc.set_text("")
        self.form_disk_popover.popdown()

        return False



    def on_form_submitted(self, button):

        name_text = self.input_name.get_text().strip()
        desc_text = self.input_desc.get_text().strip()

        #
        if not name_text:
            return
        
        # save data
        # if state is local then save in local_items_storage, 
        # if it's disk then save in disk_items_storage
        new_entry = {"name": name_text, "description": desc_text}
        print(f"inputs: {new_entry}")
        self.local_items_storage.append(new_entry)
        
       
        #
        if len(self.local_items_storage) == 1:
            self.local_items_group.remove(self.empty_list_lbl)

        #
        new_row = Adw.ActionRow()
        new_row.set_title(name_text)
        new_row.set_subtitle(desc_text)

        # add icon in each item
        new_row.add_prefix(Gtk.Image.new_from_icon_name("package-x-generic-symbolic"))
        
        # if state is local then save in local_item
        # if satte is disk then save in disk
        self.local_items_group.add(new_row)

        #
        self.input_name.set_text("")
        self.input_desc.set_text("")
        self.form_popover.popdown()

        # disk


    def on_form_disk_submitted(self, button):

        name_text = self.input_disk_name.get_text().strip()
        desc_text = self.input_disk_desc.get_text().strip()

        #
        if not name_text:
            return
        
        # save data
        # if state is local then save in local_items_storage, 
        # if it's disk then save in disk_items_storage
        new_entry = {"name": name_text, "description": desc_text}
        print(f"disk inputs: {new_entry}")
       
        
        

        #
        if not self.disk_items_storage:
            self.disk_items_group.remove(self.empty_list_lbl)
        #
        self.disk_items_storage.append(new_entry)

        #save
        self.save_data_to_disk()

        #
        new_row = Adw.ActionRow()
        new_row.set_title(name_text)
        new_row.set_subtitle(desc_text)

        # add icon in each item
        new_row.add_prefix(Gtk.Image.new_from_icon_name("package-x-generic-symbolic"))
        
        #
        self.disk_items_group.add(new_row)

        #
        self.input_disk_name.set_text("")
        self.input_disk_desc.set_text("")
        self.form_disk_popover.popdown()

         

    
    def on_home_item_clicked(self, row):
        clicked_title = row.get_title()




        if clicked_title == "Users":
            #self.center_stack.set_visible_child_name("loading_view")
            #self.trigger_users_fetch_pipeline()
           
            #thread = threading.Thread(target=self.test_ui)
            #thread.daemon = True
            #thread.start()
            #self.jam.set_name("home-jam")
            #print(f"jam-name: {self.jam.get_name()}")
            #self.center_stack.set_visible_child_name("local_test_view")
            #self.jam.center_stack.set_visible_child_name("local_test_view")
            self.center_stack.set_visible_child_name("local_test_users_view")
            
            


        elif clicked_title == "Local":
            print("Local item")
            self.info_label.set_text(f"Selected Section: {clicked_title}")
            self.state = "local"
            print(f"edit state: {self.state}")
            self.center_stack.set_visible_child_name("local_view")
            

        elif clicked_title == "Storage":
            print("Storage item")
            self.info_label.set_text(f"Selected Section: {clicked_title}")
            self.state = "disk"
            print(f"edit state: {self.state}")
            self.center_stack.set_visible_child_name("disk_view")
        
        elif clicked_title == "Posts":
            print("Posts item")
            #self.info_label.set_text(f"Selected Section: {clicked_title} #")
            #self.center_stack.set_visible_child_name("loading_view")
            self.center_stack.set_visible_child_name("local_test_posts_view")

        elif clicked_title == "Todos":
            print("Todos item")
            #self.center_stack.set_visible_child_name("loading_view")
            self.center_stack.set_visible_child_name("local_test_todos_view")

        elif clicked_title == "Test":
            print("Test item")
            self.center_stack.set_visible_child_name("local_test_view")

        elif clicked_title == "Shell Terminal":
            print("Shell item")
            #self.center_stack.set_visible_child_name("shell_view")
            #self.info_label.set_text(f"Selected Section: {clicked_title} #")
            self.center_stack.set_visible_child_name("shell_console_view")
            
        


        else:
            #self.center_stack.set_visible_child_name("welcome_view")
            self.info_label.set_text(f"Selected Section: {clicked_title}")
            self.state = ""
        # call fetching

    
     # fetch users


    def on_settings_item_clicked(self, row):
        clicked_title = row.get_title()
        self.info_label.set_text(f"Selected Section: {clicked_title}")



    def trigger_users_fetch_pipeline(self):
        """ Re-enters loading state and spins up the network thread """
        print("Starting background file reader thread...")
        self.center_stack.set_visible_child_name("loading_view")
        thread = threading.Thread(target=self.fetch_local_users)
        thread.daemon = True
        thread.start()
    

    def fetch_users(self):

        
        """try:
         url = "https://jsonplaceholder.typicode.com/users"
         req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
         with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(data)
            GLib.idle_add(self.update_users_ui, data)
        except Exception as e:
            print(f"Network error: {e}")
            GLib.idle_add(self.update_users_ui, None)"""
        #
        
        """ Robust network worker that handles 'Connection reset' gracefully """
        import socket
        try:
            url = "https://jsonplaceholder.typicode.com/users"
            
            # 1. Provide realistic browser headers to prevent the server from rejecting your VM
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
                'Accept': 'application/json',
                'Connection': 'close' # Explicitly tells the server to close neatly after sending data
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            # 2. Added a 10-second timeout constraint so the app won't hang indefinitely if the route drops
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                # Hand data back to the main UI render loop thread
                GLib.idle_add(self.update_users_ui, data)
                
        except (urllib.error.URLError, socket.error) as network_error:
            # 3. Intercept connection drops gracefully without disrupting UI elements
            print(f"Network error managed successfully: {network_error}")
            
            # Send 'None' to trigger the visual error label message on screen instead of freezing
            GLib.idle_add(self.update_users_ui, None)

    def fetch_local_users(self):
        """ Safe local file reader that unpacks GLib structures correctly """
        import time
        print("Initializing local storage file reader pipeline...")
        
        # 1. Give the main UI thread 100 milliseconds to smoothly switch to loading_view
        time.sleep(0.1) 
        
        file_path = os.path.join(GLib.get_current_dir(), "users.json")

        if not os.path.exists(file_path):
            print(f"Local Storage Error: File does not exist at {file_path}")
            GLib.idle_add(self.update_users_ui, None)
            return None

        try:
            success, content = GLib.file_get_contents(file_path)

            if success:
                if isinstance(content, bytes):
                    content = content.decode("utf-8")
                    
                data = json.loads(content)
                
                # Push back to the primary animation thread safely
                GLib.idle_add(self.update_users_ui, data)
            else:
                print("GLib failed to read file contents successfully.")
                GLib.idle_add(self.update_users_ui, None)

        except GLib.Error as e:
            print(f"GNOME GLib Error reading file system: {e.message}")
            GLib.idle_add(self.update_users_ui, None)
            
        except json.JSONDecodeError as e:
            print(f"Syntax Error: users.json contains invalid formatting: {e}")
            GLib.idle_add(self.update_users_ui, None)

        return None



    def test_ui(self):
        print("test-ui")    
        while (child := self.test_container.get_first_child()):
          self.test_container.remove(child)
        pref_group = Adw.PreferencesGroup()
        pref_group.set_title("Registered System Test")
        pref_group.set_description("Click any test card to view full test")
        pref_group.set_margin_start(12)
        pref_group.set_margin_end(12)
        pref_group.set_margin_top(12)

        lbl = Gtk.Label(label="test")

        # Create a proper row widget instead of a raw Gtk.Label
        row = Adw.ActionRow()
        row.set_title("Test Item")
        row.set_subtitle("Click to run or view details")

        # Add the row to your group
        pref_group.add(row)

        #pref_group.add(lbl)


        self.test_container.set_visible(True)
        self.test_container.append(pref_group)
        
        # 7. Shift view right here directly on the main loop thread 
        # Do NOT hide this call inside an nested force_stack_transition closure!
        self.center_stack.set_visible_child_name("test_view")
        print("Stack successfully shifted target visibility frame layer to 'test_view'")

        return False  # Critical: tells GLib loop window thread to terminate track

     


    def update_users_ui(self, users_list):
        """ Updates the main application window with loaded profile cards """
        print("update_users_ui executing... Data Received:", bool(users_list))

        # 1. Clear out old layout widgets entirely
        while child := self.users_container.get_first_child():
            self.users_container.remove(child)

        # 2. Safety Check: Handle Empty State
        if not users_list:
            error_lbl = Gtk.Label(label="Failed to pull profile records.")
            error_lbl.set_margin_top(24)
            error_lbl.set_halign(Gtk.Align.CENTER)
            error_lbl.add_css_class("dim-label")
            self.users_container.append(error_lbl)
            self.center_stack.set_visible_child_name("users_view")
            return False

        # 3. Create the Libadwaita preferences layout block
        pref_group = Adw.PreferencesGroup()
        pref_group.set_title("Registered System Users")
        pref_group.set_description("Click any user card to view full profile")
        pref_group.set_margin_start(12)
        pref_group.set_margin_end(12)
        pref_group.set_margin_top(12)

        # 4. Populate rows mapping directly to your provided JSON fields
        for user in users_list:
            user_card = Adw.ActionRow()
            user_card.set_title(user.get("name", "Unknown User"))
            user_card.set_subtitle(user.get("email", "No Email"))
            user_card.set_activatable(True)
            
            # Safe raw payload fallback hook
            user_card.user_data_payload = user

            # Decorate with standard person icon indicator
            avatar = Gtk.Image.new_from_icon_name("avatar-default-symbolic")
            user_card.add_prefix(avatar)

            # Build out right side phone layout elements
            phone_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            phone_box.set_valign(Gtk.Align.CENTER)
            
            phone_icon = Gtk.Image.new_from_icon_name("call-start-symbolic") 
            phone_lbl = Gtk.Label(label=str(user.get("phone", "No Phone")))
            phone_lbl.add_css_class("dim-label")
            
            phone_box.append(phone_icon)
            phone_box.append(phone_lbl)
            user_card.add_suffix(phone_box)
            
            # Connect to action click click event if method exists
            if hasattr(self, 'on_user_card_clicked'):
                user_card.connect("activated", self.on_user_card_clicked)
                
            pref_group.add(user_card)

        # 5. Append group layout container back into the original connected box
        self.users_container.append(pref_group)

        # 6. FORCE layout visibility states to True across the container line
        self.users_container.set_visible(True)
        
        # 7. Shift view right here directly on the main loop thread 
        # Do NOT hide this call inside an nested force_stack_transition closure!
        self.center_stack.set_visible_child_name("users_view")
        print("Stack successfully shifted target visibility frame layer to 'users_view'")

        return False  # Critical: tells GLib loop window thread to terminate track

        


        
    def on_user_card_clicked(self, row):
        user = row.user_data_payload
        print(f"User card selected: {user.get("name")}")

        #
        while child := self.right_sidebar.get_first_child():
            self.right_sidebar.remove(child)
        #
        self.right_sidebar.set_margin_top(16)
        self.right_sidebar.set_margin_start(12)
        self.right_sidebar.set_margin_end(12)
        self.right_sidebar.set_margin_bottom(16)
        #
        title_label = Gtk.Label(label=user.get("name"))
        title_label.add_css_class("title-1") # built-in font bold
        title_label.set_margin_bottom(12)
        title_label.set_halign(Gtk.Align.START)
        self.right_sidebar.append(title_label)
        #
        sidebar_group = Adw.PreferencesGroup()
        sidebar_group.set_title("User Information")

        #
        username_row = Adw.ActionRow(title="Username", subtitle=user.get("username", "N/A"))
        sidebar_group.add(username_row)
        #
        web_row = Adw.ActionRow(title="Website", subtitle=user.get("website", "N/A"))
        sidebar_group.add(web_row)
        #
        company_name = user.get("company", {}).get("name", "N/A")
        company_row = Adw.ActionRow(title="Company", subtitle=company_name)
        sidebar_group.add(company_row)

        #
        city_name = user.get("address", {}).get("city", "N/A")
        city_row = Adw.ActionRow(title="City", subtitle=city_name)
        sidebar_group.add(city_row)

        # inject the completed data card into right-sidebar
        self.right_sidebar.append(sidebar_group)
        #
        sidebar_group.set_margin_start(8)
        sidebar_group.set_margin_end(8)

    # fetch posts

    def trigger_posts_fetch_pipeline(self):
        """ Safe helper to initialize the posts view transition states """
        self.center_stack.set_visible_child_name("loading_view")
        thread = threading.Thread(target=self.fetch_posts)
        thread.daemon = True
        thread.start()


    def fetch_posts(self):
        print("fetch posts") 
        try:
            url = "https://jsonplaceholder.typicode.com/posts"
            # Provided robust headers matching your network stack requirements
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
                'Accept': 'application/json'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                GLib.idle_add(self.update_posts_ui, data)
        except Exception as e:
            print(f"Network error in posts: {e}")
            # FIX: Fall back to your dedicated posts layout handler if route drops
            GLib.idle_add(self.update_posts_ui, None)



    def update_posts_ui(self, posts_list):
        print("update_posts_ui")
        #
        # Strip out previous widgets from the posts box
        while child := self.posts_container.get_first_child():
            self.posts_container.remove(child)

        if not posts_list:
            error_lbl = Gtk.Label(label="Failed to load system articles. Check connectivity.")
            self.posts_container.append(error_lbl)
            self.center_stack.set_visible_child_name("posts_view")
            return

        pref_group = Adw.PreferencesGroup()
        pref_group.set_title("Registered System Posts")
        pref_group.set_description("Click any post card below to pull nested commentary lists into the right inspector.")

        for post in posts_list:
            post_card = Adw.ActionRow()
            post_card.set_title(post.get("title", "Unknown"))
            post_card.set_subtitle(post.get("body", "No Body"))
            post_card.set_margin_bottom(8)
            post_card.set_activatable(True)
            
            # Save raw payload dictionary inside the instance variable property
            post_card.post_data_payload = post
            
            # Prefix a text document icon indicator to the left
            post_card.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
            post_card.connect("activated", self.on_post_card_clicked)
            pref_group.add(post_card)

        self.posts_container.append(pref_group)
        self.center_stack.set_visible_child_name("posts_view")
    


    def on_post_card_clicked(self, row):
        print("on_post_card_clicked")
        post = row.post_data_payload
        print(f"User card selected: {post.get("title")}")
        

        #
        while child := self.right_sidebar.get_first_child():
            self.right_sidebar.remove(child)
        #
        self.right_sidebar.set_margin_top(16)
        self.right_sidebar.set_margin_start(12)
        self.right_sidebar.set_margin_end(12)
        self.right_sidebar.set_margin_bottom(16)
        # post->title
        title_label = Gtk.Label(label=post.get("title"))
        title_label.add_css_class("title-1") # built-in font bold
        title_label.set_margin_bottom(12)
        title_label.set_halign(Gtk.Align.START)
        self.right_sidebar.append(title_label)
        # post->body
        body_label = Gtk.Label(label=post.get("body"))
        body_label.add_css_class("dim-label") # built-in font bold
        body_label.set_margin_bottom(24)
        body_label.set_halign(Gtk.Align.START)
        body_label.set_wrap(True)
        self.right_sidebar.append(body_label)
        #
        # Instantiate persistent UI placeholder for the comments list tree
        self.sidebar_comments_group = Adw.PreferencesGroup()
        self.sidebar_comments_group.set_title("Comments")
        self.right_sidebar.append(self.sidebar_comments_group)

        # Placeholder loading indicator inside the sidebar group layout tree
        self.comments_loading_lbl = Gtk.Label(label="Retrieving commentary thread...")
        self.sidebar_comments_group.add(self.comments_loading_lbl)

        postId = post.get("id")
        print(f"postId: {postId}")

        # FIX: Correct thread invocation parameters to prevent UI freezing
        thread = threading.Thread(
            target=self.fetch_comments_by_postId, 
            args=(postId,) # Passes argument safely as tuple context parameter
        )
        thread.daemon = True
        thread.start()

        # Inject the completed data card into right-sidebar
        self.sidebar_comments_group.set_margin_start(8)
        self.sidebar_comments_group.set_margin_end(8)


    # fetch comments by postId
    def fetch_comments_by_postId(self, postId):
        print(f"fetch comments for postId {postId}")
        try:
            url = f"https://jsonplaceholder.typicode.com/comments?postId={postId}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
                'Accept': 'application/json'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                print("comments:", data)
                GLib.idle_add(self.update_comments_ui, data)
        except Exception as e:
            print(f"Network error: {e}")
            GLib.idle_add(self.update_users_ui, None)


    #
    def update_comments_ui(self, comments_list):
        print("update_comment_ui")
        print(f"len comments: {len(comments_list)}")

        # 1. Safely remove the placeholder string "Retrieving commentary thread..."
        if hasattr(self, 'comments_loading_lbl') and self.comments_loading_lbl.get_parent():
            self.sidebar_comments_group.remove(self.comments_loading_lbl)

        # 2. Check if the array came back empty or failed
        if not comments_list:
            error_msg = Gtk.Label(label="No comments found or connection timeout.")
            error_msg.add_css_class("dim-label")
            self.sidebar_comments_group.add(error_msg)
            return

        # 3. Populate your rows under the Comments heading block area cleanly
        for comment in comments_list:
            comment_row = Adw.ActionRow()
            comment_row.set_title(comment.get("email", "Anonymous"))
            comment_row.set_subtitle(comment.get("body", ""))
            comment_row.set_margin_bottom(6)
            
            # Add message bubble decorations icon to the left side
            bubble_icon = Gtk.Image.new_from_icon_name("chat-message-new-symbolic")
            comment_row.add_prefix(bubble_icon)
            
            self.sidebar_comments_group.add(comment_row)


    """

    def on_toggle_direction_clicked(self, button):
        print("on_toggle_direction_clicked")
        curr_direction = Gtk.Widget.get_default_direction()

        if curr_direction == Gtk.TextDirection.RTL:
            Gtk.Widget.set_default_direction(Gtk.TextDirection.LTR)
            self.win.set_direction(Gtk.TextDirection.LTR)
            self.info_label.set_text("Current Layout: LTR")
            self.current_lang = "en"
            self.i18n.current_lang = "en"
            #
            # Update all potential pointer targets to ensure english is loaded
            self.current_lang = "en"
            if hasattr(self, 'i18n'):
                self.i18n.current_lang = "en"
            if hasattr(self, 'lang'):
                self.lang.current_lang = "en"
            #
        else:
            Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)
            self.win.set_direction(Gtk.TextDirection.RTL)
            self.info_label.set_text("Current Layout: RTL")
            self.current_lang = "ar"
            self.i18n.current_lang = "ar"
            #
            # Update all potential pointer targets to ensure arabic is loaded
            self.current_lang = "ar"
            if hasattr(self, 'i18n'):
                self.i18n.current_lang = "ar"
            if hasattr(self, 'lang'):
                self.lang.current_lang = "ar"
        #
        #self.init_direction_lang()
        #self.info_label.queue_allocate()
        if hasattr(self, 'win') and self.win:
            self.win.set_title(f"{self.i18n._('gnome_app')}")
            #
            #self.rebuild_list_box()

        #if hasattr(self, 'tab1_box') and self.tab1_box:
            #self.tab1_box.append(self.rebuild_list_box)
        # =========================================================================
        # REPAINT ACTION 1: Update the master Adw.ViewStack tab page titles
        # =========================================================================
        if hasattr(self, 'home_page_wrapper') and self.home_page_wrapper:
            self.home_page_wrapper.set_title(self.i18n._("tab_home"))

        #
        if hasattr(self, 'nav_rows') and self.nav_rows:
            print("Refreshing action row navigation titles in UI thread...")
            for key, row_widget in self.nav_rows.items():
                # Re-fetch the text value from the freshly updated language index
                row_widget.set_title(self.i18n._(key))
        #
        if hasattr(self, 'nav_settings_rows') and self.nav_settings_rows:
            print("Refreshing action row navigation titles in UI thread...")
            for key, row_widget in self.nav_settings_rows.items():
                # Re-fetch the text value from the freshly updated language index
                row_widget.set_title(self.i18n._(key))

        #
        if hasattr(self, 'page2_wrapper') and self.page2_wrapper:
            self.page2_wrapper.set_title(self.i18n._("tab_settings"))
        #
        if hasattr(self, 'page3_wrapper') and self.page3_wrapper:
            self.page3_wrapper.set_title(self.i18n._("tab_profile"))
        # search
        if hasattr(self, 'sidebar_search_entry') and self.sidebar_search_entry:
            # Re-fetch the string matching the newly activated language flag
            self.sidebar_search_entry.set_placeholder_text(self.i18n._("search_placeholder"))
            print("Sidebar search entry placeholder text refreshed.")
        # local
        if hasattr(self, 'local_title') and self.local_title:
            self.local_title.set_label(self.i18n._("local_manager"))

        if hasattr(self, 'add_item_btn') and self.add_item_btn:
            self.add_item_btn.set_label(self.i18n._("btn_add"))

        if hasattr(self, 'popover_title') and self.popover_title:
            self.popover_title.set_label(self.i18n._("popover_add_title"))

        if hasattr(self, 'input_name') and self.input_name:
            self.input_name.set_placeholder_text(self.i18n._("input_name_ph"))

        if hasattr(self, 'input_desc') and self.input_desc:
            self.input_desc.set_placeholder_text(self.i18n._("input_desc_ph"))

        if hasattr(self, 'submit_btn') and self.submit_btn:
            self.submit_btn.set_label(self.i18n._("btn_submit"))

        if hasattr(self, 'local_items_group') and self.local_items_group:
            self.local_items_group.set_title(self.i18n._("group_title"))

        if hasattr(self, 'empty_list_lbl') and self.empty_list_lbl:
            self.empty_list_lbl.set_label(self.i18n._("empty_list_text"))

        # disk
        if hasattr(self, 'local_disk_title') and self.local_disk_title:
            self.local_disk_title.set_label(self.i18n._("disk_manager"))

        if hasattr(self, 'add_disk_item_btn') and self.add_disk_item_btn:
            self.add_disk_item_btn.set_label(self.i18n._("btn_add"))

        if hasattr(self, 'popover_disk_title') and self.popover_disk_title:
            self.popover_disk_title.set_label(self.i18n._("popover_add_title"))

        if hasattr(self, 'input_disk_name') and self.input_disk_name:
            self.input_disk_name.set_placeholder_text(self.i18n._("input_name_ph"))

        if hasattr(self, 'input_disk_desc') and self.input_disk_desc:
            self.input_disk_desc.set_placeholder_text(self.i18n._("input_desc_ph"))

        if hasattr(self, 'submit_disk_btn') and self.submit_disk_btn:
            self.submit_disk_btn.set_label(self.i18n._("btn_submit"))

        if hasattr(self, 'disk_items_group') and self.disk_items_group:
            self.disk_items_group.set_title(self.i18n._("group_disk_title"))

        if hasattr(self, 'empty_list_lbl') and self.empty_list_lbl:
            self.empty_list_lbl.set_label(self.i18n._("empty_list_text"))
        #
        if hasattr(self, 'logout_btn') and self.logout_btn:
            self.logout_btn.set_label(self.i18n._("logout_title"))
        #
        if hasattr(self, 'login_btn') and self.login_btn:
            self.login_btn.set_label(self.i18n._("login_title"))
        #
        if hasattr(self, 'input_login_email') and self.input_login_email:
            self.input_login_email.set_placeholder_text(self.i18n._("enter_email"))
        #
        if hasattr(self, 'input_login_pass') and self.input_login_pass:
            self.input_login_pass.set_placeholder_text(self.i18n._("enter_password"))

    """

    def on_toggle_theme_clicked(self, button):
        print("on_toggle_theme_clicked executing...")

        current_scheme = self.style_manager.get_color_scheme()

        if current_scheme == Adw.ColorScheme.PREFER_LIGHT or current_scheme == Adw.ColorScheme.DEFAULT:
           self.style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
           button.set_icon_name("display-brightness-symbolic")
           print("Theme scheme updated to : FORCE DARK")    
        else:
            self.style_manager.set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)
            button.set_icon_name("weather-clear-symbolic")
            print("Theme scheme updated to: FORCE LIGHT")


    def init_direction_lang(self):
         curr_direction = Gtk.Widget.get_default_direction()

         if curr_direction == Gtk.TextDirection.RTL:
             self.i18n.current_lang = "ar"
             self.current_lang = "ar"
         else:
             self.i18n.current_lang = "en"
             self.current_lang = "en"



    """def setup_actions(self):

        # Quite Action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_clicked)
        self.add_action(quit_action)

        # About Action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_clicked)
        self.add_action(about_action)

        # restart Action
        restart_action = Gio.SimpleAction.new("restart", None)
        restart_action.connect("activate", lambda action, param:  print("restart...") )
        self.add_action(restart_action)

        #"""

    def setup_actions(self):
        """ Registers all application framework GActions EXACTLY ONCE on startup """
        print("Initializing master GAction registration pipeline...")

        # 1. Register your system default helper actions (About, Quit, Restart)
        # ... (your existing action setups for about, quit, restart) ...
        # Quite Action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_clicked)
        self.add_action(quit_action)

        # About Action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_clicked)
        self.add_action(about_action)

        # restart Action
        restart_action = Gio.SimpleAction.new("restart", None)
        #restart_action.connect("activate", lambda action, param:  print("restart...") )
        restart_action.connect("activate", lambda action, param:  self.fire_notify("Gnome App","Restart Gnome App") )
        #restart_action.connect("activate", self.on_restart_clicked)
        self.add_action(restart_action)
        # 2. CRITICAL FIX: Register the logout action here ONCE, completely safe from loops
        if not self.lookup_action("logout"):
            logout_action = Gio.SimpleAction.new("logout", None)
            logout_action.connect("activate", self.on_logout_clicked)
            self.add_action(logout_action)
            print("System Logout action successfully registered to app scope runtime channels.")


    def rebuild_menu(self):
        """ Safe, optimized layout rebuilder that resets menu items cleanly """
        print(f"rebuild_menu executing... User Authenticated: {self.isLogin}")

        # =========================================================================
        # FIX 1: Reuse or instantiate your menu container model shell cleanly
        # =========================================================================
        if not hasattr(self, 'menu') or self.menu is None:
            self.menu = Gio.Menu.new()
        else:
            self.menu.remove_all() # Clears out old options to prevent layout accumulation

        # 1. Append global navigation options common to both application states
        self.menu.append("About", "app.about")
        self.menu.append("Quit", "app.quit")
        self.menu.append("Restart", "app.restart")

        # 2. Append conditional menu entries based on active authentication parameters
        if self.isLogin:
            self.menu.append("Logout", "app.logout")
            print("Visual Logout option item appended to menu model tree.")
        else:
            print("Visual Logout option item hidden from menu model tree.")

        # =========================================================================
        # FIX 2: Removed self.add_action() from here to prevent duplicate registration lag
        # =========================================================================
        return False




        


    def on_quit_clicked(self, action, parameter):
        print("on_quit_clicked")
        self.fire_notify("Gnome App","Quit Gnome App!")

    def on_restart_clicked(self, action, parameter):
        print("on_restart_clicked")
        self.fire_notify("Gnome App","Restart Gnome App!")

    def on_about_clicked(self, action, parameter):
        print("on_about_clicked")
        about = Adw.AboutWindow(
            application_name="Mein Gnome app",
            version="1.0.0",
            developer_name="Mostafa",
            transient_for=self.get_active_window()
        )
        about.present()

    def on_logout_clicked(self, action, parameter):
        print("on_logout_clicked")
        self.isLogin = False
        # rebuild menu
       
        if hasattr(self, 'root_navigation_stack'):
            #self.root_navigation_stack.set_visible_child_name("login_screen_layout")
            self.root_navigation_stack.set_visible_child_name("auth_layout")
            #self.auth_nav_stack.set_visible_child_name("login_screen_layout")
            print("Session cleared. Interface state locked back to login")
        #self.logout_action.set_enabled(False)
        GLib.idle_add(self.rebuild_menu)
        self.logout_btn.set_visible(False)
        #
        self.fire_notify("Mein Gnome Notify", "Hallo, Wilkommen!!")

    #
    def fire_notify(self, title_msg, body_msg):
        print("fire_notify")

        try:
            notification = Notify.Notification.new(
                title_msg,
                body_msg,
                "dialog-information-symbolic"
            )

            notification.set_urgency(Notify.Urgency.NORMAL)
            notification.show()
            print("Desktop bubble notification success!")

        except Exception as e:
            print(f"Error OS notify: {e}")


    
   
if __name__ == "__main__":
    print("main...")
    app = MyApp()
    app.run()