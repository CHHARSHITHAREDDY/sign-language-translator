# 🧠🔤 Speech to Sign Language Translator

A Python-based desktop application that converts spoken or typed text into corresponding sign language animations using GIFs.

## 🚀 Features
- 🎙️ Speech-to-text recognition using `speech_recognition`
- ✍️ Text-to-sign translation using preloaded sign GIFs
- 🖼️ Smooth animation playback via Tkinter UI
- 🔤 Fallback to alphabet signs when word GIF is not available

🧠 How it works
Speak or enter a sentence.

App checks if full-word .webp exists.

If yes → plays that GIF.

If no → falls back to alphabet letter-by-letter signing.

Displayed using a Tkinter GUI.
