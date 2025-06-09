import cv2
import pyautogui
import mediapipe as mp
from PIL import Image, ImageTk
import settings

mp_hands = mp.solutions.hands

def process_video(cap, gesture_var, output_label, log_text):
    with mp_hands.Hands(
        min_detection_confidence=settings.MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=settings.MIN_TRACKING_CONFIDENCE
    ) as hands:
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

                    x = int(index_tip.x * settings.SCREEN_WIDTH)
                    y = int(index_tip.y * settings.SCREEN_HEIGHT)
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
                log_text.insert("end", "Click Detected!\n")
                log_text.see("end")

            frame = cv2.resize(frame, (output_label.winfo_width(), output_label.winfo_height()))
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
            output_label.imgtk = imgtk
            output_label.configure(image=imgtk)

            if not gesture_var.get():
                break

    cap.release()
    output_label.config(image='')