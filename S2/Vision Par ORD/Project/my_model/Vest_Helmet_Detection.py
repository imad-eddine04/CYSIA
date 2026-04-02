import customtkinter
from tkinter import filedialog
import cv2
from ultralytics import YOLO
import threading


#model wil be downloaded automaticaly in the first run
#if you have another model , just paste the url on MODEL_PATH = "your model"
MODEL_PATH = "my_model.pt"

#--- GUI APPEARANCE ---
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #--- WINDOW SETUP ---
        self.title("Vision Par Ordinateur Project")
        self.geometry("500x350")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        #--- WIDGETS ---
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

        #--- LOAD THE MODEL ---
        #Load the model once to avoid reloading it every time.
        self.model = YOLO(MODEL_PATH)
        print(f"Successfully loaded the model: {MODEL_PATH}")

    #--CORE FUNCTIONS ---
    def run_on_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=(("Image Files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
        )
        if not file_path:
            return

        #run detection in a separate thread to keep the GUI responsive
        thread = threading.Thread(target=self._process_image, args=(file_path,))
        thread.start()

    def _process_image(self, file_path):
        results = self.model(file_path, stream=False)  #stream=False for single images
        for r in results:
            im_array = r.plot()  #r.plot() returns a BGR numpy array
            cv2.imshow("Model Detection", im_array)
        cv2.waitKey(0)  #Wait for a key press to close the window
        cv2.destroyAllWindows()

    def run_on_video(self):
        file_path = filedialog.askopenfilename(
            title="Select a Video",
            filetypes=(("Video Files", "*.mp4 *.avi *.mov"), ("All files", "*.*"))
        )
        if not file_path:
            return

        #run detection in a separate thread so the main menu is saved
        thread = threading.Thread(target=self._process_stream, args=(file_path,))
        thread.start()

    def run_on_camera(self):
        #Use 0 for the default webcam
        thread = threading.Thread(target=self._process_stream, args=(0,))
        thread.start()

    def _process_stream(self, source):
        """Processes a video file or live camera stream."""
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"Error: Could not open video source '{source}'")
            return

        #Create a named window and make it full screen
        cv2.namedWindow("model Detection", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("model Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            success, frame = cap.read()
            if not success:
                break

            #Run YOLOv8 inference on the frame
            results = self.model(frame, stream=True, verbose=False)

            #Visualize the results on the frame
            for r in results:
                annotated_frame = r.plot()
                cv2.imshow("model Detection", annotated_frame)

            #Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = App()
    app.mainloop()

