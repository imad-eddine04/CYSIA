import customtkinter
from tkinter import filedialog
import cv2
from ultralytics import YOLO
import threading
import numpy as np

MODEL_PATH = "my_model.pt"

# --- ICON PATHS ---
ICON_PATHS = {
    "person": "icons/person.png",
    "helmet": "icons/helmet.png",
    "vest":   "icons/vest.png",
}

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Vision Par Ordinateur Project")
        self.geometry("500x350")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(
            self.main_frame, text="Choose an Input Source", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label.pack(pady=30, padx=10)

        self.image_button = customtkinter.CTkButton(
            self.main_frame, text="Upload Image", command=self.run_on_image
        )
        self.image_button.pack(pady=12, padx=10)

        self.video_button = customtkinter.CTkButton(
            self.main_frame, text="Upload Video", command=self.run_on_video
        )
        self.video_button.pack(pady=12, padx=10)

        self.camera_button = customtkinter.CTkButton(
            self.main_frame, text="Use Live Camera", command=self.run_on_camera
        )
        self.camera_button.pack(pady=12, padx=10)

        self.model = YOLO(MODEL_PATH)
        print(f"Successfully loaded the model: {MODEL_PATH}")
        print(f"Model classes: {self.model.names}")

        # --- LOAD & RESIZE ICONS ONCE ---
        self.icons = self._load_icons(size=28)

    def _load_icons(self, size=28):
        """Load icons from disk, resize them, and return as a dict of BGRA numpy arrays."""
        icons = {}
        for key, path in ICON_PATHS.items():
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # keep alpha channel if exists
            if img is None:
                print(f"Warning: Could not load icon '{path}', will skip icon for '{key}'")
                icons[key] = None
                continue

            # If no alpha channel, add one (fully opaque)
            if img.shape[2] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

            icons[key] = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)
        return icons

    def _overlay_icon(self, frame, icon, x, y):
        """Paste a BGRA icon onto a BGR frame at position (x, y) using alpha blending."""
        if icon is None:
            return

        ih, iw = icon.shape[:2]
        fh, fw = frame.shape[:2]

        # Clamp to frame boundaries
        x1, y1 = max(x, 0), max(y, 0)
        x2, y2 = min(x + iw, fw), min(y + ih, fh)
        ix1, iy1 = x1 - x, y1 - y
        ix2, iy2 = ix1 + (x2 - x1), iy1 + (y2 - y1)

        if x2 <= x1 or y2 <= y1:
            return

        icon_crop  = icon[iy1:iy2, ix1:ix2]
        frame_crop = frame[y1:y2, x1:x2]

        alpha = icon_crop[:, :, 3:4].astype(np.float32) / 255.0
        icon_bgr = icon_crop[:, :, :3].astype(np.float32)
        frame_bgr = frame_crop.astype(np.float32)

        blended = (alpha * icon_bgr + (1 - alpha) * frame_bgr).astype(np.uint8)
        frame[y1:y2, x1:x2] = blended

    def _draw_stats(self, frame, stats):
        """Draws a semi-transparent stats box with icons on the top-left of the frame."""
        labels = [
            ("person", "Persons", stats["person"], (255, 200,   0)),  # yellow
            ("helmet", "Helmets", stats["helmet"], (  0, 255, 120)),  # green
            ("vest",   "Vests",   stats["vest"],   (  0, 180, 255)),  # orange
        ]

        icon_size   = 28
        row_height  = 40
        box_x, box_y = 10, 10
        box_w = 250
        box_h = 36 + len(labels) * row_height

        overlay = frame.copy()
        cv2.rectangle(overlay, (box_x, box_y), (box_x + box_w, box_y + box_h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        # Title
        cv2.putText(frame, "Live Statistics", (box_x + 10, box_y + 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        for i, (key, label, count, color) in enumerate(labels):
            row_y = box_y + 36 + i * row_height

            # Icon (vertically centered in the row)
            icon_y = row_y + (row_height - icon_size) // 2
            self._overlay_icon(frame, self.icons.get(key), box_x + 10, icon_y)

            # Text next to icon
            text_x = box_x + 10 + icon_size + 8
            text_y = row_y + (row_height + 10) // 2
            cv2.putText(frame, f"{label}: {count}", (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # ── image ──────────────────────────────────────────────────────────────────

    def run_on_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=(("Image Files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
        )
        if not file_path:
            return
        thread = threading.Thread(target=self._process_image, args=(file_path,))
        thread.start()

    def _process_image(self, file_path):
        results = self.model(file_path, stream=False)
        for r in results:
            im_array = r.plot()
            stats = {"person": 0, "helmet": 0, "vest": 0}
            for box in r.boxes:
                class_id   = int(box.cls[0])
                class_name = self.model.names[class_id].lower()
                if class_name in stats:
                    stats[class_name] += 1
            self._draw_stats(im_array, stats)
            cv2.imshow("Model Detection", im_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # ── video ──────────────────────────────────────────────────────────────────

    def run_on_video(self):
        file_path = filedialog.askopenfilename(
            title="Select a Video",
            filetypes=(("Video Files", "*.mp4 *.avi *.mov"), ("All files", "*.*"))
        )
        if not file_path:
            return
        thread = threading.Thread(target=self._process_stream, args=(file_path,))
        thread.start()

    # ── camera ─────────────────────────────────────────────────────────────────

    def run_on_camera(self):
        thread = threading.Thread(target=self._process_stream, args=(0,))
        thread.start()

    # ── shared stream loop ─────────────────────────────────────────────────────

    def _process_stream(self, source):
        """Processes a video file or live camera stream."""
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"Error: Could not open video source '{source}'")
            return

        cv2.namedWindow("Model Detection", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Model Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            success, frame = cap.read()
            if not success:
                break

            results = self.model(frame, stream=True, verbose=False)
            stats   = {"person": 0, "helmet": 0, "vest": 0}

            for r in results:
                annotated_frame = r.plot()
                for box in r.boxes:
                    class_id   = int(box.cls[0])
                    class_name = self.model.names[class_id].lower()
                    if class_name in stats:
                        stats[class_name] += 1
                self._draw_stats(annotated_frame, stats)
                cv2.imshow("Model Detection", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = App()
    app.mainloop()