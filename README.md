Here is a draft for the `README.md` file:

---

# Digital Reading Assistant - ReadAloud

This project is a Digital Reading Assistant developed as an undergraduate project at the Department of Electrical & Computer Engineering, University of Peloponnese for the course "Digital Sound and Image Processing." The project was performed by Tzavara A., under the supervision of Associate Prof. Athanasios Koutras.

## Description

The Digital Reading Assistant is a versatile tool designed to help users with text-to-speech and speech-to-text functionalities, along with the ability to read files, describe images, and extract text from PDFs. The project includes the following features:

1. **Voice Input:** Converts spoken words into text using Google's Speech Recognition API.
2. **Text-to-Speech:** Reads aloud text using ElevenLabs' Text-to-Speech service.
3. **File Reading:** Opens text files and displays the content in the application.
4. **PDF Reading:** Extracts text content from PDF files and displays it in the application.
5. **Image Description:** Uses a YOLO-based model to detect objects in images and provide a description.

The application is built using Python's `tkinter` library for the graphical user interface.

## Features

- **Real-time voice-to-text conversion**
- **Text reading using advanced speech synthesis**
- **File and PDF content display**
- **Basic image recognition and description capabilities**
- **Graphical interface for user-friendly interaction**

## Requirements

To run this project, the following dependencies must be installed:

- Python 3.7 or higher
- `tkinter` for the graphical user interface (usually included with Python)
- `speech_recognition` for converting speech to text
- `Pillow` for handling images
- `PyPDF2` for reading PDFs
- `elevenlabs` for text-to-speech synthesis
- `opencv-python` for image processing
- `numpy` for numerical operations
- `pyttsx3` as an optional text-to-speech fallback (if desired)

You will also need to set up an API key for ElevenLabs and a Google Cloud credentials JSON file for the Speech-to-Text service.

## Setup Instructions

1. **Install Python Dependencies:**
   ```
   pip install tkinter speechrecognition pillow pypdf2 elevenlabs opencv-python numpy
   ```

2. **Configure API Keys:**
   - Replace the placeholder `API_KEY` in the code with your ElevenLabs API key.
   - Make sure the `Google Cloud` credentials file (`speech2text.json`) is set up and accessible.

3. **Run the Application:**
   ```
   python readaloud.py
   ```

## Usage Notes

- The application requires a microphone for voice input and speakers or headphones for audio output.
- Make sure the specified Google Cloud credentials and ElevenLabs API key are valid.
- The image description functionality relies on a pre-trained YOLO model, which should be configured with appropriate weights and configuration files.

## License

This project is intended for educational purposes and may not be used for commercial applications without proper licensing.

---

Feel free to edit and expand this draft to include more specific details or instructions.
