import tkinter as tk
from gui import create_gui
from gesture_module import start_video_thread, stop_video_thread
from voice_module import start_voice_thread, stop_voice_thread

# Tkinter root
root = tk.Tk()
root.title("Multimodal Input System")
root.geometry("1000x700")

# Voice and gesture toggles
voice_thread = None
gesture_thread = None

# Callbacks
def toggle_voice_input(is_enabled):
    if is_enabled:
        log_text.insert(tk.END, "Voice input enabled\n")
        voice_indicator.config(text="Voice Status: Listening...", bg="#28a745", fg="white")
        start_voice_thread(log_text, voice_indicator)
    else:
        log_text.insert(tk.END, "Voice input disabled\n")
        voice_indicator.config(text="Voice Status: Inactive", bg="#cccccc", fg="black")
        stop_voice_thread()

def toggle_gesture_input(is_enabled):
    if is_enabled:
        log_text.insert(tk.END, "Gesture input enabled\n")
        start_video_thread(output_label, log_text)
    else:
        log_text.insert(tk.END, "Gesture input disabled\n")
        stop_video_thread()

# Build GUI
voice_var, gesture_var, output_label, log_text, voice_indicator = create_gui(
    root, toggle_voice_input, toggle_gesture_input
)

root.mainloop()