import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import speech_recognition as sr
from PIL import Image
import PyPDF2
import tempfile
import os
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import atexit
import subprocess
import platform
import cv2
import numpy as np

class TextSpeechApp:
    def __init__(self, root, api_key):
        self.root = root
        self.api_key = api_key
        self.root.title("Digital Reading Assistant")  # Ψηφιακός Βοηθός Ανάγνωσης Κειμένου

        # Create the text area for input or display
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Arial', 12))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a button frame for various actions
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, pady=10)

        # Create buttons for different functionalities
        self.create_buttons()

        # Initialize the ElevenLabs client
        self.client = ElevenLabs(api_key=self.api_key)

        # Initialize a list to keep track of temporary files
        self.temp_files = []
        atexit.register(self.cleanup_temp_files)

    def create_buttons(self):
        buttons = [
            ("Voice Input", self.voice_to_text),  # Φωνητική Εισαγωγή
            ("Open File", self.open_file),  # Άνοιγμα Αρχείου
            ("Image Description", self.image_description),  # Περιγραφή Εικόνας
            ("Open PDF", self.read_pdf),  # Άνοιγμα PDF
            ("Text to Speech", self.text_to_speech)  # Ανάγνωση Κειμένου
        ]
        for text, command in buttons:
            button = tk.Button(self.button_frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=10, expand=True)

    def voice_to_text(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                messagebox.showinfo("Information", "Please speak now.")  # Πληροφορία, Παρακαλώ μιλήστε τώρα.
                audio_data = recognizer.listen(source)
                text = recognizer.recognize_google(audio_data, language='el-GR')
                self.text_area.insert(tk.END, text + '\n')
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand your voice.")  # Σφάλμα, Δεν μπόρεσα να καταλάβω τη φωνή σας.
        except sr.RequestError:
            messagebox.showerror("Error", "There was an issue with the speech recognition service.")  # Σφάλμα, Υπήρξε πρόβλημα με την υπηρεσία αναγνώρισης ομιλίας.

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.text_area.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read the file: {e}")  # Σφάλμα, Δεν ήταν δυνατή η ανάγνωση του αρχείου

    def image_description(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            try:
                description = describe_image(file_path)
                self.text_area.insert(tk.END, f"\n\nImage Description:\n{description}\n")  # Περιγραφή Εικόνας
            except Exception as e:
                messagebox.showerror("Error", f"Could not describe the image: {e}")  # Σφάλμα, Δεν ήταν δυνατή η περιγραφή της εικόνας

    def read_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ''.join([page.extract_text() for page in reader.pages if page.extract_text()])
                    self.text_area.insert(tk.END, f"\n\nPDF Content:\n{text}\n")  # Περιεχόμενο PDF
            except Exception as e:
                messagebox.showerror("Error", f"Could not read the PDF: {e}")  # Σφάλμα, Δεν ήταν δυνατή η ανάγνωση του PDF

    def text_to_speech(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if text:
            try:
                # Generate audio using ElevenLabs
                audio = self.client.generate(text=text, 
                                            voice='Rachel',
                                            model="eleven_multilingual_v2")

                # Check if the result is a generator or iterable, and write to file in chunks
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    # If 'audio' is an iterable or generator, write it chunk by chunk
                    if isinstance(audio, (bytes, bytearray)):
                        # Directly write if it's a byte-like object
                        tmp_file.write(audio)
                    else:
                        for chunk in audio:
                            tmp_file.write(chunk)

                    tmp_file_path = tmp_file.name

                # Keep track of the temporary file for cleanup
                self.temp_files.append(tmp_file_path)

                # Play the audio using a cross-platform method
                if platform.system() == "Darwin":  # macOS
                    subprocess.run(["afplay", tmp_file_path])
                elif platform.system() == "Linux":
                    subprocess.run(["xdg-open", tmp_file_path])
                else:  # Windows
                    os.startfile(tmp_file_path)

            except Exception as e:
                messagebox.showerror("Error", f"There was an issue with the ElevenLabs service: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter text for reading.")

    def cleanup_temp_files(self):
        for file_path in self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass

# Function for describing an image using an external model (placeholder for now)
def describe_image(image_path, yolo_dir='./yolo_files', confidence_threshold=0.25):
    # Paths to YOLO files
    weights_path = os.path.join(yolo_dir, "yolov3.weights")
    config_path = os.path.join(yolo_dir, "yolov3.cfg")
    names_path = os.path.join(yolo_dir, "coco.names")

    # Load YOLO
    net = cv2.dnn.readNet(weights_path, config_path)
    with open(names_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Load image
    image = cv2.imread(image_path)
    height, width, _ = image.shape

 # Detect objects
    blob = cv2.dnn.blobFromImage(image, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    # Get bounding boxes, confidences, and class IDs
    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Max Suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)
    
    objects = [classes[class_ids[i]] for i in indexes]
    unique_objects = list(set(objects))

    if not unique_objects:
        return "No objects detected with confidence above " + str(confidence_threshold)
    
    description = "This image contains: " + ", ".join(unique_objects[:5])
    return description


if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual API key for ElevenLabs
    API_KEY = 'REPLACE WITH YOUR API KEY FROM ELEVENLABS'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'speech2text.json' #use your own json file from google
    root = tk.Tk()
    app = TextSpeechApp(root, API_KEY)
    root.mainloop()