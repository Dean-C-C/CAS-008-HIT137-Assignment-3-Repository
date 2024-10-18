import tkinter as tk
from tkinter import messagebox
from langdetect import detect, DetectorFactory
from googletrans import Translator

DetectorFactory.seed = 0  # makes sure of accuarate results from langdetect

# 1. Base Class for Main Application 
class LanguageDetectionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Language Detection & Translation App")
        self.geometry("500x400")
        self.create_widgets()

    # Encapsulation (widget creation)
    def create_widgets(self):
        self.input_frame = InputFrame(self)
        self.input_frame.pack(pady=20)

        self.output_frame = OutputFrame(self)
        self.output_frame.pack(pady=20)

# 2. Input Frame Class
class InputFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="Enter text:")
        self.label.pack()

        self.text_entry = tk.Text(self, height=5, width=50)
        self.text_entry.pack()

        self.detect_button = tk.Button(self, text="Detect Language & Translate", command=self.detect_and_translate)
        self.detect_button.pack(pady=10)

    # how to handle language detection and translation
    def detect_and_translate(self):
        user_text = self.text_entry.get("1.0", tk.END).strip()
        if user_text:
            try:
                # Detects language
                detected_language = detect(user_text)

                # Translates the text (English)
                translator = Translator()
                translated_text = translator.translate(user_text, dest='en').text

                # to detect the languge and display
                self.master.output_frame.display_result(detected_language, translated_text)
            except Exception as e:
                messagebox.showerror("Error", f"Could not detect language or translate: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter some text!")

# Output Frame Class
class OutputFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="Detected Language & Translation:")
        self.label.pack()

        self.result_label = tk.Label(self, text="", font=("Helvetica", 14))
        self.result_label.pack()

        self.translation_label = tk.Label(self, text="", font=("Helvetica", 12), wraplength=400)
        self.translation_label.pack()

    # Method Overriding: Customizing how the result can be changed
    def display_result(self, detected_language, translated_text):
        self.result_label.config(text=f"Detected Language: {detected_language}")
        self.translation_label.config(text=f"Translated Text (to English): {translated_text}")

# Final part
if __name__ == "__main__":
    app = LanguageDetectionApp()
    app.mainloop()

