import customtkinter
from PIL import Image, ImageEnhance

# --- Configuration ---
BACKGROUND_IMAGE_PATH = "background.jpg"
DISPLAY_SIZE = (960, 540)
ICON_FOLDER = "icons"  # Path to your new icons folder


class UIDesigner:
    """
    This class is responsible for creating and laying out all the UI elements.
    """

    def __init__(self, app_instance):
        self.app = app_instance
        self.video_display_label = None
        self.stats_frame = None  # We now use a frame to hold stats widgets
        self.loaded_icons = self.load_icons()

    def load_icons(self):
        """Loads icons from the icon folder into a dictionary."""
        icons = {}
        try:
            icons["person"] = customtkinter.CTkImage(Image.open(f"{ICON_FOLDER}/person.png"), size=(24, 24))
            icons["helmet"] = customtkinter.CTkImage(Image.open(f"{ICON_FOLDER}/helmet.png"), size=(24, 24))
            icons["vest"] = customtkinter.CTkImage(Image.open(f"{ICON_FOLDER}/vest.png"), size=(24, 24))
        except FileNotFoundError as e:
            print(f"Warning: Could not load icon. {e}")
        return icons

    def create_home_frame(self):
        """Creates and returns the home screen frame."""
        home_frame = customtkinter.CTkFrame(self.app, corner_radius=0)
        home_frame.grid(row=0, column=0, sticky="nsew")

        try:
            original_image = Image.open(BACKGROUND_IMAGE_PATH)
            darkened_image = ImageEnhance.Brightness(original_image).enhance(0.5)
            bg_image = customtkinter.CTkImage(darkened_image, size=(1300, 700))
            background_label = customtkinter.CTkLabel(home_frame, image=bg_image, text="")
            background_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            print(f"Warning: Background image not found at '{BACKGROUND_IMAGE_PATH}'")

        # --- UI ENHANCEMENT: SEMI-TRANSPARENT MENU ---
        # Instead of a transparent frame, we create one with a low alpha color.
        menu_frame = customtkinter.CTkFrame(home_frame, fg_color=("#333333", "#222222"), corner_radius=15,
                                            border_width=1, border_color="#444444")
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = customtkinter.CTkLabel(menu_frame, text="SAFETY MONITORING",
                                             font=customtkinter.CTkFont(size=40, weight="bold"))
        title_label.pack(pady=(20, 30), padx=50)

        # --- UI ENHANCEMENT: ROUNDED, GLOWING BUTTONS ---
        button_font = customtkinter.CTkFont(size=18, weight="bold")

        live_camera_button = customtkinter.CTkButton(
            menu_frame, text="Live Camera", command=self.app.start_live_camera, height=50,
            font=button_font, corner_radius=25, fg_color="#28a745", hover_color="#32CD32"
        )
        live_camera_button.pack(pady=10, padx=20, fill="x")

        process_image_button = customtkinter.CTkButton(
            menu_frame, text="Process Image", command=self.app.start_image_processing, height=50,
            font=button_font, corner_radius=25, fg_color="#007bff", hover_color="#0096FF"
        )
        process_image_button.pack(pady=10, padx=20, fill="x")

        process_video_button = customtkinter.CTkButton(
            menu_frame, text="Process Video", command=self.app.start_video_processing, height=50,
            font=button_font, corner_radius=25, fg_color="#007bff", hover_color="#0096FF"
        )
        process_video_button.pack(pady=(10, 20), padx=20, fill="x")

        return home_frame

    def create_main_app_frame(self):
        """Creates and returns the main application interface frame."""
        main_app_frame = customtkinter.CTkFrame(self.app, fg_color="transparent")
        main_app_frame.grid_columnconfigure(0, weight=1)
        main_app_frame.grid_rowconfigure(0, weight=1)

        main_content = customtkinter.CTkFrame(main_app_frame)
        main_content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_content.grid_rowconfigure(0, weight=1)
        main_content.grid_columnconfigure(0, weight=3)
        main_content.grid_columnconfigure(1, weight=1)

        self.video_display_label = customtkinter.CTkLabel(main_content, text="Feed will appear here.",
                                                          font=customtkinter.CTkFont(size=20))
        self.video_display_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        sidebar = customtkinter.CTkFrame(main_content)
        sidebar.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        stats_title = customtkinter.CTkLabel(sidebar, text="Statistics",
                                             font=customtkinter.CTkFont(size=24, weight="bold"))
        stats_title.pack(pady=20, padx=20)

        # --- UI ENHANCEMENT: FRAME FOR ICON-BASED STATS ---
        # This frame will be cleared and repopulated with stats
        self.stats_frame = customtkinter.CTkFrame(sidebar, fg_color="transparent")
        self.stats_frame.pack(pady=10, padx=20, fill="x", anchor="w")

        back_button = customtkinter.CTkButton(sidebar, text="Back to Home (Q)", command=self.app.show_home_frame,
                                              fg_color="#585858", hover_color="#686868")
        back_button.pack(side="bottom", fill="x", padx=20, pady=20)

        return main_app_frame
