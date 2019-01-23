import ctypes
import multiprocessing
import queue
import tkinter    as     tk
import tkinter.scrolledtext
from   lib.worker import Process

class MainWindow(object):
    def __init__(self):
        self.process = None
        self.queue   = multiprocessing.Queue(100)
        self.root = tk.Tk()

        # text
        tk.Label(self.root, text='Enter message:').pack()
        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack()

        # time
        tk.Label(self.root, text='Enter time (s)').pack()
        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack()

        # button
        self.button = tk.Button(self.root, text='start', command=self.start)
        self.button.pack()

        # text
        self.display_text = tk.scrolledtext.ScrolledText(self.root, height=20)
        self.display_text.pack()

        # End process on exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_deleted)

        self.root.after_idle(self.process_queue)

    def __delete__(self):
        self.stop()
        self.process = None

    def get_message(self):
        return self.message_entry.get()
    def set_message(self, value):
        self.message_entry.delete('0.0', tk.END)
        self.message_entry.insert('0.0', value)
        self.root.update()
    message = property(get_message, set_message)

    def get_display(self):
        return self.display_text.get('0.0', tk.END)
    def set_display(self, value):
        self.display_text.delete('0.0', tk.END)
        self.display_text.insert('0.0', value)
        self.root.update()
    display = property(get_display, set_display)

    def get_time_s(self):
        return float(self.time_entry.get())
    def set_time_s(self, value):
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, f'{value}')
        self.root.update()
    time_s = property(get_time_s, set_time_s)

    def mainloop(self, *args):
        return self.root.mainloop(*args)

    def start(self, *args):
        self.stop()
        self.display = ''
        self.process = Process(self.queue)
        self.process.start(self.message, self.time_s)
    def stop(self):
        if not self.process:
            return
        self.process.stop()
    def process_queue(self):
        # process queue asynchronously
        # when gui is idle
        try:
            while True:
                line = self.queue.get_nowait()
                self.display += line
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue) # 100 ms
    def on_window_deleted(self):
        self.stop()
        self.root.destroy()
