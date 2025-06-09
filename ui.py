import tkinter as tk
from tkinter import ttk
import threading
import cv2
import pyautogui
import mediapipe as mp
from PIL import Image, ImageTk

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Tkinter GUI setup
root = tk.Tk()
root.title("Multimodal Input System")
root.geometry("1100x750")
root.configure(bg="#f0f2f5")

style = ttk.Style()
style.configure("TLabelFrame", font=("Segoe UI", 12, "bold"))
style.configure("TCheckbutton", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11))
style.configure("TLabelframe.Label", foreground="#0b5394")

# Layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=4)
root.rowconfigure(1, weight=1)

# Left Panel
toggle_frame = ttk.LabelFrame(root, text="Enable Inputs")
toggle_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

voice_var = tk.BooleanVar()
gesture_var = tk.BooleanVar()

voice_toggle = ttk.Checkbutton(toggle_frame, text="Enable Voice Input", variable=voice_var)
gesture_toggle = ttk.Checkbutton(toggle_frame, text="Enable Hand Gestures", variable=gesture_var, command=lambda: toggle_video_stream())

voice_toggle.pack(pady=15, padx=20, anchor="w")
gesture_toggle.pack(pady=15, padx=20, anchor="w")

# Right Panel
output_frame = ttk.LabelFrame(root, text="Output Display")
output_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

output_label = tk.Label(output_frame, bg="black")
output_label.pack(expand=True, fill="both", padx=15, pady=15)

# Bottom Panel
log_frame = ttk.LabelFrame(root, text="Logs")
log_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=15, sticky="nsew")

log_text = tk.Text(log_frame, wrap="word", height=6, font=("Consolas", 10), bg="#1e1e1e", fg="#00ff00", insertbackground="white")
log_text.pack(expand=True, fill="both", padx=10, pady=10)

# Globals
cap = None
video_thread = None

# Video stream
def video_stream():
    global cap
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while gesture_var.get():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            click_detected = False

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    index_tip = hand_landmarks.landmark[8]
                    thumb_tip = hand_landmarks.landmark[4]

                    x = int(index_tip.x * screen_width)
                    y = int(index_tip.y * screen_height)
                    pyautogui.moveTo(x, y)

                    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
                    if distance < 0.04:
                        pyautogui.click()
                        click_detected = True

                    fx = int(index_tip.x * frame.shape[1])
                    fy = int(index_tip.y * frame.shape[0])
                    cv2.circle(frame, (fx, fy), 10, (0, 255, 0), -1)

            if click_detected:
                cv2.putText(frame, "Click Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                log_text.insert(tk.END, "Click Detected!\n")
                log_text.see(tk.END)

            frame = cv2.resize(frame, (output_label.winfo_width(), output_label.winfo_height()))
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
            output_label.imgtk = imgtk
            output_label.configure(image=imgtk)

            if not gesture_var.get():
                break

    cap.release()
    cap = None
    output_label.config(image='')

def toggle_video_stream():
    global video_thread
    if gesture_var.get():
        if video_thread is None or not video_thread.is_alive():
            video_thread = threading.Thread(target=video_stream, daemon=True)
            video_thread.start()
    else:
        if cap:
            cap.release()
        output_label.config(image='')

# Run GUI
root.mainloop()