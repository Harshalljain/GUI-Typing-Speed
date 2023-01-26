import tkinter as tk  # GUI module
import time
import threading  # We don't want same thread to manage time n GUi to avoid lagging
import random  # So text randomly


class TypeSpeedGUI:

    def __init__(self):
        self.root = tk.Tk()  # self.root as parent object
        self.root.title("Typing speed Application")
        self.root.geometry("800x600")

        self.texts = open("text.txt", "r").read().split("\n")
        self.frame = tk.Frame(self.root)  # For the frame

        self.sample_label = tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 18))  # label for the txt that is selected
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24))  # input entry
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        # To trigger the start of the timer when the input entry is passed
        self.input_entry.bind("<KeyRelease>", self.start)

        self.speed_label = tk.Label(self.frame, text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM", font=("Helvetica", 18))  # Will show Character per speed n character per minute
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)  # We make the frame larger by doing that

        self.counter = 0  # For counting hashable object
        self.running = False  # Boolean

        self.root.mainloop()

    def start(self, event):  # When we bind keydown , self.start it will start an event i.e which key was pressed
        if not self.running:
            if not event.keycode in [16, 17, 18]:  # key codes for specific keys
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()

        if not self.sample_label.cget("text").startswith(self.input_entry.get()):
            self.input_entry.config(fg = "red")
        else:
            self.input_entry.config(fg = "black")

        if self.input_entry.get() == self.sample_label.cget('text'):
            self.running = False
            self.input_entry.config(fg = "green")

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get().split(" ")) / self.counter 
            wpm = wps * 60
            self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM\n{wps:.2f} WPS\n{wpm:.2f} WPM")

    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM")
        self.sample_label.config(text=random.choice(self.texts))
        self.input_entry.delete(0, tk.END)


TypeSpeedGUI()
