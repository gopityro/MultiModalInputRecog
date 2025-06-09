import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # for using icons

def create_gui(root, toggle_voice_callback, toggle_gesture_callback):
    voice_var = tk.BooleanVar()
    gesture_var = tk.BooleanVar()

    # Colors
    background_color = "#f4f6f9"
    frame_color = "#f4f6f9"
    highlight_color = "#0b5394"
    log_bg = "#1e1e1e"
    log_fg = "#00ff00"

    root.configure(bg=background_color)
    root.title("Multimodal Input System")
    root.geometry("900x600")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    root.rowconfigure(0, weight=4)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=0)

    # Load icons
    try:
        voice_img = Image.open("voice_icon.png").resize((20, 20), Image.ANTIALIAS)
        gesture_img = Image.open("hands.png").resize((20, 20), Image.ANTIALIAS)
        voice_icon = ImageTk.PhotoImage(voice_img)
        gesture_icon = ImageTk.PhotoImage(gesture_img)
    except Exception:
        voice_icon = gesture_icon = None  # fallback if icons not found

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabelFrame", background=frame_color, font=("Segoe UI", 12, "bold"))
    style.configure("TLabelframe.Label", foreground=highlight_color, background=frame_color)
    style.configure("TCheckbutton", font=("Segoe UI", 11), background=frame_color)

    # Frame for toggles
    toggle_frame = ttk.LabelFrame(root, text="Enable Inputs", padding=20)
    toggle_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    voice_toggle = ttk.Checkbutton(toggle_frame, text=" Voice Input",
                                   image=voice_icon, compound="left",
                                   variable=voice_var,
                                   command=lambda: toggle_voice_callback(voice_var.get()))
    gesture_toggle = ttk.Checkbutton(toggle_frame, text=" Hand Gestures",
                                     image=gesture_icon, compound="left",
                                     variable=gesture_var,
                                     command=lambda: toggle_gesture_callback(gesture_var.get()))

    voice_toggle.image = voice_icon
    gesture_toggle.image = gesture_icon

    voice_toggle.pack(pady=5, padx=10, anchor="w")
    gesture_toggle.pack(pady=5, padx=10, anchor="w")

    # Frame for output
    output_frame = ttk.LabelFrame(root, text="Video Stream", padding=10)
    output_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    output_label = tk.Label(output_frame, bg="black", relief="sunken", bd=2)
    output_label.pack(expand=True, fill="both", padx=10, pady=10)

    # Log area
    log_frame = ttk.LabelFrame(root, text="Logs", padding=10)
    log_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

    log_text = tk.Text(log_frame, wrap="word", height=8,
                       font=("Consolas", 10), bg=log_bg, fg=log_fg,
                       insertbackground="white", relief="flat", bd=1)
    log_text.pack(expand=True, fill="both", padx=5, pady=5)

    # Voice status indicator
    voice_indicator = tk.Label(root, text="🎤 Voice Status: Inactive",
                               bg="#d3d3d3", fg="black", font=("Segoe UI", 11),
                               anchor="w", padx=10)
    voice_indicator.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))

    return voice_var, gesture_var, output_label, log_text, voice_indicator