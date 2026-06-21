import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib, Gdk

import sys
import urllib.request
import threading
import json


print("start py")


class MyApp(Adw.Application):
    def __init__(self):
        print("MyApp init")
        super().__init__(
            application_id="com.example.myapp", 
            flags=Gio.ApplicationFlags.FLAGS_NONE
            )
        #self.connect('activate', self.on_activate)

    def do_activate(self):
        # this is called g_application_activate() -> app.run()

        # locale
        #Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)



        # window
        #win = Adw.ApplicationWindow(application=app)
        self.win = Adw.ApplicationWindow(application=self)
        self.win.set_title("Mein Gnome app")
        self.win.set_default_size(600, 400)

        #
        self.apply_custom_styles()

        # create toolbar
        toolbar_view = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        # add css-class to header-bar
        header_bar.add_css_class("custom-topbar")
        # add header_bar in toolbar
        toolbar_view.add_top_bar(header_bar)

        # toggle button for switch locale
        toggle_btn = Gtk.Button.new_from_icon_name("object-flip-horizontal-symbolic")
        toggle_btn.set_tooltip_text("Toggle RTL/LTR")
        toggle_btn.connect("clicked", self.on_toggle_direction_clicked)
        # add toggle_btn in header-bar
        header_bar.pack_start(toggle_btn)

        # menu in header_bar
        menu = Gio.Menu.new()
        menu.append("About", "app.about")
        menu.append("Quit", "app.quit")


        # menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_menu_model(menu)
        menu_button.set_icon_name("open-menu-symbolic")

        # add in header_bar
        header_bar.pack_end(menu_button)



        # actions for menu clicks
        self.setup_actions()


        

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
        tab1_box.append(Gtk.Label(label="Tab1"))

        page1 = view_stack.add_titled(tab1_box, "home", "Home")
        page1.set_icon_name("user-home-symbolic") 

        # left: items
        list_box = Gtk.ListBox()
        list_box.add_css_class("boxed-list")

        home_items = [
            ("Local", "folder-download-symbolic"),
            ("Storage", "drive-harddisk-symbolic"),
            ("Users", "avatar-default-symbolic"),
            ("Posts", "mail-send-receive-symbolic"),
            ("Todos", "checkbox-checked-symbolic")
        ]

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



        tab1_box.append(list_box)

        # tab2
        tab2_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        tab2_box.set_margin_top(12)
        tab2_box.append(Gtk.Label(label="tab2"))

        page2 = view_stack.add_titled(tab2_box, "settings", "Settings")
        page2.set_icon_name("emblem-system-symbolic")


        #tab3
        tab3_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        tab3_box.set_margin_top(12)
        tab3_box.append(Gtk.Label(label="tab3"))

        page3 = view_stack.add_titled(tab3_box, "profile", "Profile")
        page3.set_icon_name("avatar-default-symbolic")


        # view_switcher
        view_switcher = Adw.ViewSwitcher()
        view_switcher.set_stack(view_stack)
        
        view_switcher.set_margin_top(6)
        #view_switcher.set_margin_start(6)
        #view_switcher.set_margin_end(6)
        #view_switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        view_switcher.add_css_class("custom-view-switcher-bg")


        # view_switcher_bar
        # bottom viewSwitcherBar
        view_switcher_bar = Adw.ViewSwitcherBar()
        view_switcher_bar.set_stack(view_stack)
        view_switcher_bar.set_reveal(True)

        # add in left_sidebar
        left_sidebar.append(view_switcher)
        left_sidebar.append(view_stack)
        left_sidebar.append(view_switcher_bar)
        
        
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

        # View C: users_container
        self.users_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.users_container.set_margin_top(24)
        self.users_container.set_margin_bottom(24)
        self.users_container.set_margin_start(24)
        self.users_container.set_margin_end(24)

        scroll_win.set_child(self.users_container)
        self.center_stack.add_named(scroll_win, "users_view")

        # set default view state
        self.center_stack.set_visible_child_name("welcome_view")



        #self.info_label = Gtk.Label(label="Current Layout: LTR")
        #self.info_label.set_vexpand(True)
        #center_content.append(self.info_label)
        
         
         
        # right-sidebar 
        self.right_sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        #self.right_sidebar.add_css_class("sidebar-panel")
        self.right_sidebar.set_size_request(200, -1)
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
        outer_split_view = Adw.OverlaySplitView()
        outer_split_view.set_sidebar(self.right_sidebar)
        outer_split_view.set_content(inner_split_view)
        outer_split_view.set_sidebar_position(Gtk.PackType.END)
        outer_split_view.set_min_sidebar_width(200)

       


        #
        toolbar_view.set_content(outer_split_view)
        self.win.set_content(toolbar_view)
        #win.set_content(box)
        self.win.present()

    
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
             border-right: 1px solid; #cccccc;
          }

          .custom-view-switcher-bg {
             background-color: #d0e1f9;
             padding: 6px;
             border-bottom: 1px solid #b0c4de;
          }

          splitview > box:last-child {
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


        

        """
        # create css provider
        css_provider = Gtk.CssProvider()
        #css_provider.load_from_data(css_data)

        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_file_path = os.path.join(current_dir, "style.css")

        try:
            css_provider.load_from_data(css_file_path)  
            #
            # attach css provider globally
            display = Gdk.Display.get_default()
            if display:
                Gtk.StyleContext.add_provider_for_display(
                    display,
                    css_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
            print("css file loaded successfully")

        except Exception as e:
            print(f"Error loading css file from disk: {e}")

        

    
    def on_home_item_clicked(self, row):
        clicked_title = row.get_title()

        if clicked_title == "Users":
            #self.center_stack.set_visible_child_name("loading_view")
            #
            thread = threading.Thread(target=self.fetch_users)
            thread.daemon = True
            thread.start()


        else:
            #self.center_stack.set_visible_child_name("welcome_view")
            self.info_label.set_text(f"Selected Section: {clicked_title}")
        # call fetching

    
     # fetch
    def fetch_users(self):
        
        try:
         url = "https://jsonplaceholder.typicode.com/users"
         req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
         with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(data)
            GLib.idle_add(self.update_users_ui, data)
        except Exception as e:
            print(f"Network error: {e}")
            GLib.idle_add(self.update_users_ui, None)
            


    def update_users_ui(self, users_list):
        print("fetched users:", users_list)
        while child := self.users_container.get_first_child():
            self.users_container.remove(child)
        #
        if not users_list:
            error_lbl = Gtk.Label(label="Failed to pull profile records.")
            self.users_container.append(error_lbl)
            self.center_stack.set_visible_child_name("users_view")
            return
        #
        pref_group = Adw.PreferencesGroup()
        pref_group.set_title("Registered System Users")
        pref_group.set_description("Click any user card to view full profile")

        for user in users_list:
            user_card = Adw.ActionRow()
            user_card.set_title(user.get("name", "Unknown"))
            user_card.set_subtitle(user.get("email", "No Email"))
            user_card.set_margin_bottom(8)

            #
            user_card.set_activatable(True)
            #
            user_card.user_data_payload = user

            #
            avatar = Gtk.Image.new_from_icon_name("avatar-default-symbolic")
            user_card.add_prefix(avatar)

            #
            phone_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            phone_box.set_valign(Gtk.Align.CENTER)
            #
            phone_icon = Gtk.Image.new_from_icon_name("")
            phone_lbl = Gtk.Label(label=user.get("phone", "No Phone"))
            phone_lbl.add_css_class("dim-label")
            #
            phone_box.append(phone_icon)
            phone_box.append(phone_lbl)
            #
            user_card.add_suffix(phone_box)
            #
            user_card.connect("activated", self.on_user_card_clicked)
            #
            pref_group.add(user_card)
            #
            # add to screen layout and hide the loading spinner
        self.users_container.append(pref_group)
        self.center_stack.set_visible_child_name("users_view")


        
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




    def on_toggle_direction_clicked(self, button):
        print("on_toggle_direction_clicked")
        curr_direction = Gtk.Widget.get_default_direction()

        if curr_direction == Gtk.TextDirection.RTL:
            Gtk.Widget.set_default_direction(Gtk.TextDirection.LTR)
            self.win.set_direction(Gtk.TextDirection.LTR)
            self.info_label.set_text("Current Layout: LTR")
        else:
            Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)
            self.win.set_direction(Gtk.TextDirection.RTL)
            self.info_label.set_text("Current Layout: RTL")
        #
        #self.info_label.queue_allocate()


    def setup_actions(self):

        # Quite Action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_clicked)
        self.add_action(quit_action)

        # About Action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_clicked)
        self.add_action(about_action)


    def on_quit_clicked(self, action, parameter):
        print("on_quit_clicked")

    def on_about_clicked(self, action, parameter):
        print("on_about_clicked")
        about = Adw.AboutWindow(
            application_name="Mein Gnome app",
            version="1.0.0",
            developer_name="Mostafa",
            transient_for=self.get_active_window()
        )
        about.present()

    
   
if __name__ == "__main__":
    print("main...")
    app = MyApp()
    app.run()