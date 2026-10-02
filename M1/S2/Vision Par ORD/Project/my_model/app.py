import customtkinter
from tkinter import filedialog
import cv2
from ultralytics import YOLO
import threading
from PIL import Image
import time
import collections

from ui_design import UIDesigner, DISPLAY_SIZE

# --- Configuration ---
MODEL_PATH = "my_model.pt"

# --- High-Performance Global State ---
source_lock = threading.Lock()
latest_frame_from_source = None
latest_processed_data = None
stop_event = threading.Event()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Vision-Based Safety Monitoring")
        self.geometry("1300x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.ui = UIDesigner(self)
        self.home_frame = self.ui.create_home_frame()
        self.main_app_frame = self.ui.create_main_app_frame()

        self.show_home_frame()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.bind("<q>", self.handle_q_press)

    # --- UI Switching and Control Logic ---

    def handle_q_press(self, event=None):
        self.show_home_frame()

    def show_home_frame(self):
        stop_event.set()
        self.main_app_frame.grid_remove()
        self.home_frame.grid()
        self.home_frame.lift()

    def show_main_app_frame(self):
        self.home_frame.grid_remove()
        self.main_app_frame.grid(row=0, column=0, sticky="nsew")

    def on_closing(self):
        stop_event.set()
        self.destroy()

    # --- Button Commands ---

    def start_live_camera(self):
        self.show_main_app_frame()
        start_all_threads(0)
        self.update_gui_loop()

    def start_image_processing(self):
        filepath = filedialog.askopenfilename(title="Select an Image",
                                              filetypes=(("Image Files", "*.jpg *.jpeg *.png"), ("All files", "*.*")))
        if not filepath: return

        self.show_main_app_frame()
        stop_event.set()
        image = cv2.imread(filepath)

        model_instance = YOLO(MODEL_PATH)
        results = model_instance(image)
        annotated_image = results[0].plot()

        stats = collections.Counter()
        for r in results:
            for cls_id in r.boxes.cls:
                stats[model_instance.names[int(cls_id)]] += 1

        self.update_video_display(annotated_image)
        self.update_stats_display(stats)

    def start_video_processing(self):
        filepath = filedialog.askopenfilename(title="Select a Video",
                                              filetypes=(("Video Files", "*.mp4 *.avi *.mov"), ("All files", "*.*")))
        if not filepath: return

        self.show_main_app_frame()
        start_all_threads(filepath)
        self.update_gui_loop()

    # --- GUI Update Logic ---

    def update_gui_loop(self):
        if stop_event.is_set(): return

        if latest_processed_data:
            frame, stats = latest_processed_data
            self.update_video_display(frame)
            self.update_stats_display(stats)

        self.after(30, self.update_gui_loop)

    def update_video_display(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)

        ctk_image = customtkinter.CTkImage(pil_image, size=DISPLAY_SIZE)
        self.ui.video_display_label.configure(image=ctk_image)
        self.ui.video_display_label.image = ctk_image

    def update_stats_display(self, stats):
        for widget in self.ui.stats_frame.winfo_children():
            widget.destroy()

        # Sort the stats so the order is always consistent
        sorted_stats = sorted(stats.items()) if stats else []

        if not sorted_stats:
            no_stats_label = customtkinter.CTkLabel(self.ui.stats_frame, text="No objects detected.",
                                                    font=customtkinter.CTkFont(size=16))
            no_stats_label.pack(anchor="w")
            return

        for class_name, count in sorted_stats:
            stat_line_frame = customtkinter.CTkFrame(self.ui.stats_frame, fg_color="transparent")
            stat_line_frame.pack(fill="x", pady=4)

            icon = self.ui.loaded_icons.get(class_name)
            icon_label = customtkinter.CTkLabel(stat_line_frame, image=icon, text="")
            icon_label.pack(side="left", padx=(0, 10))

            text_label = customtkinter.CTkLabel(stat_line_frame, text=f"{class_name.capitalize()}: {count}",
                                                font=customtkinter.CTkFont(size=18))
            text_label.pack(side="left")


# --- High-Performance Threading Functions ---

def frame_reader_thread(source):
    global latest_frame_from_source
    cap = cv2.VideoCapture(source)
    while not stop_event.is_set() and cap.isOpened():
        success, frame = cap.read()
        if not success: break
        with source_lock:
            latest_frame_from_source = frame
        time.sleep(0.01)
    cap.release()


def frame_processor_thread():
    global latest_processed_data
    model = YOLO(MODEL_PATH)
    while not stop_event.is_set():
        frame_to_process = None
        with source_lock:
            if latest_frame_from_source is not None:
                frame_to_process = latest_frame_from_source.copy()

        if frame_to_process is not None:
            # --- THE FINAL, CORRECTED LOGIC ---
            # Call the model on a single frame WITHOUT stream=True. This returns a list.
            results = model(frame_to_process, verbose=False)

            # The list contains one result object for the frame at index 0.
            result_object = results[0]

            # Use this single result object to get BOTH the annotated image and the stats.
            annotated_frame = result_object.plot()

            stats = collections.Counter()
            for cls_id in result_object.boxes.cls:
                try:
                    stats[model.names[int(cls_id)]] += 1
                except (IndexError, KeyError):
                    pass  # Safely ignore if a class ID is not in the model names

            # Package the correct data together.
            latest_processed_data = (annotated_frame, stats)
            # --- END OF FIX ---
        else:
            time.sleep(0.01)


def start_all_threads(source):
    global latest_frame_from_source, latest_processed_data
    stop_event.set()
    time.sleep(0.1)
    stop_event.clear()
    latest_frame_from_source = None
    latest_processed_data = None
    threading.Thread(target=frame_reader_thread, args=(source,), daemon=True).start()
    threading.Thread(target=frame_processor_thread, daemon=True).start()


# --- Main Execution ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
