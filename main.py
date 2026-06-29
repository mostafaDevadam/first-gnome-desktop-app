import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, Adw, Gio, GLib, Gdk, Notify

Notify.init('com.example.myapp')

import re
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
            #
           

"""class HandleJsonFile():

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
"""

class HandleJsonFile:

    def read_json_file(self, populate_ui_cards, folder_name, json_file_name):
        """
        Loads JSON asynchronously in a background thread to prevent UI freezing,
        then dispatches the dataset to the main UI loop via GLib.idle_add.
        """
        file_path = os.path.join(os.getcwd(), folder_name, f"{json_file_name}.json")

        if not os.path.exists(file_path):
            print(f"JSON file does not exist: {file_path}")
            # Safely pass an empty dataset back to clear loading spin indicators
            GLib.idle_add(populate_ui_cards, [])
            return False

        def async_worker():
            try:
                # 1. Open with explicit UTF-8 to safeguard Arabic localization text strings
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                print(f"Data parsed successfully. Size: {len(data)} items.")
                
                # 2. Dispatch UI payload updates safely to the main main loop thread channel
                GLib.idle_add(populate_ui_cards, data)
                
            except Exception as e:
                print(f"ERROR reading/parsing JSON file asynchronously: {e}")
                GLib.idle_add(populate_ui_cards, [])

        # 3. Spin worker task out onto its own execution thread channel to completely eliminate frame lag
        threading.Thread(target=async_worker, daemon=True).start()

    def load_data_from_json_file(self, folder_name, json_file_name):
        """Synchronously reads and returns a parsed list array from disk safely."""
        file_path = os.path.join(os.getcwd(), folder_name, f"{json_file_name}.json")
        
        if os.path.exists(file_path):
            try:
                # Force UTF-8 stream bindings to preserve dynamic character arrays
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading historical database tracking data file: {e}")
                
        return []

    def save_data_to_json_file(self, arr, folder_name, json_file_name):
        """Synchronously dumps data to a localized JSON file with UTF-8 safety."""
        # Ensure parent directory layout layer paths are physically present on disk before writing
        target_dir = os.path.join(os.getcwd(), folder_name)
        os.makedirs(target_dir, exist_ok=True)
        
        file_path = os.path.join(target_dir, f"{json_file_name}.json")

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # ensure_ascii=False saves text natively instead of turning Arabic into hex characters
                json.dump(arr, f, indent=4, ensure_ascii=False)
            print(f"Database array synchronized safely down under: {file_path}")
        except Exception as e:
            print(f"Critical error updating physical JSON datastore block metrics: {e}")

class UserService:

    def __init__(self):
        pass

    
    def get_user_email(self, email):
                   json_file = HandleJsonFile()
                   json_db = json_file.load_data_from_json_file("storage", "accounts")

                   if not json_db:
                       print("no data found for updating profile info")
                       return

                   print(f"json_db data: {json_db}")
                   # get doc based on email
                   account_user = {}
                   #updated_account_user = {}
                   is_account_found = False
                   for account in json_db:
                        if account.get("email") == email:
                           is_account_found = True
                           account_user = account
                           print(f"found account user: {account}")
                           #
                           #account["name"] = name
                           #account["email"] = email
                           #account["username"] = username
                           #account["phone"] = phone
                           #account["website"] = website
                           #
                           #updated_account_user = account
                           
                           #



                        else:
                           is_account_found = False
        
        
                   #
                   return account_user

    def update_user_by_email(self, target_email, data):
                   json_file = HandleJsonFile()
                   json_db = json_file.load_data_from_json_file("storage", "accounts")
                   active_user = {}

                   if not json_db:
                       print("no data found for updating profile info")
                       return

                   print(f"json_db data: {json_db}")
                   # get doc based on email
                   account_user = {}
                   updated_account_user = {}
                   is_account_found = False
                   for idx, account in enumerate(json_db):
                        if account.get("email") == target_email:
                           is_account_found = True
                           account_user = account
                           print(f"found account user: {account}")
                           #
                           #account["name"] = name
                           #account["email"] = email
                           #account["username"] = username
                           #account["phone"] = phone
                           #account["website"] = website
                           #account.clear()
                           json_db[idx] = data
                           #
                           updated_account_user = json_db[idx]
                           break
                           
                           #



                        else:
                           is_account_found = False
                    #
                   if is_account_found:
                        print(f"account user: {account}")
                        print(f"updated_account_user: {updated_account_user}")
                        #
                        
                        #
                        json_file.save_data_to_json_file(json_db, "storage", "accounts")
                        #
                        print(f"after json_db FIXED: {json_db}")
                        #
                        #active_user = updated_account_user
                        #self.active_user = updated_account_user
                        #self.active_username = updated_account_user.get("name")
                        #self.refresh_profile_header()
                        #
                        #if hasattr(self, 'toast_overlay'):
                            #success = self.i18n._("success_update_msg")
                            #self.toast_overlay.add_toast(Adw.Toast.new(success))
                        return updated_account_user
                    #
                   else:
                        #if hasattr(self, 'toast_overlay'):
                            #failed = self.i18n._("failed_update_msg")
                            #self.toast_overlay.add_toast(Adw.Toast.new("Account not found!"))
                        return None


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
                                    #
                                    "tab_home": "Home",
                                    "tab_settings": "Settings",
                                    "tab_profile" : "Profile",
                                    #
                                    "item_test": "Test",
                                    "item_local": "Local",
                                    "item_storage": "Storage",
                                    "item_users": "Users",
                                    "item_posts": "Posts",   # Pure English value mapping
                                    "item_todos": "Todos",
                                    "item_shell": "Shell Terminal",
                                    #
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
                                    #
                                    "login_title": "Login",
                                    "email": "Email",
                                    "password": "Password",
                                    "enter_email": "Enter Email",
                                    "enter_password": "Enter Password",
                                    "validation_password": "Too short! Password must be at least 3 characters.",
                                    "validation_email": "Invalid email format (e.g., user@example.com).",
                                    "password_required": "Password is required",
                                    "email_required": "Email is required",
                                    "login_success_msg": "Login successful! Welcome back.",
                                    "logout_title": "Logout",
                                    "login_failure_msg": "Login failed: Email and password fields cannot be empty.",
                                    #"register_title": "Register",
                                    "register_success_msg": "Account created successfully! Please login.",
                                    "register_failure_msg": "Registration failed: All fields are required.",
                                    #"register_success_msg": "Register successful! Welcome.",
                                    #"register_failure_msg": "Register failed: Email and password fields cannot be empty.",
                                    #
                                    "setting_general_item": "General",
                                    "setting_account_item": "Account",
                                    "setting_notifications_item": "Notifications",
                                    "setting_display_item": "display",
                                    "setting_colors_item": "Colors" ,
                                    "setting_keyboard_item": "Keyboard",
                                    #
                                    "profile_info": "Info",
                                    "profile_address": "Address",
                                    "profile_company": "Company",
                                    #
                                    "register_title": "Create Account",
                                    "username": "Username",
                                    "enter_username": "Enter Username",
                                    "btn_register": "Register",
                                    "switch_to_register": "Don't have an account? Sign Up",
                                    "switch_to_login": "Already have an account? Sign In",
                                    #
                                    "welcome_user": "Welcome", 
                                    #
                                    "success_update_msg": "Success updated!",
                                    #
                                    # Inside your en dictionary:
                                    "username_label": "Username",
                                    "email_label": "Email Address",
                                    "dark_mode": "Dark Theme",
                                    "animations": "Enable Animations",
                                    "notifications_sound": "Play Sound on Alerts",
                                    "accent_color": "Accent Color",
                                    "layout_title": "Keyboard Layout",





                              
                              
                              
                               },
                                "ar": {  # Matches your custom 'self.current_lang = "ar"' target
                                    "posts": "المنشورات",
                                    "posts_mgmt": "إدارة المنشورات",
                                    "add_new": "إضافة عنصر جديد",
                                    "enter_name": "أدخل الاسم...",
                                    "no_items": "لم يتم تسجيل أي عناصر بعد.",
                                    #
                                    "tab_home": "الرئيسية",
                                    "tab_settings": "الاعدادات",
                                    "tab_profile" : "حسابي", #"الملف الشخصي",
                                    #
                                    "item_test": "تجربة",
                                    "item_local": "محلي",
                                    "item_storage": "التخزين",
                                    "item_users": "المستخدمين",
                                    "item_posts": "المنشورات", # Pure Arabic value mapping
                                    "item_todos": "المهام",
                                    "item_shell": "الشل",
                                    "item_text" : "محطة الشل",
                                    #
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
                                    #
                                    "login_title": "دخول",
                                    #"register_title": "تسجيل",
                                    "email": "Email",
                                    "password": "Password",
                                    "enter_email": "ادخل البريد الالكترونى",
                                    "enter_password": "ادخل كلمة السر",
                                    "password_required": "كلمة المرور مطلوبة",
                                    "email_required": "البريد الإلكتروني مطلوب",
                                    "validation_password": "قصيرة جداً! يجب أن تتكون كلمة المرور من 6 أحرف على الأقل.",
                                    "validation_email": "صيغة البريد الإلكتروني غير صالحة (مثال: user@example.com).",


                                    "login_success_msg": "تم تسجيل الدخول بنجاح! مرحبًا بعودتك.",
                                    "logout_title": "خروج",
                                    "login_failure_msg": "فشل تسجيل الدخول: لا يمكن ترك حقول البريد الإلكتروني وكلمة المرور فارغة.",
                                    # setting
                                    "setting_general_item": "عام",
                                    "setting_account_item": "الحساب",
                                    "setting_notifications_item": "الإشعارات",
                                    "setting_display_item": "العرض",
                                    "setting_colors_item": "الألوان",
                                    "setting_keyboard_item": "لوحة المفاتيح",
                                    # profile
                                    "profile_info": "معلومات",
                                    "profile_address": "العنوان",
                                    "profile_company": "الشركة",

                                    #
                                    "register_title": "إنشاء حساب",
                                    "register_success_msg": "تم إنشاء الحساب بنجاح! يرجى تسجيل الدخول.",
                                    "register_failure_msg": "فشل التسجيل: جميع الحقول مطلوبة.",
                                    "username": "اسم المستخدم",
                                    "enter_username": "أدخل اسم المستخدم",
                                    "btn_register": "تسجيل",
                                    "switch_to_register": "ليس لديك حساب؟ سجل الآن",
                                    "switch_to_login": "لديك حساب بالفعل؟ تسجيل الدخول",
                                    #
                                    "welcome_user": "مرحباً",
                                    #
                                    "success_update_msg": "تم التحديث بنجاح!",
                                    #
                                    # Inside your ar dictionary:
                                    "username_label": "اسم المستخدم",
                                    "email_label": "البريد الإلكتروني",
                                    "dark_mode": "المظهر الداكن",
                                    "animations": "تفعيل الحركات",
                                    "notifications_sound": "تشغيل صوت عند التنبيهات",
                                    "accent_color": "اللون الأساسي",
                                    "layout_title": "تخطيط لوحة المفاتيح",


                               
                                },
                                  "de": {
                                    "posts": "Beiträge",
                                    "posts_mgmt": "Beitragsverwaltung",
                                    "add_new": "Neu hinzufügen",
                                    "enter_name": "Name eingeben...",
                                    "no_items": "Noch keine Einträge aufgezeichnet.",
                                    #
                                    "tab_home": "Startseite",
                                    "tab_settings": "Einstellungen",
                                    "tab_profile" : "Konto",  # Fits best in your compact tab bar layout
                                    #
                                    "item_test": "Test",
                                    "item_local": "Lokal",
                                    "item_storage": "Speicher",
                                    "item_users": "Benutzer",
                                    "item_posts": "Beiträge",
                                    "item_todos": "Aufgaben",
                                    "item_shell": "Shell-Terminal",
                                    #
                                    "shell_manager": "System-Shell-Arbeitsbereich",
                                    "shell_run_btn": "Ausführen",
                                    "shell_placeholder": "Shell-Befehl hier eingeben...",
                                    "gnome_app": "Meine Gnome-App",
                                    "search_placeholder": "Einträge suchen...",
                                    "local_manager": "Lokaler Listen-Manager",
                                    "btn_add": "Hinzufügen",
                                    "popover_add_title": "Neu hinzufügen",
                                    "input_name_ph": "Name eingeben...",
                                    "input_desc_ph": "Beschreibung eingeben",
                                    "btn_submit": "Absenden",
                                    "group_title": "Gespeicherte lokale Einträge",
                                    "empty_list_text": "Noch keine Einträge aufgezeichnet. Klicken Sie oben auf 'Hinzufügen', um eine Liste zu erstellen.",
                                    "group_disk_title": "Gespeicherte Daten auf Datenträger mit Einträgen",
                                    "disk_manager": "Datenträger-Listen-Manager",
                                    #
                                    "login_title": "Anmelden",
                                    "email": "E-Mail",
                                    "password": "Passwort",
                                    "enter_email": "E-Mail eingeben",
                                    "enter_password": "Passwort eingeben",
                                    "password_required": "Passwort ist erforderlich",
                                    "email_required": "E-Mail ist erforderlich",
                                    "validation_password": "Zu kurz! Das Passwort muss mindestens 6 Zeichen lang sein.",
                                    "validation_email": "Ungültiges E-Mail-Format (z. B. user@example.com).",


                                    "login_success_msg": "Anmeldung erfolgreich! Willkommen zurück.",
                                    "logout_title": "Abmelden",
                                    "login_failure_msg": "Anmeldung fehlgeschlagen: E-Mail- und Passwortfelder dürfen nicht leer sein.",
                                    "register_success_msg": "Konto erfolgreich erstellt! Bitte einloggen.",
                                    "register_failure_msg": "Registrierung fehlgeschlagen: Alle Felder sind erforderlich.",
                                    # setting
                                    "setting_general_item": "Allgemein",
                                    "setting_account_item": "Konto",
                                    "setting_notifications_item": "Benachrichtigungen",
                                    "setting_display_item": "Anzeige",
                                    "setting_colors_item": "Farben",
                                    "setting_keyboard_item": "Tastatur",
                                    # profile
                                    "profile_info": "Info",
                                    "profile_address": "Adresse",
                                    "profile_company": "Firma",

                                    #
                                    "register_title": "Konto erstellen",
                                    "username": "Benutzername",
                                    "enter_username": "Benutzername eingeben",
                                    "btn_register": "Registrieren",
                                    "switch_to_register": "Kein Konto? Jetzt registrieren",
                                    "switch_to_login": "Bereits ein Konto? Anmelden",
                                    #
                                    "welcome_user": "Willkommen",
                                    #
                                    "success_update_msg": "Erfolgreich aktualisiert!",
                                    #
                                    # Inside your de dictionary:
                                    "username_label": "Benutzername",
                                    "email_label": "E-Mail-Adresse",
                                    "dark_mode": "Dunkles Design",
                                    "animations": "Animationen aktivieren",
                                    "notifications_sound": "Ton bei Benachrichtigungen abspielen",
                                    "accent_color": "Akzentfarbe",
                                    "layout_title": "Tastaturlayout",

                                }

                }



    def _(self, key):
        """ Inline key translator lookup utility """
        # Pull string based on active language, default back to English if missing
        lang_dict = self.translations.get(self.current_lang, self.translations["en"])
        
        # Return the translated text or return the raw key string if not found
        return lang_dict.get(key, self.translations["en"].get(key, key))

