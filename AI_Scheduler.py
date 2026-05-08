import customtkinter as ctk
from tkinter import messagebox
import time
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SmartSchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Smart Scheduler")
        self.geometry("1000x800")

        self.is_timer_running = False
        self.mode = "STUDY"  
        self.study_remaining = 0
        self.total_entertainment_seconds = 0
        self.task_list = []
        self.sec_per_task = 0

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=300)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.setup_sidebar()

        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.setup_main_view()

    def setup_sidebar(self):
        ctk.CTkLabel(self.sidebar_frame, text="Smart Coach", font=("Segoe UI", 24, "bold")).pack(pady=20)
        
        ctk.CTkLabel(self.sidebar_frame, text="Total Daily Hours:").pack(anchor="w", padx=25)
        self.hours_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="مثلاً 8")
        self.hours_entry.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.sidebar_frame, text="Tasks (Separate by comma):").pack(anchor="w", padx=25)
        self.tasks_entry = ctk.CTkTextbox(self.sidebar_frame, height=100)
        self.tasks_entry.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.sidebar_frame, text="Task Difficulty:").pack(anchor="w", padx=25, pady=(15,0))
        self.difficulty_slider = ctk.CTkSlider(self.sidebar_frame, from_=1, to=3, number_of_steps=2)
        self.difficulty_slider.set(2)
        self.difficulty_slider.pack(fill="x", padx=20, pady=5)
        
        label_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        label_frame.pack(fill="x", padx=20)
        ctk.CTkLabel(label_frame, text="Easy (Relax)", font=("Segoe UI", 10), text_color="#55aaff").pack(side="left")
        ctk.CTkLabel(label_frame, text="Hard (Focus)", font=("Segoe UI", 10), text_color="#ff5555").pack(side="right")
        
        self.gen_btn = ctk.CTkButton(self.sidebar_frame, text="Build My Day 🚀", font=("Segoe UI", 14, "bold"), 
                                     command=self.generate_schedule)
        self.gen_btn.pack(fill="x", padx=20, pady=30)

    def setup_main_view(self):
        self.schedule_display = ctk.CTkTextbox(self.main_frame, font=("Segoe UI", 15))
        self.schedule_display.pack(fill="both", expand=True, padx=20, pady=20)

        self.entertainment_lbl = ctk.CTkLabel(self.main_frame, text="🎮 Gaming Vault: 00:00:00", 
                                              font=("Segoe UI", 22, "bold"), text_color="#FFB000")
        self.entertainment_lbl.pack(pady=5)

        self.timer_label = ctk.CTkLabel(self.main_frame, text="00:00:00", font=("Segoe UI", 85, "bold"))
        self.timer_label.pack(pady=10)

        self.mode_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.mode_frame.pack(pady=10)

        self.study_mode_btn = ctk.CTkButton(self.mode_frame, text="Study Mode 📖", width=180, height=50, 
                                             fg_color="#1f538d", font=("Segoe UI", 13, "bold"), command=self.switch_to_study)
        self.study_mode_btn.grid(row=0, column=0, padx=10)

        self.game_mode_btn = ctk.CTkButton(self.mode_frame, text="Gaming Mode 🕹️", width=180, height=50, 
                                            fg_color="#8e44ad", font=("Segoe UI", 13, "bold"), command=self.switch_to_gaming)
        self.game_mode_btn.grid(row=0, column=1, padx=10)

        self.ctrl_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.ctrl_frame.pack(pady=15)

        self.timer_btn = ctk.CTkButton(self.ctrl_frame, text="Start", width=140, height=45, command=self.toggle_timer)
        self.timer_btn.grid(row=0, column=0, padx=10)

        self.done_btn = ctk.CTkButton(self.ctrl_frame, text="Task Done! ✅", fg_color="#28a745", hover_color="#218838",
                                       width=140, height=45, font=("Segoe UI", 13, "bold"), command=self.manual_finish)
        self.done_btn.grid(row=0, column=1, padx=10)

    def generate_schedule(self):
        try:
            hours = float(self.hours_entry.get())
            self.task_list = [t.strip() for t in self.tasks_entry.get("1.0", "end-1c").split(',') if t.strip()]
            if not self.task_list: raise ValueError("دخل المهام!")

            diff_factor = self.difficulty_slider.get() 
            study_ratio = 0.6 + (diff_factor * 0.1) 
            
            total_study_sec = hours * 3600 * study_ratio
            self.total_entertainment_seconds = (hours * 3600) - total_study_sec
            self.sec_per_task = total_study_sec / len(self.task_list)

            self.study_remaining = int(self.sec_per_task)
            self.mode = "STUDY"
            self.update_ui_state()
            messagebox.showinfo("تم بناء الجدول", "تم توزيع المهام بنجاح! بالتوفيق في يومك.")
        except:
            messagebox.showerror("خطأ", "اتأكد من كتابة الساعات والمهام بشكل صحيح.")

    def switch_to_study(self):
        self.is_timer_running = False
        self.mode = "STUDY"
        self.update_ui_state()
        messagebox.showinfo("وضع التركيز", "تم التحويل لوضع المذاكرة.")

    def switch_to_gaming(self):
        if self.total_entertainment_seconds <= 0:
            messagebox.showwarning("الخزنة فاضية", "لا يوجد رصيد لعب حالياً، أنجز مهمة لشحن الخزنة!")
            return
        self.is_timer_running = False
        self.mode = "GAMING"
        self.update_ui_state()
        messagebox.showinfo("وقت الراحة", "تم التحويل لوضع اللعب. استمتع برصيدك!")

    def update_ui_state(self):
        color = "#1f538d" if self.mode == "STUDY" else "#8e44ad"
        self.timer_btn.configure(text="Start", fg_color=color)
        
        if self.mode == "STUDY":
            self.remaining_seconds = self.study_remaining
            self.timer_label.configure(text_color="white")
        else:
            self.remaining_seconds = int(self.total_entertainment_seconds)
            self.timer_label.configure(text_color="#FFB000")
        
        self.update_timer_label()
        self.update_entertainment_ui()
        self.refresh_schedule_display()

    def toggle_timer(self):
        if not self.is_timer_running:
            if self.remaining_seconds > 0:
                self.is_timer_running = True
                self.timer_btn.configure(text="Pause", fg_color="#c0392b")
                threading.Thread(target=self.run_timer, daemon=True).start()
        else:
            self.is_timer_running = False
            self.update_ui_state()

    def run_timer(self):
        while self.is_timer_running and self.remaining_seconds > 0:
            time.sleep(1)
            self.remaining_seconds -= 1
            
            if self.mode == "STUDY":
                self.study_remaining = self.remaining_seconds
            else:
                self.total_entertainment_seconds = self.remaining_seconds
                self.after(0, self.update_entertainment_ui)
            
            self.after(0, self.update_timer_label)

        if self.remaining_seconds <= 0 and self.is_timer_running:
            self.is_timer_running = False
            if self.mode == "GAMING":
                self.after(0, lambda: messagebox.showinfo("انتهى الوقت", "رصيد اللعب خلص، حان وقت العودة للمذاكرة!"))
                self.after(0, self.switch_to_study)
            else:
                self.after(0, lambda: messagebox.showinfo("انتهى وقت المهمة", "انتهى الوقت المخصص للمهمة حالياً."))

    def manual_finish(self):
        if self.mode == "STUDY" and self.study_remaining > 0:
            bonus = self.study_remaining
            self.total_entertainment_seconds += bonus
            
            current_task = self.task_list[0] if self.task_list else "المهمة"
            if self.task_list: self.task_list.pop(0)
            
            self.is_timer_running = False
            
            messagebox.showinfo("أحسنت! ✅", 
                                f"تم إنهاء '{current_task}' بنجاح..\n"
                                f"تم إضافة {bonus/60:.1f} دقيقة إضافية لخزنة الجيمنج! 🎮")
            
            if not self.task_list:
                self.study_remaining = 0
                messagebox.showinfo("مبروك", "تم الانتهاء من جميع مهام اليوم!")
            else:
                self.study_remaining = int(self.sec_per_task)
            
            self.update_ui_state()
        else:
            messagebox.showwarning("تنبيه", "هذا الزر مخصص لإنهاء مهام المذاكرة فقط.")

    def update_timer_label(self):
        h, m, s = self.convert_seconds(self.remaining_seconds)
        self.timer_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")

    def update_entertainment_ui(self):
        h, m, s = self.convert_seconds(self.total_entertainment_seconds)
        self.entertainment_lbl.configure(text=f"🎮 Gaming Vault: {h:02d}:{m:02d}:{s:02d}")

    def convert_seconds(self, seconds):
        seconds = max(0, int(seconds))
        mins, secs = divmod(seconds, 60)
        hrs, mins = divmod(mins, 60)
        return hrs, mins, secs

    def refresh_schedule_display(self):
        self.schedule_display.delete("1.0", "end")
        self.schedule_display.insert("end", "📋 REMAINING TASKS:\n\n")
        for t in self.task_list: self.schedule_display.insert("end", f"📍 {t}\n")

if __name__ == "__main__":
    app = SmartSchedulerApp()
    app.mainloop()