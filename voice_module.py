import threading
import time

voice_active_flag = [False]
voice_thread = None

import speech_recognition as sr

def dummy_voice_recognition(log_text, voice_indicator):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        voice_indicator.config(text="Voice Status: Listening...", bg="#28a745")
        log_text.insert("end", "[Voice] Adjusted for ambient noise\n")
        log_text.see("end")

    while voice_active_flag[0]:
        try:
            with mic as source:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                log_text.insert("end", f"[Voice] Recognized: {command}\n")
                log_text.see("end")
        except sr.WaitTimeoutError:
            log_text.insert("end", "[Voice] Listening timeout...\n")
            log_text.see("end")
        except sr.UnknownValueError:
            log_text.insert("end", "[Voice] Could not understand audio.\n")
            log_text.see("end")
        except Exception as e:
            log_text.insert("end", f"[Voice] Error: {str(e)}\n")
            log_text.see("end")

    voice_indicator.config(text="Voice Status: Inactive", bg="#cccccc")

def start_voice_thread(log_text, voice_indicator):
    global voice_thread
    voice_active_flag[0] = True
    voice_thread = threading.Thread(target=dummy_voice_recognition, args=(log_text, voice_indicator), daemon=True)
    voice_thread.start()

def stop_voice_thread():
    voice_active_flag[0] = False