# Form
class Form():

    def __init__(self):
        pass




# input-box: build -> params: password-entry or email-entry
class FormField(Gtk.Box):

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)
        self.set_size_request(300, -1)
        #self.build()

    def build(self, entry: Gtk.Entry):
        self.append(entry)

class Validation(Gtk.Label):

    def __init__(self):
        super().__init__()
        self.set_visible(False)
        self.add_css_class("error-msg")

    
    def hide(self):
        self.set_visible(False)

    def visible(self):
        self.set_visible(True)


    

# Field(Input(Validation),Validation)
"""
f = Field()
v = Validation()
i = Input(v)
f.append(i)
f.append(v)

"""

# password-entry
class InputPassword(Gtk.PasswordEntry):

    def __init__(self, app, validation: Validation, placeholder_text, ):
        super().__init__()
        self.validation = validation
        #self.set_placeholder_text(placeholder_text)
        self.placeholder_text = placeholder_text
        #self.input_box = FormField()
        #self.input_box.append(self)
        #self.form = form
        self.app = app
        #
        self.build()


    def build(self):
        #password_entry = Gtk.PasswordEntry(placeholder_text="enter pass")
        
        #self.add_css_class("error")
        # Set maximum length to 8 characters
        text_widget = self.get_delegate()
        #text_widget.set_placeholder_text("Enter 3 to 8 characters")
        text_widget.set_placeholder_text(self.placeholder_text)
        text_buffer = text_widget.get_buffer()
        text_buffer.set_max_length(8)

        # Connect to the changed signal to validate the minimum length
        self.connect("notify::text", self.on_password_changed)
        #self.input_box.append(self)
        # validation password
        #self.validation_pass_lbl = Gtk.Label()
        #self.validation_pass_lbl.set_visible(False)
        #self.validation_pass_lbl.add_css_class("error-msg")
        #self.validation_pass_lbl.add_css_class("visible")
        #self.input_box.append(self.validation_pass_lbl)
        #self.validation_pass_lbl = Gtk.Label()
        #self.input_box.append(self.validation_pass_lbl)
        #
        #return self

    #def get(self):
        #return self



    def on_password_changed(self, entry, pspec):
        text = entry.get_text()
        print(f"on_password_changed: {text}")

        #
        if len(text) == 0:
            entry.add_css_class("error")  
            #self.validation_pass_lbl.set_text("Password is required")
            #self.validation_pass_lbl.set_visible(True)
            self.validation.set_text("Password is required")
            self.validation.visible()
        elif len(text) < 3:
            entry.add_css_class("error")
            #self.validation_pass_lbl.set_text("Too short! Password must be at least 3 characters.")
            #self.validation_pass_lbl.set_visible(True)
            self.validation.set_text("Too short! Password must be at least 3 characters.")
            self.validation.visible()
        else:
            entry.remove_css_class("error")
            #self.validation_pass_lbl.set_visible(False)
            self.validation.hide()

class InputBasicPassword(Gtk.Entry):

    def __init__(self, app, placeholder_text, validation: Validation):
         super().__init__(placeholder_text=placeholder_text)
         #self.input_login_pass = Gtk.Entry(placeholder_text=self.app.i18n._("enter_password"))
         self.app = app
         self.validation = validation
         self.set_visibility(False)
         self.set_input_purpose(Gtk.InputPurpose.PASSWORD)
         self.connect("notify::text", self.on_password_changed)
         self.isValid = False
        

    def on_password_changed(self, entry, pspec):
        text = entry.get_text()
        print(f"on_password_changed: {text}")

        #
        if len(text) == 0:
            entry.add_css_class("error")  
            #self.validation_pass_lbl.set_text("Password is required")
            #self.validation_pass_lbl.set_visible(True)
            #self.validation.set_text("Password is required") #self.app.i18n._("password_required")
            self.validation.set_text(self.app.i18n._("password_required"))
            self.app.register_widget(self.validation, "label", "password_required")
            # self.app.register_widget(self.validation, "label", "password_required")
            self.validation.visible()
        elif len(text) < 6:
            entry.add_css_class("error")
            #self.validation_pass_lbl.set_text("Too short! Password must be at least 3 characters.")
            #self.validation_pass_lbl.set_visible(True)
            #self.validation.set_text("Too short! Password must be at least 6 characters.") #self.app.i18n._("validation_login_password")
            # self.app.register_widget(self.validation, "label", "validation_login_password")
            self.validation.set_text(self.app.i18n._("validation_password"))
            self.app.register_widget(self.validation, "label", "validation_password")
            #
            self.validation.visible()
            self.isValid = False
        else:
            entry.remove_css_class("error")
            #self.validation_pass_lbl.set_visible(False)
            self.validation.hide()
            self.isValid = True


EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class InputBasicEmail(Gtk.Entry):

    def __init__(self, app, placeholder_text, validation: Validation):
        super().__init__(placeholder_text=placeholder_text)
        self.app = app
        self.validation = validation
        self.set_input_purpose(Gtk.InputPurpose.EMAIL)
        self.connect("notify::text", self.on_email_changed)
        self.isValid = False
    
    def on_email_changed(self, entry, pspec):
        text = entry.get_text()
        print(f"on_email_changed: {text}")

        #
        if len(text) == 0:
            entry.add_css_class("error")  
            #self.validation_pass_lbl.set_text("Password is required")
            #self.validation_pass_lbl.set_visible(True)
            #self.validation.set_text("Email is required") #self.app.i18n._("email_required")
            self.validation.set_text(self.app.i18n._("email_required"))
            self.app.register_widget(self.validation, "label", "email_required")
            # self.app.register_widget(self.validation, "label", "password_required")
            self.validation.visible()
        elif not re.match(EMAIL_REGEX, text):
                entry.add_css_class("error")
                #self.validation.set_text("Invalid email format (e.g., user@example.com).")
                self.validation.set_text(self.app.i18n._("validation_email"))
                self.app.register_widget(self.validation, "label", "validation_email")
                self.validation.visible()
                self.isValid = False
                

                """elif len(text) < 15:
                    entry.add_css_class("error")
                    #self.validation_pass_lbl.set_text("Too short! Password must be at least 3 characters.")
                    #self.validation_pass_lbl.set_visible(True)
                    self.validation.set_text("Too short! Email must be at least 15 characters.") #self.app.i18n._("validation_login_password")
                    # self.app.register_widget(self.validation, "label", "validation_login_password")
                    #
                    self.validation.visible()"""
        
        else:
            entry.remove_css_class("error")
            #self.validation_pass_lbl.set_visible(False)
            self.validation.hide()
            self.isValid = True
        
        

