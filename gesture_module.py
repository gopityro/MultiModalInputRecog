import threading
import cv2
import pyautogui
import mediapipe as mp
from PIL import Image, ImageTk

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

cap = None
video_thread = None

def video_stream(output_label, log_text, gesture_active_flag):
    global cap
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while gesture_active_flag[0]:
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
                    distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
                    if distance < 0.04:
                        pyautogui.click()
                        click_detected = True
                    fx = int(index_tip.x * frame.shape[1])
                    fy = int(index_tip.y * frame.shape[0])
                    cv2.circle(frame, (fx, fy), 10, (0, 255, 0), -1)
            if click_detected:
                cv2.putText(frame, "Click Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                log_text.insert("end", "Click Detected!\n")
                log_text.see("end")
            frame = cv2.resize(frame, (output_label.winfo_width(), output_label.winfo_height()))
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
            output_label.imgtk = imgtk
            output_label.configure(image=imgtk)
        cap.release()
        output_label.config(image='')

gesture_active_flag = [False]

def start_video_thread(output_label, log_text):
    global video_thread
    gesture_active_flag[0] = True
    video_thread = threading.Thread(target=video_stream, args=(output_label, log_text, gesture_active_flag), daemon=True)
    video_thread.start()

def stop_video_thread():
    gesture_active_flag[0] = False