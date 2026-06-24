import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib, Gdk

import sys
import urllib.request
import threading
import json
import os

print("start py")

# dark, i18n, search, cache
# save users, posts, comments in json files in init/background
# search in: local, storage, users


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
           


class MyApp(Adw.Application):

    state = ""
    def __init__(self):
        print("MyApp init")
        super().__init__(
            application_id="com.example.myapp", 
            flags=Gio.ApplicationFlags.FLAGS_NONE
            )
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
        self.data_file_path = os.path.join(curr_dir, "local_data.json")
        self.disk_items_storage = self.load_data_from_disk()
        self.disk_items_group = Adw.PreferencesGroup()

    

    def load_data_from_disk(self):
        if os.path.exists(self.data_file_path):
            try:
                with open(self.data_file_path, "r") as f:
                    
                    return json.load(f)
              
            except Exception as e:
                print(f"Error reading data file: {e}")
        return []
    
    def save_data_to_disk(self):
        try:
            with open(self.data_file_path, "w") as f:
                json.dump(self.disk_items_storage, f, indent=4)
        except Exception as e:
            print(f"Error saving data file: {e}")



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
        #view_switcher_bar.set_stack(view_stack)
        #view_switcher_bar.set_reveal(True)

        # add in left_sidebar
        left_sidebar.append(view_switcher)
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
        self.sidebar_search_entry.set_placeholder_text("Search records...")

        self.sidebar_search_entry.connect("search-changed", self.on_sidebar_search_changed)

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
        #self.jam.build_test_view()
        self.build_test_posts_view()
        self.build_test_todos_view()

        # test jasmin
        j = self.jam.get_name()
        print(f"jam: {j}")


        # View E: Local
        self.build_local_tabs_view()

        # View F: storage in disk
        self.build_disk_tabs_view()

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

            if not self.local_items_storage:
                print("Cannot search because no data!")
                return
            filtered_data = []
            for item in self.local_items_storage:
                name = item.get("name", "").lower()
                description = item.get("description", "").lower()
                #
                if search_query in name or search_query in description:
                    filtered_data.append(item)

            
            if not filtered_data:
                return False
            
            self.display_local_filtered_results(filtered_data)
            
           

            print(f"Memory filter match loop complete, Rendering {len(filtered_data)} matches")
        elif active_view_name == "disk_view":
             print("disk_view")
        

        elif active_view_name == "local_test_users_view":
            print("local_test_users_view")

        elif active_view_name == "local_test_posts_view":
            print("local_test_posts_view")

        elif active_view_name == "local_test_todos_view":
            print("local_test_todos_view")



            
    


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

        local_items_group = Adw.PreferencesGroup()
        local_items_group.set_title("Users")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(local_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.center_stack.add_named(local_wrapper, "local_test_users_view")


        docs = []   


        def test_fetch():
            print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            
            file_path = os.path.join(GLib.get_current_dir(), "./data/users.json")

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
                        card.set_title(item.get("name", "test"))
                        card.set_subtitle(item.get("email", "test"))
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

    def build_test_posts_view(self):
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

        local_items_group = Adw.PreferencesGroup()
        local_items_group.set_title("Users")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(local_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.center_stack.add_named(local_wrapper, "local_test_posts_view")


        docs = []   


        def test_fetch():
            print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            
            file_path = os.path.join(GLib.get_current_dir(), "./data/posts.json")

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
                        card.set_subtitle(item.get("body", "test"))
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


    def build_test_comments_by_postId_view(self, parent_container, postId):
       print(f"build_test_comments_by_postId_view : {postId}")
       #
       def test_fetch():
            print("test_fetch")
            import time


            #for child in self.right_sidebar.observe_children():
                    #self.right_sidebar.remove(child)

            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            
            file_path = os.path.join(GLib.get_current_dir(), "./data/comments.json")

            if not os.path.exists(file_path):
                print("no json file")
                return False
            
            print("json file exists!")

           

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


            try:
                success, content = GLib.file_get_contents(file_path)

                if success:
                    if isinstance(content, bytes):
                        content = content.decode("utf-8")
                        
                    data = json.loads(content)
                    print(f"data size: {len(data)}")

                    comment_count = 0
                    
                    for item in data:
                        pid = item.get("postId")
                        #id = item.get("id")
                        if pid == postId:
                            print(f"comment item: {item}")
                            #docs.append(item)
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
                    
                    # --- ACTION TAKEN HERE ---
                    # Now that docs is populated, safely trigger your UI updates or prints:
                    #print(f"len docs inside callback: {len(docs)}")

                    #local_items_group.queue_resize()
                    #sidebar_group.queue_resize()
                     # If no comments found, show a message
                    if comment_count == 0:
                        empty_label = Gtk.Label(label="No comments for this post")
                        empty_label.add_css_class("dim-label")
                        empty_label.set_margin_top(12)
                        empty_label.set_margin_bottom(12)
                        comments_group.add(empty_label)
                    
                    comments_group.queue_resize()
                    
                    

                else:
                    print("GLib failed to read comments file contents successfully.")
            except Exception as e:
                print(f"ERROR: {e}")

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

        local_items_group = Adw.PreferencesGroup()
        local_items_group.set_title("test ui")


        # PRE-PACK HIERARCHY: Assemble the structure before the async population starts
        content_box.append(local_items_group)
        scroll_win.set_child(content_box)
        local_wrapper.set_content(scroll_win)
        
        # Mount layout to stack structure immediately 
        self.center_stack.add_named(local_wrapper, "local_test_todos_view")


        docs = []   


        def test_fetch():
            print("test_fetch")
            import time
            time.sleep(0.1)  # Note: blocking sleep here blocks the main thread if called via idle_add
            
            file_path = os.path.join(GLib.get_current_dir(), "./data/todos.json")

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
                        #card.set_subtitle(item.get("author", "test"))
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


    
    def build_local_tabs_view(self):
        #
        print(f"state#: {self.state}")
        #
        local_wrapper = Adw.ToolbarView()

        local_action_bar = Gtk.HeaderBar()
        local_action_bar.set_show_title_buttons(False)

        #
        local_title = Gtk.Label(label="Local List Manager")
        local_title.add_css_class("heading")
        local_action_bar.set_title_widget(local_title)
        #
        self.add_item_btn = Gtk.Button(label="Add")
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
        popover_title = Gtk.Label(label="Add New One")
        popover_title.add_css_class("title-3")
        popover_title.set_halign(Gtk.Align.START)
        form_box.append(popover_title)
        # inputs
        self.input_name = Gtk.Entry(placeholder_text="Enter name...")
        form_box.append(self.input_name)

        self.input_desc = Gtk.Entry(placeholder_text="Enter description")
        form_box.append(self.input_desc)

        # submit button
        submit_btn = Gtk.Button(label="Submit")
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
        self.local_items_group.set_title("Stored Local Entries")

        #
        

        #
        self.empty_list_lbl = Gtk.Label(label="No items recorded yet. click 'Add' above to build a list.")
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
        local_title = Gtk.Label(label="Disk List Manager")
        local_title.add_css_class("heading")
        local_action_bar.set_title_widget(local_title)
        #
        self.add_disk_item_btn = Gtk.Button(label="Add")
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
        popover_title = Gtk.Label(label="Add New One")
        popover_title.add_css_class("title-3")
        popover_title.set_halign(Gtk.Align.START)
        form_box.append(popover_title)
        # inputs
        self.input_disk_name = Gtk.Entry(placeholder_text="Enter name...")
        form_box.append(self.input_disk_name)

        self.input_disk_desc = Gtk.Entry(placeholder_text="Enter description")
        form_box.append(self.input_disk_desc)

        # submit button
        submit_btn = Gtk.Button(label="Submit")
        submit_btn.add_css_class("suggested-action")
        submit_btn.connect("clicked", self.on_form_disk_submitted)
        form_box.append(submit_btn)

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
        self.disk_items_group = Adw.PreferencesGroup()
        self.disk_items_group.set_title("Stored Data in Disk with Entries")

        #
        

        #
        if not self.disk_items_storage:
          self.empty_disk_list_lbl = Gtk.Label(label="No items recorded yet. click 'Add' above to build a list.")
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
            self.jam.set_name("home-jam")
            print(f"jam-name: {self.jam.get_name()}")
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
            #self.center_stack.set_visible_child_name("loading_view")
            self.center_stack.set_visible_child_name("local_test_posts_view")

        elif clicked_title == "Todos":
            print("Todos item")
            #self.center_stack.set_visible_child_name("loading_view")
            self.center_stack.set_visible_child_name("local_test_todos_view")
            
        


        else:
            #self.center_stack.set_visible_child_name("welcome_view")
            self.info_label.set_text(f"Selected Section: {clicked_title}")
            self.state = ""
        # call fetching

    
     # fetch users

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