# AuthForm: form-title, fields: name(register), email, password
class AuthForm(Gtk.Box):

    def __init__(self, app, auth, isRegister, title, submit_btn_title, submit_event):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)
        self.set_size_request(300, -1)
        self.app = app
        self.auth = auth
        #
        self.isRegister = isRegister
        self.title = title
        #
        self.on_submit_button_clicked = submit_event
        self.submit_btn_title = submit_btn_title

        #
        self.build()


    
    def build(self):
        # title
        title_lbl = Gtk.Label(label=self.title)
        title_lbl.add_css_class("title-1")
        title_lbl.set_margin_bottom(12)
        self.app.register_widget(title_lbl, "label", self.title)
        self.append(title_lbl)

        if self.isRegister:
           # input name
            name_form_field = FormField()
            validation_name = Validation()
            self.input_name = Gtk.Entry()
            self.input_name.set_input_purpose(Gtk.InputPurpose.NAME)
            self.app.register_widget(self.input_name, "placeholder", "enter_name")
            #self.input_name = InputBasicName(app=self.app, placeholder_text=self.app.i18n._("enter_name"), validation=validation_name)
            #self.app.register_widget(self.input_name, "placeholder", "enter_name")
            name_form_field.append(self.input_name)
            name_form_field.append(validation_name)
            self.append(name_form_field)

           

        # input email
        email_form_field = FormField()
        validation_email = Validation()
        self.input_email = InputBasicEmail(app=self.app, placeholder_text=self.app.i18n._("enter_email"), validation=validation_email)
        self.app.register_widget(self.input_email, "placeholder", "enter_email")
        email_form_field.append(self.input_email)
        email_form_field.append(validation_email)
        self.append(email_form_field)

        # input password
        pass_form_field = FormField()
        validation_password = Validation()
        self.input_pass = InputBasicPassword(app=self.app, placeholder_text=self.app.i18n._("enter_password"), validation=validation_password)
        pass_form_field.append(self.input_pass)
        pass_form_field.append(validation_password)
        self.append(pass_form_field)

        # btn
        self.submit_btn = Gtk.Button() #(label="login_title")
        self.app.register_widget(self.submit_btn, "label", self.submit_btn_title )
        self.submit_btn.add_css_class("suggested-action")
        #self.login_btn.add_css_class("login_btn")
        self.submit_btn.set_margin_top(8)
        self.submit_btn.connect("clicked", self.on_submit)
        self.append(self.submit_btn)

        # if register
        if self.isRegister:
             # link to switch to login screen layout
            to_login_btn = Gtk.Button()
            to_login_btn.set_has_frame(False)
            to_login_btn.set_margin_top(4)
            self.app.register_widget(to_login_btn, "label", "switch_to_login")
            to_login_btn.connect("clicked", lambda x: self.auth.auth_nav_stack.set_visible_child_name("login_screen_layout"))
            self.append(to_login_btn)
        else:
             # link to switch to register screen layout
            to_register_btn = Gtk.Button()
            to_register_btn.set_has_frame(False)
            to_register_btn.set_margin_top(4)
            self.app.register_widget(to_register_btn, "label", "switch_to_register")
            to_register_btn.connect("clicked", lambda x: self.auth.auth_nav_stack.set_visible_child_name("register_screen_layout"))
            self.append(to_register_btn)

    def on_submit(self, button):
        input_email = self.input_email
        input_pass = self.input_pass
        email = input_email.get_text().strip()
        password = input_pass.get_text().strip()

        print(f"login password: {password}")

        if (self.isRegister and (not self.input_name or not email or not password)) or (not self.isRegister and (not email or not password)) :
            print("Authentication Failure Email or Password is incorrect")
            self.app.isLogin = False
            self.app.logout_btn.set_visible(False)
            failure_msg = self.app.i18n._("login_failure_msg") 
            failure_toast = Adw.Toast.new(failure_msg)
            failure_toast.set_timeout(3)
            self.app.toast_overlay.add_toast(failure_toast)
            return
        #
        if not input_email.isValid or not input_pass.isValid:
            print("Authentication Failure Email or Password is invalid")
            self.app.isLogin = False
            self.app.logout_btn.set_visible(False)
            failure_msg = self.app.i18n._("login_failure_msg") 
            failure_toast = Adw.Toast.new(failure_msg)
            failure_toast.set_timeout(3)
            self.app.toast_overlay.add_toast(failure_toast)
            return
        # callback
        self.on_submit_button_clicked(button)



        



# Auth component
class AuthComponent(Gtk.Box):

    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.app = app
        #
        # stacks
        # 1. auth stack
        self.auth_nav_stack = Gtk.Stack()
        self.auth_nav_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.auth_nav_stack.set_transition_duration(250)
        self.append(self.auth_nav_stack)
        #self.auth_nav_stack.add_named(login_box, "login_screen_layout")
        #self.auth_nav_stack.add_named(register_box, "register_screen_layout")
        #active layout in auth stack is login_screen_layout
        #self.auth_nav_stack.set_visible_child_name("register_screen_layout")   
        #
        self.handle_json_file = HandleJsonFile()
        #
        self.build_login_layout()
        self.build_register_layout()
        #
        self.active_username = ""
        #



    def build_login_layout(self):
        # login
        self.login_form = AuthForm(app=self.app, auth=self, isRegister=False,title="login_title", 
                                   submit_btn_title="login_title",submit_event=self.on_login_button_clicked)
        self.auth_nav_stack.add_named(self.login_form, "login_screen_layout")

   

    def build_register_layout(self):
        # register
        self.register_form = AuthForm(app=self.app, auth=self, isRegister=True,title="register_title", 
                                      submit_btn_title="btn_register", submit_event=self.on_register_button_clicked)
        self.auth_nav_stack.add_named(self.register_form, "register_screen_layout")


    def test_submit(self, button):
        print("test_submit")
        pass

    def on_login_button_clicked(self, button):
        #email = self.input_login_email.get_text().strip()
        #password = self.input_login_pass.get_text().strip()
        input_login_email = self.login_form.input_email
        input_login_pass = self.login_form.input_pass
        email = input_login_email.get_text().strip()
        password = input_login_pass.get_text().strip()

        print(f"login password: {password}")

        """if not email or not password :
            print("Authentication Failure Email or Password is incorrect")
            self.app.isLogin = False
            self.app.logout_btn.set_visible(False)
            failure_msg = self.app.i18n._("login_failure_msg") 
            failure_toast = Adw.Toast.new(failure_msg)
            failure_toast.set_timeout(3)
            self.app.toast_overlay.add_toast(failure_toast)
            return
        #
        if not input_login_email.isValid or not input_login_pass.isValid:
            print("Authentication Failure Email or Password is invalid")
            self.app.isLogin = False
            self.app.logout_btn.set_visible(False)
            failure_msg = self.app.i18n._("login_failure_msg") 
            failure_toast = Adw.Toast.new(failure_msg)
            failure_toast.set_timeout(3)
            self.app.toast_overlay.add_toast(failure_toast)
            return"""

        #
        

        # check login in json file
        base_dir = GLib.get_current_dir()
        storage_dir = os.path.join(base_dir, "storage")
        file_path = os.path.join(storage_dir, "accounts.json")

        #
        if not os.path.exists(file_path):
            error_text = self.app.i18m._("login_failure_msg")
            self.app.toast_overlay.add_toast(Adw.Toast.new(error_text))
            return
        #
        authenticated = False
        active_username = "username"
        active_user = {}
        #
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                db = json.load(f)

                #
                if isinstance(db, list):
                    for account in db:
                        if account.get("email") == email and account.get("password") == password:
                            authenticated = True
                            active_username = account.get("name")
                            active_user = account
                            #self.app.profile_lbl.set_text(active_username)
                            break

        except Exception as e:
            print(f"Error Login: {e}")
            self.app.toast_overlay.add_toast(Adw.Toast.new("Database Error"))
        #
        if authenticated:
            print(f"Authentication success for profile")
            self.app.isLogin = True
            self.app.logout_btn.set_visible(True)
            # pass active_username to profile-label
            #self.app.profile_lbl.set_text(active_username)
            self.active_username = active_username
            print(f"self.active_username: {self.active_username} , active_username: {active_username}")
            self.app.active_username = active_username
            self.app.active_user = active_user
            #
            print(f"active user: {active_user} , app.active_user: {self.app.active_user}")
            self.app.refresh_profile_header()
            # config for autologin
            json_file = HandleJsonFile()
            config_data = {
                "auto_login": True,
                "saved_email": email,
            }
            json_file.save_data_to_json_file(config_data, "storage", "config")
            #
            # clear inputs
            #self.input_login_email.set_text("")
            #self.input_login_pass.set_text("")
            input_login_email.set_text("")
            input_login_pass.set_text("")
            #
            print("Layout interface canvas unlocked.")
            #
            success_message = self.app.i18n._("login_success_msg") 
            toast = Adw.Toast.new(success_message)
            toast.set_timeout(3)
            self.app.toast_overlay.add_toast(toast)
            #
            #self.menu.append("Logout", "app.logout")
            #self.app.rebuild_menu()
            #GLib.idle_add(self.app.rebuild_menu)
            self.app.main_menu_component.rebuild_menu()
           

            #
            self.app.fire_notify("Mein Gnome Login", "Login in success for Mein Gnome App!")
            #
            self.app.root_navigation_stack.set_visible_child_name("main_layout")
        else:
            error_text = self.app.i18n._("login_failure_msg")
            self.app.toast_overlay.add_toast(Adw.Toast.new(error_text))

    def on_password_changed(self, entry, pspec):
        text = entry.get_text()
        print(f"on_password_changed: {text}")

        #
        """if len(text) == 0:
            entry.add_css_class("error")  
            self.validation_pass_lbl.set_text("Password is required")
            self.validation_pass_lbl.set_visible(True)
        elif len(text) < 3:
            entry.add_css_class("error")
            self.validation_pass_lbl.set_text("Too short! Password must be at least 3 characters.")
            self.validation_pass_lbl.set_visible(True)
        else:
            entry.remove_css_class("error")
            self.validation_pass_lbl.set_visible(False)"""

    def on_register_button_clicked(self, button):
        #name = self.input_register_name.get_text().strip()
        #email = self.input_register_email.get_text().strip()
        #password = self.input_register_pass.get_text().strip()

        input_register_email = self.register_form.input_email
        input_register_pass = self.register_form.input_pass
        input_register_name = self.register_form.input_name
        name = input_register_name.get_text().strip()
        email = input_register_email.get_text().strip()
        password = input_register_pass.get_text().strip()

        
        #
        #self.isLogin = True
        #self.logout_btn.set_visible(True)
        #self.logout_action.set_enabled(True)

        # save
        user = {
            "name": name,
            "email": email,
            "password": password,
        }
        print(f"regsitered user: {user}")
        print(f"regsitered : name: {name} , email: {email}, password: {password}")
        #self.handle_json_file.save_data_to_json_file()
        base_dir = GLib.get_current_dir()
        storage_dir = os.path.join(base_dir, "storage")
        file_path = os.path.join(storage_dir, "accounts.json")
        #file_path = os.path.join(GLib.get_current_dir(), f"./storage/accounts.json")
        
        os.makedirs(storage_dir, exist_ok=True)

        db = []

        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    
                    try:
                        db = json.load(f)
                        if not isinstance(db, list):
                            db = []
                    except json.JSONDecodeError:
                        db = []
                       
        except Exception as e:
            print(f"Error saving data file: {e}")
            db = []

        
        db.append(user)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=4, ensure_ascii=False)
                print(f"User account addedd successfully under: {file_path}")
        except Exception as e:
            print(f"Critical error writing updated json {e}")   


        

        # clear inputs
        input_register_email.set_text("")
        input_register_pass.set_text("")
        input_register_name.set_text("")
        #
        print("Layout interface canvas unlocked.")
        #
        success_message = self.app.i18n._("register_success_msg")
        toast = Adw.Toast.new(success_message)
        toast.set_timeout(3)
        self.app.toast_overlay.add_toast(toast)
        #
        self.auth_nav_stack.set_visible_child_name("login_screen_layout")
        #
        #self.menu.append("Logout", "app.logout")
        #self.rebuild_menu()
        #GLib.idle_add(self.rebuild_menu)

