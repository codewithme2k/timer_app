import tkinter as tk
from datetime import datetime, timedelta

class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        "Display text in tooltip window"
        self.x = event.x + self.widget.winfo_rootx() + 20
        self.y = event.y + self.widget.winfo_rooty() + 20
        
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (self.x, self.y))
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffff", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Đồng Hồ Đếm Thời Gian")
        self.root.configure(bg='black')
        
        self.is_fullscreen = False
        self.timer_running = False
        self.timer_paused = False
        self.remaining_time = None
        self.font_config = ('Helvetica', 190, 'bold')
        
        self.initialize_ui()

    def initialize_ui(self):
        self.root.bind("<F11>", self.toggle_fullscreen)
        
        self.timer_label = tk.Label(self.root, text="", font=self.font_config, fg='white', bg='black')
        self.timer_label.pack(expand=True)
        
        self.hour_entry = tk.Entry(self.root, width=5, fg='white', bg='black', insertbackground='white')
        self.minute_entry = tk.Entry(self.root, width=5, fg='white', bg='black', insertbackground='white')
        self.hour_entry.pack(side=tk.LEFT)
        self.minute_entry.pack(side=tk.LEFT)
        
        countdown_button = tk.Button(self.root, text="⏺", command=self.start_countdown, fg='white', bg='black')
        countdown_button.pack(side=tk.LEFT)
        ToolTip(countdown_button, "Start the countdown")

        self.pause_button = tk.Button(self.root, text="⏸", command=self.pause_countdown, fg='white', bg='black')
        self.pause_button.pack(side=tk.LEFT)
        ToolTip(self.pause_button, "Pause/Resume the countdown")
        
        real_time_button = tk.Button(self.root, text="⇆", command=self.start_real_time, fg='white', bg='black')
        real_time_button.pack(side=tk.RIGHT)
        ToolTip(real_time_button, "Display real time")

        
    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen  # Đảo ngược trạng thái
        self.root.attributes("-fullscreen", self.is_fullscreen)  # Cập nhật thuộc tính toàn màn hình của cửa sổ

    # Các phương thức khác giữ nguyên như trước đây
    def start_real_time(self):
        self.reset_timer()
        self.update_time()

    def reset_timer(self):
        if self.timer_running:
            self.timer_label.after_cancel(self.timer_running)
        self.timer_paused = False
        self.pause_button.config(text="⏸")

    def update_time(self):
        now = datetime.now()
        self.timer_label.config(text=now.strftime('%H:%M:%S'))
        self.timer_running = self.timer_label.after(1000, self.update_time)

    def start_countdown(self):
        if self.timer_paused:
            return
        hours = int(self.hour_entry.get()) if self.hour_entry.get() else 0
        minutes = int(self.minute_entry.get()) if self.minute_entry.get() else 0
        self.end_time = datetime.now() + timedelta(hours=hours, minutes=minutes)
        self.reset_timer()
        self.update_countdown()

    def update_countdown(self):
        if self.timer_paused:
            return
        remaining = self.end_time - datetime.now()
        if remaining.total_seconds() > 0:
            self.timer_label.config(text=str(remaining).split('.')[0])
            self.timer_running = self.timer_label.after(1000, self.update_countdown)
        else:
            self.timer_label.config(text="0:00:00")
            self.timer_running = False

    def pause_countdown(self):
        if self.timer_paused:
            self.pause_button.config(text="⏸ ")
            self.timer_paused = False
            self.end_time = datetime.now() + self.remaining_time
            self.update_countdown()
        else:
            self.pause_button.config(text="▶")
            self.timer_paused = True
            if self.timer_running:
                self.timer_label.after_cancel(self.timer_running)
            remaining = self.end_time - datetime.now()
            self.remaining_time = remaining

root = tk.Tk()
app = TimerApp(root)
root.mainloop()
