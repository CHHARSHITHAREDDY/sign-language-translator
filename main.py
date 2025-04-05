


import numpy as np
import cv2
import os
import PIL
from PIL import ImageTk
import PIL.Image
import speech_recognition as sr
import tkinter as tk
from tkinter import Label, Text, Button, Frame

def check_sim(word, file_map):
    return file_map.get(word.lower(), None)

def generate_sign_gif(text):
    all_frames = []
    final = PIL.Image.new('RGB', (380, 260))
    words = text.split()
    
    for word in words:
        match = check_sim(word, file_map)
        if match:
            im = PIL.Image.open(os.path.join(op_dest, match))
            for frame_cnt in range(getattr(im, "n_frames", 1)):
                im.seek(frame_cnt)
                frame = im.copy().convert("RGB").resize((380, 260))
                all_frames.append(frame)
        else:
            for char in word:
                try:
                    im = PIL.Image.open(os.path.join(alpha_dest, f"{char.lower()}_small.gif"))
                    for frame_cnt in range(getattr(im, "n_frames", 1)):
                        im.seek(frame_cnt)
                        tmp_path = f"tmp_{char}.png"
                        im.save(tmp_path)
                        img = cv2.imread(tmp_path)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (380, 260))
                        all_frames.append(PIL.Image.fromarray(img))
                        os.remove(tmp_path)
                except FileNotFoundError:
                    continue
        
    final.save("out.gif", save_all=True, append_images=all_frames, duration=100, loop=0)
    return all_frames

class SpeechToSignApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧠 Two-Way Sign Language Translator")
        self.geometry("850x650")
        self.configure(bg="#f0f4f8")

        # Title
        title = Label(self, text="Sign Language Translator", font=("Helvetica", 20, "bold"), bg="#f0f4f8", fg="#333")
        title.pack(pady=20)

        # Frame for input and buttons
        control_frame = Frame(self, bg="#f0f4f8")
        control_frame.pack(pady=10)

        self.label = Label(control_frame, text="Speak or Enter Text Below:", font=("Verdana", 12), bg="#f0f4f8")
        self.label.pack(pady=5)

        self.text_input = Text(control_frame, height=4, width=60, font=("Consolas", 11))
        self.text_input.pack(pady=5)

        button_frame = Frame(control_frame, bg="#f0f4f8")
        button_frame.pack(pady=10)

        self.voice_button = Button(button_frame, text="🎤 Record Voice", font=("Verdana", 10), command=self.hear_voice, bg="#dbeafe", activebackground="#93c5fd")
        self.voice_button.pack(side="left", padx=10)

        self.convert_button = Button(button_frame, text="🔁 Convert to Sign", font=("Verdana", 10), command=self.convert_text, bg="#bbf7d0", activebackground="#86efac")
        self.convert_button.pack(side="left", padx=10)

        self.status_label = Label(control_frame, text="", font=("Verdana", 10), fg="red", bg="#f0f4f8")
        self.status_label.pack(pady=5)

        # Output
        self.gif_label = Label(self, bg="#f0f4f8")
        self.gif_label.pack(pady=20)

    def hear_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.text_input.delete("1.0", "end")
            self.status_label.config(text="🎙️ Listening...")
            self.update()

            audio = recognizer.record(source, duration=5)
            try:
                text_output = recognizer.recognize_google(audio)
                self.text_input.insert("end", text_output)
                self.status_label.config(text="✅ Recognized Successfully")
            except sr.UnknownValueError:
                self.status_label.config(text="⚠️ Could not understand audio.")
            except sr.RequestError:
                self.status_label.config(text="❌ Speech recognition service error.")

    def convert_text(self):
        input_text = self.text_input.get("1.0", "end-1c").strip()
        if not input_text:
            self.status_label.config(text="⚠️ Please enter or speak some text.")
            return
        
        self.status_label.config(text="🔄 Generating sign language GIF...")
        self.update()

        frames = generate_sign_gif(input_text)

        def play_gif(cnt=0):
            if cnt < len(frames):
                imgtk = ImageTk.PhotoImage(frames[cnt])
                self.gif_label.configure(image=imgtk)
                self.gif_label.image = imgtk
                self.after(100, play_gif, cnt + 1)

        play_gif()
        self.status_label.config(text="✅ Done!")

if __name__ == "__main__":
    op_dest = "./filtered_data/"
    alpha_dest = "./alphabet/"
    dir_listing = os.listdir(op_dest)
    file_map = {
        item.replace(".webp", "").lower(): item
        for item in dir_listing
        if item.endswith(".webp")
    }

    app = SpeechToSignApp()
    app.mainloop()