# MenuLanguagesComponent 
class MenuLanguagesComponent(Gio.Menu):

      def __init__(self, app):
           super().__init__()
           self.app = app
           #
           self.build_menu_items()
           self.register_statful_action()


      def build_menu_items(self):
          # menu: language-switcher 
            #menu_lang = Gio.Menu.new()
            """menu_lang.append("English", "app.lang::en")
            menu_lang.append("Deutsch (German)", "app.lang::de")
            menu_lang.append("العربية (Arabic)", "app.lang::ar")"""
        

            # English item
            en_item = Gio.MenuItem.new("English", "app.lang::en")
            en_item.set_attribute_value("icon", GLib.Variant.new_string("preferences-desktop-locale-symbolic"))
            self.append_item(en_item)

            # German Item
            de_item = Gio.MenuItem.new("Deutsch (German)", "app.lang::de")
            de_item.set_attribute_value("icon", GLib.Variant.new_string("preferences-desktop-locale-symbolic"))
            self.append_item(de_item)

            
            # Arabic item
            ar_item = Gio.MenuItem.new("العربية (Arabic)", "app.lang::ar")
            ar_item.set_attribute_value("icon", GLib.Variant.new_string("preferences-desktop-locale-symbolic"))
            self.append_item(ar_item)

            

            
            #header_bar.pack_end(lang_menu_button)
            #
      def register_statful_action(self):
            # Create action
            lang_action = Gio.SimpleAction.new_stateful(
                "lang",
                GLib.VariantType.new("s"),
                GLib.Variant.new_string("en")
            )
            lang_action.connect("activate", self.on_language_action_activated)
            self.app.add_action(lang_action)
          

      def get_menu_button(self):
            lang_menu_button = Gtk.MenuButton()
            lang_menu_button.set_icon_name("preferences-desktop-locale-symbolic")
            lang_menu_button.set_menu_model(self)
            return lang_menu_button
            


      def on_language_action_activated(self, action, parameter):
            print("on_language_action_activated")
            #
            lang_code = parameter.get_string()
            print(f"lang_code: {lang_code}")
            action.set_state(GLib.Variant.new_string(lang_code))
            #action.set_state(parameter)
            self.app.change_app_language(lang_code)
            #
                     

    
class CardComponent(Adw.ActionRow):

    def __init__(self):
        super().__init__()
        #self.app = app

    
    def build(self, item, icon_name, state):
        # 
        if state == "test":
           self.set_title(item.get("title", state))
           self.set_subtitle(item.get("author", state))
           self.set_subtitle(str(item.get("year", 0)))
        elif state == "users":
           self.set_title(item.get("name", state))
           self.set_subtitle(item.get("email", state))
        elif state == "posts":
             self.set_title(item.get("title", state))
             self.set_subtitle(item.get("body", state))
        elif state == "comments":
            self.set_title(item.get("name", state))
            self.set_subtitle(item.get("body", state))
        elif state == "todos":
            self.set_title(item.get("title", state))


        # icon
        self.add_prefix(Gtk.Image.new_from_icon_name(icon_name))

        
class MainMenuComponent(Gio.Menu):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setup_actions()
        self.build()


    def build(self):
        self.remove_all()

        # =========================================================================
        # FIX 1: Reuse or instantiate your menu container model shell cleanly
        # =========================================================================

        # 1. Append global navigation options common to both application states
        self.append("About", "app.about")
        self.append("Quit", "app.quit")
        self.append("Restart", "app.restart")

        # 2. Append conditional menu entries based on active authentication parameters
        if getattr(self.app, 'isLogin', False):
            self.append("Logout", "app.logout")
            print("Visual Logout option item appended to menu model tree.")
        else:
            print("Visual Logout option item hidden from menu model tree.")

        # =========================================================================
        # FIX 2: Removed self.add_action() from here to prevent duplicate registration lag
        # =========================================================================
        return False

    def setup_actions(self):
        """ Registers all application framework GActions EXACTLY ONCE on startup """
        print("Initializing master GAction registration pipeline...")

        # 1. Register your system default helper actions (About, Quit, Restart)
        # ... (your existing action setups for about, quit, restart) ...
        # Quite Action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.app.on_quit_clicked)
        self.app.add_action(quit_action)

        # About Action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.app.on_about_clicked)
        self.app.add_action(about_action)

        # restart Action
        if not self.app.lookup_action("restart"):
            restart_action = Gio.SimpleAction.new("restart", None)
            restart_action.connect("activate", lambda action, param:  self.app.fire_notify("Gnome App","Restart Gnome App") )
            self.app.add_action(restart_action)
        # Logout Action
        if not self.app.lookup_action("logout"):
            logout_action = Gio.SimpleAction.new("logout", None)
            logout_action.connect("activate", self.app.on_logout_clicked)
            self.app.add_action(logout_action)
            print("System Logout action successfully registered to app scope runtime channels.")


    def rebuild_menu(self):
         GLib.idle_add(self.build)
         

    def get_menu_button(self):
        # menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_menu_model(self)
        menu_button.set_icon_name("open-menu-symbolic")
        return menu_button


class ListBoxComponent(Gtk.ListBox):

    def __init__(self):
        super().__init__()

    def build(self, css_class_name):
        pass


class TabBox(Gtk.Box):

    def __init__(self, app, wrapper_title, key, icon_name):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.app = app
        self.page_wrapper = self.app.view_stack.add_titled(self, wrapper_title, self.app.i18n._(key))
        self.page_wrapper.set_icon_name(icon_name) 
        self.app.register_widget(self.page_wrapper, 'title', key)
        #
        """if wrapper_title == "profile":
            row = Adw.ActionRow()
            self.append(row)"""
        #    

    def build(self, list_box: Gtk.ListBox, items, nav_rows):
        
        for key, icon_name in items:
            row = Adw.ActionRow()
            
            # Initial text mapping on initialization canvas
            row.set_title(self.app.i18n._(key))
            #row.set_title(key)
            row.set_activatable(True)

            # Store the translation key identifier tag property on the row instance
            row.nav_item_key_id = key

            prefix_icon = Gtk.Image.new_from_icon_name(icon_name)
            row.add_prefix(prefix_icon)

            suffix_arrow = Gtk.Image.new_from_icon_name("go-next-symbolic")
            row.add_suffix(suffix_arrow)

            row.connect("activated", self.app.on_home_item_clicked)

            list_box.append(row)
            
            # Save a link to this row matching its translation tracking key
            nav_rows[key] = row
        self.append(list_box) # tab3_box.append(self.list3_box)
        
        return nav_rows
    


class SearchBarComponent(Gtk.Box):

    def __init__(self, app):
        super().__init__()
        self.app = app
        #
        self.build()


    def build(self):
         # search-bar
        #search_bar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.sidebar_search_entry = Gtk.SearchEntry()
        self.sidebar_search_entry.set_hexpand(True)
        self.sidebar_search_entry.set_placeholder_text(self.app.i18n._("search_placeholder"))
        self.sidebar_search_entry.connect("search-changed", self.app.on_sidebar_search_changed)
        self.app.register_widget(self.sidebar_search_entry, 'placeholder', 'search_placeholder')

        self.append(self.sidebar_search_entry)

    
    
class LoadingBoxComponent(Gtk.Box):

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.build()
    
    def build(self):
        #loading_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_valign(Gtk.Align.CENTER)
        spinner = Gtk.Spinner()
        spinner.start()
        spinner.set_size_request(40, 40)
        self.append(spinner)
        loading_label = Gtk.Label(label="Fetching live user cards...")
        self.append(loading_label)
    

