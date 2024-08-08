import tkinter as tk
from tkinter import filedialog, messagebox
import assemblyai as aai
import os
from hide import *

# Initialize AssemblyAI
aai.settings.api_key = my_api_key

class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Transcription App")

        self.label = tk.Label(root, text="Choose an video file to transcribe:")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=5)

        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Transcription", command=self.save_transcription, state=tk.DISABLED)
        self.save_button.pack(pady=5)

        self.file_path = None
        self.transcription_text = None

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mov;*.avi")])
        if self.file_path:
            self.transcribe_file()

    def transcribe_file(self):
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(self.file_path)

        if transcript.status == aai.TranscriptStatus.error:
            messagebox.showerror("Error", f"Error: {transcript.error}")
        else:
            self.transcription_text = transcript.text
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.transcription_text)
            self.save_button.config(state=tk.NORMAL)

    def save_transcription(self):
        if self.transcription_text:
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if save_path:
                with open(save_path, "w") as text_file:
                    text_file.write(self.transcription_text)
                messagebox.showinfo("Success", "Transcription saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
