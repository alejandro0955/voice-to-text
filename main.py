import customtkinter as ctk
import tkinter as tk
import speech_recognition as sr
from threading import *
import pyglet
pyglet.options['win32_gdi_font'] = True

recording = False
font = 'Arial'
pyglet.font.add_file('asl.ttf')



def live_transcribe():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Live transcription started. Press 'q' to stop recording.")
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        
        while True:
            if recording == False:  # Stop recording when 'q' is pressed
                break
            
            try:
                audio = recognizer.listen(source, timeout=None)
                text = recognizer.recognize_google(audio)
                asl_output.insert(tk.END, text)
                eng_output.insert(tk.END, text)
                print(f"📝 {text}")
            
            except sr.UnknownValueError:
                pass

def threading():
    thread1 = Thread(target=live_transcribe)
    thread1.start()

def button_click():
    global recording
    if recording == True:
        button.configure(text="Start Recording")
        recording = False
    else:
        recording = True
        threading()
        button.configure(text="Stop Recording")

    #logic to respond to checkboxes accordingly
    #winfo_ismapped checks if the textboxes are already drawn, I do that to make sure they're there when I call destroy()
    if asl_state.get() == "on" and eng_state.get() == "on":
        print("Both buttons")
        asl_output.pack(pady=10)
        eng_output.pack(pady=10)
    elif asl_state.get() == "on" and eng_state.get() == "off":
        print("Asl button")
        asl_output.pack(pady=10)
        eng_output.pack_forget()
    elif eng_state.get() == "on" and asl_state.get()=="off":
        print("Eng button")
        eng_output.pack(pady=10)
        asl_output.pack_forget()
    elif eng_state.get() == "off" and asl_state.get()=="off":
        print("No button")
        eng_output.pack_forget()
        asl_output.pack_forget()


root = ctk.CTk()
root.iconbitmap('icon.ico')
root.title("")
root.minsize(300,300)


#"Voice to text" label
label = ctk.CTkLabel(root, text="Voice to text", font=('Arial',25))
label.pack(pady=20)

#ASL Textbox
asl_output = ctk.CTkTextbox(root, height=100, font=("Gallaudet", 48))
#English textbox
eng_output = ctk.CTkTextbox(root, height=100, font=("Arial", 14))

#Sign language checkbox
asl_state= ctk.StringVar(value="on")
asl_box= ctk.CTkCheckBox(root, text="American Sign Language", variable=asl_state, onvalue="on", offvalue="off")
asl_box.pack(pady=10, padx=20)

#English checkbox
eng_state = ctk.StringVar(value="on")
eng_box = ctk.CTkCheckBox(root, text="English", variable=eng_state, onvalue="on", offvalue="off")
eng_box.pack(pady=10, padx=20)

#"Start recording" button
button = ctk.CTkButton(root, text="Start Recording", command=button_click, font=('Arial',14))
button.pack(pady=10)

root.mainloop()