#
class TestViewClass():

    def __init__(self, app):
        self.app = app
        self.handle_json_file = HandleJsonFile()
        self.build()

    
    def build(self):
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
        self.app.test_items_group.set_title("test ui")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(self.app.test_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.app.center_stack.add_named(local_wrapper, "local_test_view")

        


        def test_fetch():
            print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            

            def card_clicked(row):
                print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.app.right_sidebar.get_first_child():
                    self.app.right_sidebar.remove(child)
                #
                self.app.right_sidebar.set_margin_top(16)
                self.app.right_sidebar.set_margin_start(12)
                self.app.right_sidebar.set_margin_end(12)
                self.app.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.app.right_sidebar.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("author"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                self.app.right_sidebar.append(body_label)
                #
                print(f"item year: {item.get("year")}")
                year_label = Gtk.Label(label=str(item.get("year", 0)))
                year_label.add_css_class("dim-label") # built-in font bold
                year_label.set_margin_bottom(24)
                year_label.set_halign(Gtk.Align.START)
                year_label.set_wrap(True)
                self.app.right_sidebar.append(year_label)
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
                        self.app.test_items.append(item)
                        c = CardComponent()
                        #
                        #card = Adw.ActionRow()
                        #c.set_title(item.get("title", "test"))
                        c.build(item, "text-x-generic-symbolic", "test")
                        #c.set_subtitle(item.get("author", "test"))
                        #c.set_subtitle(str(item.get("year", 0)))
                        c.set_activatable(True)
                        c.payload = item
                        c.connect("activated", card_clicked)
                        #c.add_prefix(Gtk.Image.new_from_icon_name("text-x-generic-symbolic"))
                        self.app.test_items_group.add(c)
                    
                    # --- ACTION TAKEN HERE ---
                    # Now that docs is populated, safely trigger your UI updates or prints:
                    #print(f"len docs inside callback: {len(docs)}")

                self.app.test_items_group.queue_resize()
            

            #self.read_json_file(populate_ui_cards, "data", "test")
            self.handle_json_file.read_json_file(populate_ui_cards, "data", "test")
            #print(f"read_json: {data}")
            #
            
            


            return False # Stop the GLib idle loop from repeating this function
        
        # Queue the function to run as soon as the main loop is ready
        GLib.idle_add(test_fetch)
        
    def card_clicked(self, row):
                print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.app.right_sidebar.get_first_child():
                    self.app.right_sidebar.remove(child)
                #
                self.app.right_sidebar.set_margin_top(16)
                self.app.right_sidebar.set_margin_start(12)
                self.app.right_sidebar.set_margin_end(12)
                self.app.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.app.right_sidebar.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("author"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                self.app.right_sidebar.append(body_label)
                #
                print(f"item year: {item.get("year")}")
                year_label = Gtk.Label(label=str(item.get("year", 0)))
                year_label.add_css_class("dim-label") # built-in font bold
                year_label.set_margin_bottom(24)
                year_label.set_halign(Gtk.Align.START)
                year_label.set_wrap(True)
                self.app.right_sidebar.append(year_label)
                #sidebar_group = Adw.PreferencesGroup()
                #sidebar_group.set_title("User Information")

               
                # inject the completed data card into right-sidebar
                #self.right_sidebar.append(sidebar_group)
                #
                #sidebar_group.set_margin_start(8)
                #sidebar_group.set_margin_end(8)

class UsersViewClass():

    def __init__(self, app):
        self.app = app
        self.handle_json_file = HandleJsonFile()
        self.build()

    def build(self):
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
        self.app.local_users_group.set_title("Users")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(self.app.local_users_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.app.center_stack.add_named(local_wrapper, "local_test_users_view")


           


        def test_fetch():
            #print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add

            def card_clicked(row):
                #print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.app.right_sidebar.get_first_child():
                    self.app.right_sidebar.remove(child)
                #
                self.app.right_sidebar.set_margin_top(16)
                self.app.right_sidebar.set_margin_start(12)
                self.app.right_sidebar.set_margin_end(12)
                self.app.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("name"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.app.right_sidebar.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("email"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                self.app.right_sidebar.append(body_label)
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
                self.app.right_sidebar.append(sidebar_group)
                #
                sidebar_group.set_margin_start(8)
                sidebar_group.set_margin_end(8)

            def populate_ui_cards(data):
                for item in data:
                           
                        self.app.local_users_items.append(item)
                        c = CardComponent()
                        c.build(item, "text-x-generic-symbolic", "users")
                        c.set_activatable(True)
                        c.payload = item
                        c.connect("activated", self.user_card_clicked)
                        self.app.local_users_group.add(c)
                        #
                    
                    

                self.app.local_users_group.queue_resize()


            #self.read_json_file(populate_ui_cards, "data", "users")
            self.handle_json_file.read_json_file(populate_ui_cards, "data", "users")

            

            return False # Stop the GLib idle loop from repeating this function
        
        # Queue the function to run as soon as the main loop is ready
        GLib.idle_add(test_fetch)
    
    #
    def user_card_clicked(self, row):
                #print(f"user_card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.app.right_sidebar.get_first_child():
                    self.app.right_sidebar.remove(child)
                #
                self.app.right_sidebar.set_margin_top(16)
                self.app.right_sidebar.set_margin_start(12)
                self.app.right_sidebar.set_margin_end(12)
                self.app.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("name"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.app.right_sidebar.append(title_label)
                #
                body_label = Gtk.Label(label=item.get("email"))
                body_label.add_css_class("dim-label") # built-in font bold
                body_label.set_margin_bottom(24)
                body_label.set_halign(Gtk.Align.START)
                body_label.set_wrap(True)
                self.app.right_sidebar.append(body_label)
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
                self.app.right_sidebar.append(sidebar_group)
                #
                sidebar_group.set_margin_start(8)
                sidebar_group.set_margin_end(8)
       
class TodosViewClass():

    def __init__(self, app):
        self.app = app
        self.handle_json_file = HandleJsonFile()
        self.build()

    def build(self):
        #
        #print(f"state#: {self.state}")
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

        #self.local_todos_group = Adw.PreferencesGroup()
        self.app.local_todos_group.set_title("Todos")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(self.app.local_todos_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.app.center_stack.add_named(local_wrapper, "local_test_todos_view")


        


        def test_fetch():
            #print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add

            def card_clicked(row):
                print(f"card_clicked: {row.payload}")

                item = row.payload

                #
                while child := self.app.right_sidebar.get_first_child():
                    self.app.right_sidebar.remove(child)
                #
                self.app.right_sidebar.set_margin_top(16)
                self.app.right_sidebar.set_margin_start(12)
                self.app.right_sidebar.set_margin_end(12)
                self.app.right_sidebar.set_margin_bottom(16)
                #
                title_label = Gtk.Label(label=item.get("title"))
                title_label.add_css_class("title-1") # built-in font bold
                title_label.set_margin_bottom(12)
                title_label.set_halign(Gtk.Align.START)
                self.app.right_sidebar.append(title_label)
                #
                
            def populate_ui_cards(data):
                for item in data:
                        c = CardComponent()
                        c.build(item, "text-x-generic-symbolic", "todos")
                        self.app.local_todos_items.append(item)
                        c.set_activatable(True)
                        c.payload = item
                        c.connect("activated", card_clicked)
                        self.app.local_todos_group.add(c)
                    
                    
                    

                self.app.local_todos_group.queue_resize()
            self.handle_json_file.read_json_file(populate_ui_cards, "data", "todos")
            #
            return False # Stop the GLib idle loop from repeating this function
        
        # Queue the function to run as soon as the main loop is ready
        GLib.idle_add(test_fetch)


class PostsViewClass():

    def __init__(self, app):
         self.app = app
         self.handle_json_file = HandleJsonFile()
         self.build()
         self.comments_view_class = CommentsViewClass()



    def build(self):
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
        #self.local_posts_group = Adw.PreferencesGroup()
        self.app.local_posts_group.set_title("Posts")

        content_box.append(self.app.local_posts_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        self.app.center_stack.add_named(local_wrapper, "local_test_posts_view")

        # Context-isolated click row callback handler
        def card_clicked(row):
            print(f"card_clicked: {row.payload}")
            item = row.payload

            while child := self.app.right_sidebar.get_first_child():
                self.app.right_sidebar.remove(child)
            
            self.app.right_sidebar.set_margin_top(16)
            self.app.right_sidebar.set_margin_start(12)
            self.app.right_sidebar.set_margin_end(12)
            self.app.right_sidebar.set_margin_bottom(16)
            
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

            #self.build_test_comments_by_postId_view(main_box, item.get("id"))
            self.comments_view_class.build_by_postId(main_box, item.get("id"))

            self.app.right_sidebar.append(main_box)
            self.app.right_sidebar.set_vexpand(True)
            self.app.right_sidebar.set_hexpand(False)

        # Thread-safe function to build individual rows onto the UI loop
        # Thread-safe function to build individual rows onto the UI loop
        def populate_ui_cards(posts_data):
            print("Populating UI cards cleanly...")

            # =========================================================================
            # 1. BULLETPROOF CLEAR: Clear out EVERYTHING attached inside content_box
            # =========================================================================
            # This climbs out of your group to the parent container box, and completely 
            # flushes every single layout element on screen so duplication or warnings are impossible.
            if hasattr(self, 'local_posts_group') and self.app.local_posts_group.get_parent():
                content_box = self.app.local_posts_group.get_parent()
                
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
                self.app.local_posts_group = Adw.PreferencesGroup()
                self.app.local_posts_group.set_title("Posts")
                content_box.append(self.app.local_posts_group)

            # -------------------------------------------------------------------------
            # 2. POPULATE CARDS: Draw brand-new ActionRow cards on the clean layout
            # -------------------------------------------------------------------------
            for item in posts_data:
                self.app.local_posts_items.append(item)
                c = CardComponent()
                c.build(item, "text-x-generic-symbolic", "posts")
                c.set_activatable(True)
                # Bind item payload context directly to row object
                c.payload = item
                c.connect("activated", card_clicked)
                self.app.local_posts_group.add(c)
            
            # Force layout refresh and switch focus state
            self.app.local_posts_group.set_visible(True)
            self.app.local_posts_group.queue_resize()
            return False

        # Background processing worker thread function
        def test_fetch_worker():
            print("test_fetch worker running in thread background...")
            import threading
            import time
            
            # Safe non-blocking delay inside thread
            time.sleep(0.1)  
            
           

            #
            #self.read_json_file(populate_ui_cards, "data", "posts")
            self.handle_json_file.read_json_file(populate_ui_cards, "data", "posts")
            


            

        # Fire off the data fetch routine inside a detached background worker thread
        worker_thread = threading.Thread(target=test_fetch_worker, daemon=True)
        worker_thread.start()


class CommentsViewClass():

    def __init__(self):
        #self.app = app
        self.handle_json_file = HandleJsonFile()
        

    def build_by_postId(self, parent_container, postId):
       print(f"build_test_comments_by_postId_view : {postId}")
       #
       def test_fetch():
            print("test_fetch")
            import time


            #for child in self.right_sidebar.observe_children():
                    #self.right_sidebar.remove(child)

            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add

           

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
                            c = CardComponent()
                            c.build(item, "text-x-generic-symbolic", "comments")
                            c.set_activatable(False)
                            c.set_margin_bottom(5)
                            comments_group.add(c)
                    
                    
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
        self.nav_profile_rows = {}
        #
        self.isLogin = False
        self.logout_btn = Gtk.Button(label=self.i18n._('logout_title'))
        #self.logout_action = Gio.SimpleAction.new("logout", None)
        #
        self.menu = Gio.Menu.new()
        #
        self.main_menu_component = MainMenuComponent(app=self)
        #
        self.search_bar_component = SearchBarComponent(app=self)
        #
        self.active_username = ""
        self.active_user = {}


        #
    

    def check_auto_login_status(self):
        
        json_file = HandleJsonFile()
        config = json_file.load_data_from_json_file("storage", "config")
        #
        if not isinstance(config, dict) or not config.get("auto_login"):
            print("Auto-login not enabled or configuration missong")
            return False
        #
        saved_email = config.get("saved_email")
        if not saved_email:
            return False
        #
        userService = UserService()
        account = userService.get_user_email(saved_email)
        if not account:
            print("Account not found and cannot auto-login!")
            return False
            #
        #
        self.active_user = account
        self.active_username = account.get("name")
        print(f"Auto-login verified successfully for user profile: {account}")
        return True
        #
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
        self.refresh_profile_header()

    def refresh_profile_header(self):
        if hasattr(self, 'profile_lbl') and self.profile_lbl:
            #user_name = getattr(self, "active_username", '')

            #print(f"username: {user_name}")


            if self.active_username:
                print(f"re active_user: {self.active_user}")
                welcome_prefix = self.i18n._("welcome_user") if hasattr(self.i18n, "_") else "Welcome"
                self.profile_lbl.set_text(f"{welcome_prefix}, {self.active_username}")
                # re-render
                self.build_profile_info_view()
                #GLib.idle_add(self.build_profile_company_view)
                #GLib.idle_add(self.build_profile_address_view)
                #self.build_profile_company_view()
                #self.build_profile_address_view()
                
            else:
                print(f"cannot get active_name")
                self.profile_lbl.set_text("")
        #

    def refresh_row_dictionaries(self):
        target_dictionaries = ['nav_rows', 'nav_settings_rows', 'nav_profile_rows']
        for row_attr in target_dictionaries:
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
         

    def clear_right_sidebar(self):
        while child := self.right_sidebar.get_first_child():
                       self.right_sidebar.remove(child)

    def clear_center_stack(self):
        while child := self.center_stack.get_first_child():
                       self.center_stack.remove(child)

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
        # auto-login
        auto_login_success = self.check_auto_login_status()

        #

        

        # create toolbar
        toolbar_view = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        # add css-class to header-bar
        header_bar.add_css_class("custom-topbar")
        # add header_bar in toolbar
        #
        #toolbar_view.add_top_bar(header_bar)

        # menu: language-switcher 
        self.lang_menu_component = MenuLanguagesComponent(app=self)
        switcher_button = self.lang_menu_component.get_menu_button()
        header_bar.pack_end(switcher_button)

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

        

        """GLib.idle_add(self.rebuild_menu)
        self.setup_actions()


        # menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_menu_model(self.menu)
        menu_button.set_icon_name("open-menu-symbolic")"""

        # add in header_bar
        #header_bar.pack_end(menu_button)
        #self.main_menu_component.rebuild_menu()
        main_menu_button = self.main_menu_component.get_menu_button()
        header_bar.pack_end(main_menu_button)




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
        self.view_stack = Adw.ViewStack()
        self.view_stack.set_vexpand(True)
        self.view_stack.set_margin_start(8)
        self.view_stack.set_margin_end(8)

        #tab1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        tab1_box = TabBox(app=self, wrapper_title="home", key="tab_home", icon_name="user-home-symbolic")
        tab1_box.set_margin_top(12)

       

        # Left items list box configuration
        self.list_box = ListBoxComponent() #Gtk.ListBox()
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
        self.nav_rows = tab1_box.build(self.list_box, home_items,  self.nav_rows)
        

        
        # tab2
        #tab2_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        tab2_box = TabBox(app=self, wrapper_title="settings", key="tab_settings", icon_name="emblem-system-symbolic")
        tab2_box.set_margin_top(12)
        #tab2_box.append(Gtk.Label(label="tab2"))

        


        #
        self.list2_box = ListBoxComponent() #Gtk.ListBox()
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
        self.nav_settings_rows = tab2_box.build(self.list2_box, settings_items,  self.nav_settings_rows)
        
        

       


        #tab3
        # profile_info
        

        #tab3_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        tab3_box = TabBox(app=self, wrapper_title="profile", key="tab_profile", icon_name="avatar-default-symbolic")
        tab3_box.set_margin_top(12)
        #
      
        # profile-label
        self.profile_lbl = Gtk.Label()
        self.profile_lbl.add_css_class("title-2")
        self.profile_lbl.set_margin_bottom(16)
        self.profile_lbl.set_justify(Gtk.Justification.CENTER)
        tab3_box.append(self.profile_lbl)
        #tab3_box.append(Gtk.Label(label="tab3"))
        #
        self.list3_box = ListBoxComponent() #Gtk.ListBox()
        self.list3_box.add_css_class("boxed-list")

        profile_items = [
            ("profile_info", "user-info-symbolic"),
            ("profile_address", "mark-location-symbolic"),
            ("profile_company", "org.gnome.Settings-about-symbolic"),
        ]

        # Tracking dictionary to easily find rows during translation refresh cycles
        self.nav_profile_rows = tab3_box.build(self.list3_box, profile_items,  self.nav_profile_rows)

       


        

        


        # view_switcher
        self.view_switcher = Adw.ViewSwitcher()
        self.view_switcher.set_stack(self.view_stack)
        
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
        left_sidebar.append(self.view_stack)
        #left_sidebar.append(view_switcher_bar)
        # search-bar
        """search_bar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        search_bar_box.set_margin_top(12)
        search_bar_box.set_margin_bottom(12)
        search_bar_box.set_margin_start(16)
        search_bar_box.set_margin_end(16)

        self.sidebar_search_entry = Gtk.SearchEntry()
        self.sidebar_search_entry.set_hexpand(True)
        self.sidebar_search_entry.set_placeholder_text(self.i18n._("search_placeholder"))
        self.sidebar_search_entry.connect("search-changed", self.on_sidebar_search_changed)
        self.register_widget(self.sidebar_search_entry, 'placeholder', 'search_placeholder')

        search_bar_box.append(self.sidebar_search_entry)"""

        #self.search_bar_component = SearchBarComponent(app=self)

        left_sidebar.append(self.search_bar_component)
        
        
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
        """loading_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        loading_box.set_valign(Gtk.Align.CENTER)
        spinner = Gtk.Spinner()
        spinner.start()
        spinner.set_size_request(40, 40)
        loading_box.append(spinner)
        loading_label = Gtk.Label(label="Fetching live user cards...")
        loading_box.append(loading_label)"""

        loading_box = LoadingBoxComponent()
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
        #self.build_test_view()
        self.test_view_class = TestViewClass(app=self)
        #
        #self.build_test_users_view()
        self.users_view_class = UsersViewClass(app=self)
        #
        #self.build_test_posts_view2()
        PostsViewClass(app=self)
        self.comments_view_class = CommentsViewClass()
        #
        #self.build_test_todos_view()
        TodosViewClass(app=self)
        #
        # View E: Local
        self.build_local_tabs_view()
        # View F: storage in disk
        self.build_disk_tabs_view()
        # View : Shell
        self.build_shell_view()

        # View : Profile-info
        #self.build_profile_info_view()
        # View : Profile-address
        #self.build_profile_address_view()
        # View : Profile-company
        #self.build_profile_company_view()


        # View S: Posts
        """self.posts_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.posts_container.set_margin_top(24)
        self.posts_container.set_margin_bottom(24)
        self.posts_container.set_margin_start(24)
        self.posts_container.set_margin_end(24)

        scroll_win.set_child(self.posts_container)
        self.center_stack.add_named(scroll_win, "posts_view")"""
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



        

        # use AuthComponent
        auth_panel_view = AuthComponent(app=self)





        # 2. root nav stack
        self.root_navigation_stack = Gtk.Stack()
        self.root_navigation_stack.set_transition_type(Gtk.StackTransitionType.NONE)
        #self.root_navigation_stack.add_named(login_box, "login_screen_layout")
        #self.root_navigation_stack.add_named(self.auth_nav_stack, "auth_layout")
        self.root_navigation_stack.add_named(auth_panel_view, "auth_layout")
        self.root_navigation_stack.add_named(self.outer_split_view, "main_layout")
        #self.root_navigation_stack.set_visible_child_name("login_screen_layout")

        #
        if auto_login_success:
            self.refresh_profile_header()
            if hasattr(self, 'main_menu_component'):
                self.main_menu_component.rebuild_menu()
            #
            self.root_navigation_stack.set_visible_child_name("main_layout")
        else:
            self.root_navigation_stack.set_visible_child_name("auth_layout")

        #
        self.toast_overlay = Adw.ToastOverlay()
        #self.toast_overlay.set_child(self.root_navigation_stack)
        self.toast_overlay.set_child(header_bar)
        toolbar_view.add_top_bar(self.toast_overlay)
        



        #
        #toolbar_view.set_content(self.toast_overlay)
        toolbar_view.set_content(self.root_navigation_stack)
        self.win.set_content(toolbar_view)
        #win.set_content(box)
        self.win.present()
        #

      
    def on_logout_button_clicked(self, button):
        self.isLogin = False
        
        #
        if hasattr(self, 'root_navigation_stack'):
            self.root_navigation_stack.set_visible_child_name("auth_layout")
            #self.auth_nav_stack.set_visible_child_name("login_screen_layout")
            print("Session cleared. Interface state locked back to login")
        self.logout_btn.set_visible(False)
        #GLib.idle_add(self.rebuild_menu)
        # clear config for auto_login
        json_file = HandleJsonFile()
        empty_config = {
            "auto_login": False,
            "saved_email": "",
        }
        json_file.save_data_to_json_file(empty_config, "storage", "config")
        #
        if hasattr(self, "main_menu_component"):
            self.main_menu_component.rebuild_menu()
        #
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

            toastoverlay widget {
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

            entry.error {
               border: 2px solid #ef4444;
               background-color: #fef2f2;
            
            }

            label.error-msg {
               color: #ef4444;
               font-size: 18px;
               margin-top: 4px;
               border: 1px solid #ef4444;
               padding: 2px;

               /*opacity: 0;*/
            }

            label.error-msg.visible {
                /*opacity: 1;*/
            }

            .custom-small-pill {
                /*padding: 4px 12px;*/
                min-wdith: 100px;
                max-width: 200px;
                font-size: 15px;
                font-weight: bold;
            }

            .custom-small-pill:hover {
               background-color: #b0c4de;
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
                row.set_activatable(True)
                row.payload = item
                row.connect("activated", self.test_view_class.card_clicked)
                
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
                row.connect("activated", self.users_view_class.user_card_clicked)



                

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

                #self.build_test_comments_by_postId_view(main_box, item.get("id"))
                self.comments_view_class.build_by_postId(main_box, item.get("id"))

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
                    self.local_posts_group.set_title("Posts")
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

         

    def build_profile_info_view(self):
        #
        print(f"state#: {self.state}")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False)

        #
        self.local_title = Gtk.Label(label="Profile Info")
        self.local_title.add_css_class("heading")
        local_action_bar.set_title_widget(self.local_title)
        #
        
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
        local_items_group = Adw.PreferencesGroup()
        local_items_group.set_title("info title")
        #
        #lbl = Gtk.Label(label=self.active_user.get("name"))

        #local_items_group.add(lbl)

        #
        
        print(f"profile info user: {self.active_user.get("name")}")
        #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(5)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_size_request(240, -1)
        #
        #lbl = Gtk.Label(label="test...")
        #box.append(lbl)
        #
        """box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box1.set_margin_top(12)
        box1.set_margin_bottom(12)
        box1.set_margin_start(12)
        box1.set_margin_end(12)

        
        lbl2 = Gtk.Label(label="Name:")
        box1.append(lbl2)

        lbl2 = Gtk.Label(label=self.active_user.get("name"))
        box1.append(lbl2)

        box.append(box1)"""
        #
       

        # render edit profile form
        #def render_edit_profile_info_form(button):
        lbl = Gtk.Label(label="Edit Profile")
        lbl.set_visible(False)
        lbl.set_margin_top(20)
        self.right_sidebar.append(lbl)
        #
        sidebar_group = Adw.PreferencesGroup()
        sidebar_group.set_visible(False)
        #
        close_btn = Gtk.Button(label="Close")
        close_btn.add_css_class("pill")
        close_btn.add_css_class("custom-small-pill")
        close_btn.set_halign(Gtk.Align.END)
        close_btn.set_margin_end(20)
        close_btn.set_visible(False)

        def on_close(button):
            #self.clear_right_sidebar()
            #
            lbl.set_visible(False)
            close_btn.set_visible(False)
            sidebar_group.set_visible(False)
              
        close_btn.connect("clicked", on_close)
        self.right_sidebar.append(close_btn)
        #


        sidebar_group.set_margin_top(20)
        sidebar_group.set_margin_start(20)
        sidebar_group.set_margin_end(20)
        #sidebar_group.set_title("User Information")
        #
        input_name = Gtk.Entry(placeholder_text="Name")
        input_name.set_text(self.active_user.get("name"))
        sidebar_group.add(input_name)
        #
        input_email = Gtk.Entry(placeholder_text="Email")
        input_email.set_text(self.active_user.get("email"))
        input_email.set_margin_top(20)
        sidebar_group.add(input_email)
        #
        input_username = Gtk.Entry(placeholder_text="UserName")
        input_username.set_margin_top(20)
        sidebar_group.add(input_username)
        #
        input_phone = Gtk.Entry(placeholder_text="Phone")
        input_phone.set_margin_top(20)
        sidebar_group.add(input_phone)
        #
            #
        input_web = Gtk.Entry(placeholder_text="Website")
        input_web.set_margin_top(20)
        sidebar_group.add(input_web)
        #
        submit_btn = Gtk.Button(label="Update")
        submit_btn.set_margin_top(30)
        sidebar_group.add(submit_btn)
        #
        self.right_sidebar.append(sidebar_group)
        #
        def update_profile_info_data(button):
            name = input_name.get_text().strip()
            email = input_email.get_text().strip()
            username = input_username.get_text().strip()
            phone = input_phone.get_text().strip()
            website = input_web.get_text().strip()
            #
            update_user = {
                "name": name,
                "email": email,
                "username": username,
                "phone": phone,
                "website": website,
            }

            print(f"update_profile_info_data: {update_user}")
            # get data from json file
            json_file = HandleJsonFile()
            json_db = json_file.load_data_from_json_file("storage", "accounts")

            if not json_db:
                print("no data found for updating profile info")
                return

            print(f"json_db data: {json_db}")
            # get doc based on email
            account_user = {}
            updated_account_user = {}
            is_account_found = False
            for account in json_db:
                if account.get("email") == self.active_user.get("email"):
                    is_account_found = True
                    account_user = account
                    print(f"found account user: {account}")
                    #
                    account["name"] = name
                    account["email"] = email
                    account["username"] = username
                    account["phone"] = phone
                    account["website"] = website
                    #
                    updated_account_user = account
                    
                    #



                else:
                    is_account_found = False
            #
            if is_account_found:
                print(f"account user: {account}")
                print(f"updated_account_user: {updated_account_user}")
                #
                print(f"after json_db: {json_db}")
                #
                json_file.save_data_to_json_file(json_db, "storage", "accounts")
                #
                self.active_user = updated_account_user
                self.active_username = updated_account_user.get("name")
                self.refresh_profile_header()
                #
                if hasattr(self, 'toast_overlay'):
                    success = self.i18n._("success_update_msg")
                    self.toast_overlay.add_toast(Adw.Toast.new(success))
            #
            else:
                if hasattr(self, 'toast_overlay'):
                    #failed = self.i18n._("failed_update_msg")
                    self.toast_overlay.add_toast(Adw.Toast.new("Account not found!"))





                #


                

            # 


        
        
        #
        submit_btn.connect("clicked", update_profile_info_data)


        #
        edit_btn = Gtk.Button(label="Edit")
        edit_btn.add_css_class("pill")
        edit_btn.add_css_class("custom-small-pill")
        #edit_btn.set_size_request(150, -1) # width
        edit_btn.set_halign(Gtk.Align.END)
        #edit_btn.set_margin_top(20)
        box.append(edit_btn)
        #
        
        #
        edit_btn.connect("clicked", lambda x: [
                             lbl.set_visible(True),
                             close_btn.set_visible(True),
                             sidebar_group.set_visible(True),      
        ])
        #


       


        #
        sidebar2_group = Adw.PreferencesGroup()
        #sidebar_group.set_title("User Information")
        name_row = Adw.ActionRow(title="Name", subtitle=self.active_user.get("name", "N/A"))
        sidebar2_group.add(name_row)
        email_row = Adw.ActionRow(title="Email", subtitle=self.active_user.get("email", "N/A"))
        sidebar2_group.add(email_row)
        phone_row = Adw.ActionRow(title="Phone", subtitle=self.active_user.get("phone", "N/A"))
        sidebar2_group.add(phone_row)
        web_row = Adw.ActionRow(title="Website", subtitle=self.active_user.get("website", "N/A"))
        sidebar2_group.add(web_row)
        box.append(sidebar2_group)

        

        #
        #self.empty_list_lbl = Gtk.Label(label=self.i18n._("empty_list_text"))
        #self.empty_list_lbl.add_css_class("dim-label")
        #self.local_items_group.add(self.empty_list_lbl)
        # attach list data in ui
        content_box.append(box)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)


        #
        existing =  self.center_stack.get_child_by_name("profile_info_view")
        if existing:
            self.center_stack.remove(existing)

        self.center_stack.add_named(local_wrapper, "profile_info_view")
        #




    def build_profile_address_view(self):
        #
        while child := self.right_sidebar.get_first_child():
                   self.right_sidebar.remove(child)
        #self.right_sidebar.append(Gtk.Label(label="test..."))
        #
        print(f"state#: {self.state}")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False)

        #
        local_title = Gtk.Label(label="Address")
        local_title.add_css_class("heading")
        local_action_bar.set_title_widget(local_title)
        #
        #self.add_item_btn = Gtk.Button(label=self.i18n._("btn_add"))
        #self.add_item_btn.add_css_class("suggested-action")
        #local_action_bar.pack_end(self.add_item_btn)
        # build the form as popover
        
        # inputs
        #self.input_name = Gtk.Entry(placeholder_text=self.i18n._("input_name_ph"))
        #form_box.append(self.input_name)

        #self.input_desc = Gtk.Entry(placeholder_text=self.i18n._("input_desc_ph"))
        #form_box.append(self.input_desc)
        #
        #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_size_request(240, -1)
        #
        #lbl = Gtk.Label(label="test...")
        #box.append(lbl)
        #
        #lbl2 = Gtk.Label(label=self.active_user.get("email"))
        #box.append(lbl2)

        address = self.active_user.get("address")

       

        

        lbl4 = Gtk.Label(label="Add/Edit Address")
        lbl4.set_margin_top(20)
        lbl4.set_visible(False)
        self.right_sidebar.append(lbl4)
        #
        sidebar_group = Adw.PreferencesGroup()
        sidebar_group.set_visible(False)
        #
        submit_btn = Gtk.Button(label="Add")
        #
        close_btn = Gtk.Button(label="Close")
        close_btn.set_halign(Gtk.Align.END)
        close_btn.set_margin_end(20)
        close_btn.set_visible(False)

        def on_close(button):
            #self.clear_right_sidebar()
            #
            lbl4.set_visible(False)
            close_btn.set_visible(False)
            sidebar_group.set_visible(False)
              
        close_btn.connect("clicked", on_close)
        self.right_sidebar.append(close_btn)
        #
        


        #if not address:
        sidebar_group.set_margin_top(20)
        sidebar_group.set_margin_start(20)
        sidebar_group.set_margin_end(20)
        #sidebar_group.set_title("User Information")
        #
        input_street = Gtk.Entry(placeholder_text="Enter Street")
        sidebar_group.add(input_street)
        #
        input_zipcode = Gtk.Entry(placeholder_text="Enter Zipcode")
        input_zipcode.set_margin_top(20)
        sidebar_group.add(input_zipcode)
        #
        input_city = Gtk.Entry(placeholder_text="Enter City")
        input_city.set_margin_top(20)
        sidebar_group.add(input_city)
        #
        #submit_btn = Gtk.Button(label="Add")
        submit_btn.set_margin_top(30)
        sidebar_group.add(submit_btn)
        #
        def update_profile_address_data(button):
            street = input_street.get_text().strip()
            zipcode = input_zipcode.get_text().strip()
            city = input_city.get_text().strip()
            #
            update_address = {
                "street": street,
                "zipcode": zipcode,
                "city": city,
            }

            user_payload = dict(self.active_user)
            user_payload["address"] = update_address
                
            

            

            print(f"update_profile_address_data: {update_address}")
            print(f"update_profile_data: {user_payload}")
            #
            user_service = UserService()
            email = user_payload.get("email")
            saved = user_service.update_user_by_email(target_email=email, data=user_payload)

            #print(f"after updated self.active_user: {self.active_user}")
            if saved:
                print(f"saved: {saved}")
                self.active_user = saved
                pass
            else:
                print(f"cannot save profile address")
                pass
            #


        #
        submit_btn.connect("clicked", update_profile_address_data)
                  
             #
        
        self.right_sidebar.append(sidebar_group)
        

        #
        """btn1 = Gtk.Button(label="add")
             
        # add lbl in right_sidebar
        
        #box.append(lbl3)
        #self.right_sidebar.append(lbl4)
        btn1.connect("clicked", lambda x: [ 
                     lbl4.set_visible(True),
                     sidebar_group.set_visible(True)
        ])"""

        #box.append(btn1)
        #
        edit_btn = Gtk.Button(label="Edit")
        edit_btn.add_css_class("pill")
        edit_btn.set_halign(Gtk.Align.END)
        #edit_btn.set_margin_top(5)
        edit_btn.connect("clicked", lambda x:  [
             
             lbl4.set_visible(True),
             close_btn.set_visible(True),
             sidebar_group.set_visible(True),
            ])
        box.append(edit_btn)
        #
        #submit_btn.connect("clicked", lambda x: [
        #       print("submit add address")
        #])
        #self.right_sidebar.append(lbl4)
        #box.append(lbl4)

        #
        sidebar_group2 = Adw.PreferencesGroup()
        #sidebar_group.set_title("User Information")

        street_row = Adw.ActionRow(title="Street", subtitle=address.get("street", "N/A"))
        sidebar_group2.add(street_row)
        zipcode_row = Adw.ActionRow(title="Zipcode", subtitle=address.get("zipcode", "N/A"))
        sidebar_group2.add(zipcode_row)
        city_row = Adw.ActionRow(title="City", subtitle=address.get("city", "N/A"))
        sidebar_group2.add(city_row)
        box.append(sidebar_group2)
        
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
        local_items_group = Adw.PreferencesGroup()
        local_items_group.set_title("Address title")

        #
        

        #
        #self.empty_list_lbl = Gtk.Label(label=self.i18n._("empty_list_text"))
        #self.empty_list_lbl.add_css_class("dim-label")
        #self.local_items_group.add(self.empty_list_lbl)
        # attach list data in ui
        content_box.append(box)
        #content_box.append(local_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)


        #
        existing =  self.center_stack.get_child_by_name("profile_address_view")
        if existing:
            self.center_stack.remove(existing)
        self.center_stack.add_named(local_wrapper, "profile_address_view")
        #
        #return False

    
    def build_profile_company_view(self):
        #
        while child := self.right_sidebar.get_first_child():
                   self.right_sidebar.remove(child)
        #
        print(f"state#: {self.state}")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False)

        #
        self.local_title = Gtk.Label(label="Company")
        self.local_title.add_css_class("heading")
        local_action_bar.set_title_widget(self.local_title)
        #

       
        local_wrapper.add_top_bar(local_action_bar)

        #
        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(20)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)

        #
        local_items_group = Adw.PreferencesGroup()
        local_items_group.set_title("Company title")

        #
         #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_size_request(240, -1)
        #
        #lbl = Gtk.Label(label="test...")
        #box.append(lbl)
        #
        #lbl2 = Gtk.Label(label=self.active_user.get("email"))
        #box.append(lbl2)

        company = self.active_user.get("company")
       

        #
        lbl4 = Gtk.Label(label="Add/Edit Company")
        lbl4.set_margin_top(20)
        lbl4.set_visible(False)
        self.right_sidebar.append(lbl4)
        #
        sidebar_group = Adw.PreferencesGroup()
        sidebar_group.set_visible(False)
        #
        submit_btn = Gtk.Button(label="Add")
        #
        close_btn = Gtk.Button(label="Close")
        close_btn.set_halign(Gtk.Align.END)
        close_btn.set_margin_end(20)
        close_btn.set_visible(False)

        def on_close(button):
            #self.clear_right_sidebar()
            #
            lbl4.set_visible(False)
            close_btn.set_visible(False)
            sidebar_group.set_visible(False)
              
        close_btn.connect("clicked", on_close)
        self.right_sidebar.append(close_btn)
        #
        

        #if not company:
             #
        sidebar_group.set_margin_top(20)
        sidebar_group.set_margin_start(20)
        sidebar_group.set_margin_end(20)
        #sidebar_group.set_title("User Information")
        #
        input_name = Gtk.Entry(placeholder_text="Enter Name")
        sidebar_group.add(input_name)
        #
        input_bs = Gtk.Entry(placeholder_text="Enter Business")
        input_bs.set_margin_top(20)
        sidebar_group.add(input_bs)
        #
        #input_city = Gtk.Entry(placeholder_text="Enter City")
        #input_city.set_margin_top(20)
        #sidebar_group.add(input_city)
        #
        #submit_btn = Gtk.Button(label="Add")
        submit_btn.set_margin_top(30)
        sidebar_group.add(submit_btn)
        #sidebar_group.set_title("User Information")
        #name_row = Adw.ActionRow(title="Name", subtitle=self.active_user.get("name", "N/A"))
        #sidebar_group.add(name_row)
        #email_row = Adw.ActionRow(title="Email", subtitle=self.active_user.get("email", "N/A"))
        #sidebar_group.add(email_row)
        #
        
        self.right_sidebar.append(sidebar_group)
        #
        def update_profile_company_data(button):
            name = input_name.get_text().strip()
            bs = input_bs.get_text().strip()
            #
            update_company = {
                "name": name,
                "bs": bs,
            }

            user_payload = dict(self.active_user)
            user_payload["company"] = update_company
                
            

            

            print(f"update_profile_company_data: {update_company}")
            print(f"update_profile_data: {user_payload}")
            #
            user_service = UserService()
            email = user_payload.get("email")
            saved = user_service.update_user_by_email(target_email=email, data=user_payload)

            #print(f"after updated self.active_user: {self.active_user}")
            if saved:
                print(f"saved: {saved}")
                self.active_user = saved
                pass
            else:
                print(f"cannot save profile address")
                pass
            #


        #
        submit_btn.connect("clicked", update_profile_company_data)




        #
        #btn1.connect("clicked", lambda x:  [
        #     lbl4.set_visible(True),
        #     sidebar_group.set_visible(True),
        #    ])
        #box.append(btn1)
        #
        #submit_btn.connect("clicked", lambda x: [
        #       print("submit add company")
        #])
        edit_btn = Gtk.Button(label="Edit")
        edit_btn.add_css_class("pill")
        edit_btn.set_halign(Gtk.Align.END)
        #edit_btn.set_margin_top(20)
        edit_btn.connect("clicked", lambda x:  [
             lbl4.set_visible(True),
             close_btn.set_visible(True),
             sidebar_group.set_visible(True),
            ])
        box.append(edit_btn)
        

        #
        sidebar2_group = Adw.PreferencesGroup()
        #sidebar_group.set_title("User Information")
        name_row = Adw.ActionRow(title="Name", subtitle=company.get("name","N/A"))
        sidebar2_group.add(name_row)
        bs_row = Adw.ActionRow(title="Business", subtitle=company.get("bs","N/A"))
        sidebar2_group.add(bs_row)
        box.append(sidebar2_group)

        #self.empty_list_lbl = Gtk.Label(label=self.i18n._("empty_list_text"))
        #self.empty_list_lbl.add_css_class("dim-label")
        #self.local_items_group.add(self.empty_list_lbl)
        # attach list data in ui
        content_box.append(box)
        #content_box.append(local_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)


        #
        existing =  self.center_stack.get_child_by_name("profile_company_view")
        if existing:
            self.center_stack.remove(existing)
        self.center_stack.add_named(local_wrapper, "profile_company_view")
        #
        #return False

    
    def on_btn_add_profile_addess(self, button):
        print("add_profile_address")
        
       



    def on_btn_add_profile_company(self, button):
        print("on_btn_add_company")

    
    def safely_add_to_center_stack(self, widget, key):
        existing =  self.center_stack.get_child_by_name(key)
        if existing:
            self.center_stack.remove(existing)
        self.center_stack.add_named(widget, key)

       

    # build settings view
    def build_settings_template_view(self, action_bar_title, layout_name, box: Gtk.Box):
        print("build_settings_template_view")
        
        #action-bar-title
        #action-bar: action-bar(action-bar-title)
        #box: box(...)
        #content-box: content-box(box)
        #scroll: scroll(content-box)
        #wrapper: wrapper(scroll), wrapper(action-bar)
        #center_stack(wrapper)
        #
        
        action_bar = Gtk.HeaderBar()
        action_bar.set_show_title_buttons(False)
        actionBar_title = Gtk.Label(label= "Settings") #action_bar_title)
        actionBar_title.add_css_class("heading")
        # add actionBar_title in action_bar
        action_bar.set_title_widget(actionBar_title)
        wrapper = Adw.ToolbarView()
        # add action_bar in wrapper
        wrapper.add_top_bar(action_bar)
        #
        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        #
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(20)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        # add box in content-box
        content_box.append(box)
        # add content-box in scroll
        scroll_win.set_child(content_box)
        # add scroll in wrapper
        wrapper.set_content(scroll_win)

        #
        self.safely_add_to_center_stack(wrapper, layout_name)
        #
        #existing =  self.center_stack.get_child_by_name(layout_name)
        #if existing:
        #    self.center_stack.remove(existing)
        #self.center_stack.add_named(wrapper, layout_name)


    def build_settings_general_view(self):
        print("build_settings_general_view")
        #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_size_request(240, -1)
        #
        lbl = Gtk.Label(label="general test...")
        #box.append(lbl)
        #
        group = Adw.PreferencesGroup()
        self.register_widget(group, "title", "setting_general_item")
        #
        animation_row = Adw.SwitchRow()
        self.register_widget(animation_row, "title", "animations")
        group.add(animation_row)
        box.append(group)




        #
        self.build_settings_template_view(action_bar_title="General",layout_name="settings_general_view", box=box)
        
       

    def build_settings_account_view(self):
        print("build_settings_accounts_view")
        #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_size_request(240, -1)
        #
        lbl = Gtk.Label(label="account test...")
        #box.append(lbl)
        #
        group = Adw.PreferencesGroup()
        self.register_widget(group, "title", "setting_account_item")

        #
        username_row = Adw.EntryRow()
        self.register_widget(username_row, "title", "username_label")
        username_row.set_text(self.active_user.get("username", "N/A"))
        group.add(username_row)
        #
        email_row = Adw.EntryRow()
        self.register_widget(email_row, "title", "email_label")
        email_row.set_text(self.active_user.get("email", "N/A"))
        group.add(email_row)
        #

        #
        box.append(group) 




        #
        self.build_settings_template_view(action_bar_title="General",layout_name="settings_account_view", box=box)
        
       

    def build_settings_notifications_view(self):
        print("build_settings_notifications_view")
        #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_size_request(240, -1)
        #
        lbl = Gtk.Label(label="notifications test...")
        #box.append(lbl)
        #
        group = Adw.PreferencesGroup()
        self.register_widget(group, "title", "setting_notifications_item")
        #
        sound_row = Adw.SwitchRow()
        self.register_widget(sound_row, "title", "setting_notifications_item")
        group.add(sound_row)
        #
        box.append(group)




        #
        self.build_settings_template_view(action_bar_title="General",layout_name="settings_notifications_view", box=box)

       

    def build_settings_display_view(self):
        print("build_settings_display_view")
        #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_size_request(240, -1)
        #
        lbl = Gtk.Label(label="display test...")
        #box.append(lbl)
        #
        group = Adw.PreferencesGroup()
        self.register_widget(group, "title", "setting_display_item")
        #
        dark_mode_row = Adw.SwitchRow()
        dark_mode_row.connect("notify::active", self.on_dark_mode_toggle_changed)
        self.register_widget(dark_mode_row, "title", "dark_mode")
        group.add(dark_mode_row)
        #
        box.append(group)




        #
        self.build_settings_template_view(action_bar_title="General",layout_name="settings_display_view", box=box)
        
    
    def on_dark_mode_toggle_changed(self, switch_row, gparam_spec):
        print(f"on_dark_mode_toggle_changed")

        is_dark_mode_enabled = switch_row.get_active()

        current_scheme = self.style_manager.get_color_scheme()

        if is_dark_mode_enabled:
        #if current_scheme == Adw.ColorScheme.PREFER_LIGHT or current_scheme == Adw.ColorScheme.DEFAULT:
           self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
           
           self.theme_btn.set_icon_name("display-brightness-symbolic")
           print("Theme scheme updated to : FORCE DARK")    
        else:
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
            self.theme_btn.set_icon_name("weather-clear-symbolic")
            print("Theme scheme updated to: FORCE LIGHT")
       

    def build_settings_colors_view(self):
        print("build_settings_colors_view")
        #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_size_request(240, -1)
        #
        lbl = Gtk.Label(label="colors test...")
        #box.append(lbl)
        #
        group = Adw.PreferencesGroup()
        self.register_widget(group, "title", "setting_colors_item")
        #
        colors_dropdown_row = Adw.ComboRow()
        self.register_widget(colors_dropdown_row, "title", "accent_color")
        color_model = Gtk.StringList.new(["Blue", "Teal", "Green", "Orange", "Red"])
        colors_dropdown_row.set_model(color_model)
        group.add(colors_dropdown_row)
        #
        box.append(group)




        #
        self.build_settings_template_view(action_bar_title="General",layout_name="settings_colors_view", box=box)

        

    def build_settings_keyboard_view(self):
        print("build_settings_keyboard_view")
        #
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_size_request(240, -1)
        #
        lbl = Gtk.Label(label="keyboard test...")
        #box.append(lbl)
        #
        group = Adw.PreferencesGroup()
        self.register_widget(group, "title", "setting_keyboard_item")
        #
        k_layout_row = Adw.ComboRow()
        self.register_widget(k_layout_row, "title", "layout_title")
        k_model = Gtk.StringList.new(["English", "German", "Arabic"])
        k_layout_row.set_model(k_model)
        group.add(k_layout_row)
        #
        box.append(group)




        #
        self.build_settings_template_view(action_bar_title="General",layout_name="settings_keyboard_view", box=box)
        
    



    
    def on_home_item_clicked(self, row):
        #
        self.clear_right_sidebar()
        #
        #self.clear_center_stack()
        #

        clicked_title = row.get_title()

        if not row or not hasattr(row, 'nav_item_key_id'):
            return
        
        #
        key = row.nav_item_key_id
        print(f"left > row item activated: {key}")




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
            
        # profile tabs
        """elif clicked_title == "Info":
            #self.info_label.set_text(f"Selected Section: {clicked_title} ###")
            #self.build_profile_info_view()
            self.center_stack.set_visible_child_name("profile_info_view")

        
        elif clicked_title == "Address":
            #self.info_label.set_text(f"Selected Section: {clicked_title} ####?")
            self.build_profile_address_view()
            self.center_stack.set_visible_child_name("profile_address_view")
            
        
        
        elif clicked_title == "Company":
            #self.info_label.set_text(f"Selected Section: {clicked_title} ####!")
            self.build_profile_company_view()
            self.center_stack.set_visible_child_name("profile_company_view")
        """


        """else:
            #self.center_stack.set_visible_child_name("welcome_view")
            self.info_label.set_text(f"Selected Section: {clicked_title}")
            self.state = ""
        # call fetching"""

        #
        if key == "profile_info":
            #self.info_label.set_text(f"Selected Section: {clicked_title} ###")
            self.build_profile_info_view()
            self.center_stack.set_visible_child_name("profile_info_view")
        elif key == "profile_address":
            #self.info_label.set_text(f"Selected Section: {clicked_title} ####?")
            self.build_profile_address_view()
            self.center_stack.set_visible_child_name("profile_address_view")
        elif key == "profile_company":
            #self.info_label.set_text(f"Selected Section: {clicked_title} ####!")
            self.build_profile_company_view()
            self.center_stack.set_visible_child_name("profile_company_view")
        # settings        
        elif key == "setting_general_item":
             #self.info_label.set_text(f"Selected Section: {clicked_title} ")
             self.build_settings_general_view()
             self.center_stack.set_visible_child_name("settings_general_view")
        elif key == "setting_account_item":
             #self.info_label.set_text(f"Selected Section: {clicked_title} ")
             self.build_settings_account_view()
             self.center_stack.set_visible_child_name("settings_account_view")
        elif key == "setting_notifications_item":
             #self.info_label.set_text(f"Selected Section: {clicked_title} ")
             self.build_settings_notifications_view()
             self.center_stack.set_visible_child_name("settings_notifications_view")
        elif key == "setting_display_item":
             #self.info_label.set_text(f"Selected Section: {clicked_title} ")
             self.build_settings_display_view()
             self.center_stack.set_visible_child_name("settings_display_view")
        elif key == "setting_colors_item":
             #self.info_label.set_text(f"Selected Section: {clicked_title} ")
             self.build_settings_colors_view()
             self.center_stack.set_visible_child_name("settings_colors_view")
        elif key == "setting_keyboard_item":
             #self.info_label.set_text(f"Selected Section: {clicked_title} ")
             self.build_settings_keyboard_view()
             self.center_stack.set_visible_child_name("settings_keyboard_view")
        #



    
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
    """
    def setup_actions(self):
       
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
        
        print(f"rebuild_menu executing... User Authenticated: {self.isLogin}")

        # =========================================================================
        # FIX 1: Reuse or instantiate your menu container model shell cleanly
        # =========================================================================
        if not hasattr(self, 'menu') or self.menu is None:
            self.menu = Gio.Menu.new()
        else:
            self.menu.remove_all() # Clears out old options to prevent layout accumulation

        # 1. Append global navigation options common to both application states
        self.append("About", "app.about")
        self.append("Quit", "app.quit")
        self.append("Restart", "app.restart")

        # 2. Append conditional menu entries based on active authentication parameters
        if self.isLogin:
            self.append("Logout", "app.logout")
            print("Visual Logout option item appended to menu model tree.")
        else:
            print("Visual Logout option item hidden from menu model tree.")

        # =========================================================================
        # FIX 2: Removed self.add_action() from here to prevent duplicate registration lag
        # =========================================================================
        return False
    """



        


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
        #GLib.idle_add(self.rebuild_menu)
        #self.main_menu_component.rebuild_menu()
        self.logout_btn.set_visible(False)
        # clear config for auto_login
        json_file = HandleJsonFile()
        empty_config = {
            "auto_login": False,
            "saved_email": "",
        }
        json_file.save_data_to_json_file(empty_config, "storage", "config")
        #
        if hasattr(self, "main_menu_component"):
            self.main_menu_component.rebuild_menu()


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