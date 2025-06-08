import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
import os

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yazma Testi")
        self.root.geometry("900x600")

        self.language = tk.StringVar(value="turkish")
        self.word_count = tk.IntVar(value=200)

        self.start_time = None
        self.correct_words = 0
        self.incorrect_words = 0
        self.test_active = False
        self.words = []
        self.current_word_index = 0

        self.create_widgets()

    def load_words(self):
        if self.language.get() == "english":
            # Unix sistemler için, Windows'ta manuel dosya kullanılır
            try:
                with open("/usr/share/dict/words", "r") as f:
                    word_list = f.read().splitlines()
            except:
                with open("english_words.txt", "r") as f:
                    word_list = f.read().splitlines()
        else:
            with open("turkish_words.txt", "r", encoding="utf-8") as f:
                word_list = f.read().splitlines()

        self.words = random.sample(word_list, self.word_count.get())

    def create_widgets(self):
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10)

        tk.Label(settings_frame, text="Dil:").pack(side=tk.LEFT)
        tk.OptionMenu(settings_frame, self.language, "turkish", "english").pack(side=tk.LEFT, padx=5)

        tk.Label(settings_frame, text="Kelime Sayısı:").pack(side=tk.LEFT)
        tk.OptionMenu(settings_frame, self.word_count, 200, 1000).pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(settings_frame, text="Başlat", command=self.start_test)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.text_display = tk.Text(self.root, wrap=tk.WORD, height=10, font=("Courier", 14))
        self.text_display.pack(pady=10)
        self.text_display.config(state=tk.DISABLED)

        self.entry = tk.Entry(self.root, font=("Courier", 14), width=50)
        self.entry.pack(pady=10)
        self.entry.bind("<space>", self.check_word)

        self.timer_label = tk.Label(self.root, text="Süre: 60", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack()

    def start_test(self):
        self.load_words()
        self.correct_words = 0
        self.incorrect_words = 0
        self.current_word_index = 0
        self.test_active = True

        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, " ".join(self.words))
        self.text_display.tag_configure("correct", foreground="green")
        self.text_display.tag_configure("incorrect", foreground="red")
        self.text_display.config(state=tk.DISABLED)

        self.entry.delete(0, tk.END)
        self.result_label.config(text="")

        self.start_time = time.time()
        self.update_timer()

    def check_word(self, event):
        if not self.test_active:
            return

        typed = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        correct_word = self.words[self.current_word_index]
        self.text_display.config(state=tk.NORMAL)

        # Kelime başlangıç ve bitiş index'ini bul
        start_index = "1.0"
        for i in range(self.current_word_index):
            word_len = len(self.words[i])
            start_index = self.text_display.search(self.words[i], start_index, stopindex=tk.END)
            start_index = self.text_display.index(f"{start_index}+{word_len + 1}c")

        start = self.text_display.search(correct_word, start_index, stopindex=tk.END)
        end = f"{start}+{len(correct_word)}c"

        if typed == correct_word:
            self.text_display.tag_add("correct", start, end)
            self.correct_words += 1
        else:
            self.text_display.tag_add("incorrect", start, end)
            self.incorrect_words += 1

        self.text_display.config(state=tk.DISABLED)
        self.current_word_index += 1

        if self.current_word_index >= len(self.words):
            self.end_test()

    def update_timer(self):
        if not self.test_active:
            return

        elapsed = int(time.time() - self.start_time)
        remaining = 60 - elapsed
        self.timer_label.config(text=f"Süre: {remaining}")

        if remaining <= 0:
            self.end_test()
        else:
            self.root.after(1000, self.update_timer)

    def end_test(self):
        self.test_active = False
        self.result_label.config(
            text=f"✅ Doğru: {self.correct_words}    ❌ Yanlış: {self.incorrect_words}"
        )

# Uygulama başlat
root = tk.Tk()
app = TypingTestApp(root)
root.mainloop()
