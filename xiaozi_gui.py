import tkinter as tk
from PIL import Image, ImageTk
from xiaozi_game import XiaoziGame
from tkinter import PhotoImage
import os
import sys

class XiaoziGUI:
    def __init__(self, root):
        self.game = XiaoziGame()
        self.root = root
        self.root.title("小紫爱抽卡")
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        # Determine the path to the background image
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(__file__)

        background_image_path = os.path.join(application_path, "images", "background.png")

        self.background_image = PhotoImage(file=background_image_path)
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.main_frame = tk.Frame(root, bg='#ffffff', bd=5)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.result_frame = tk.Frame(self.main_frame, bg='#ffffff')
        self.result_frame.pack(pady=20)

        self.result_label = tk.Text(self.main_frame, height=4, font=("Helvetica", 16), bg='#ffffff', bd=0)
        self.result_label.insert(tk.END, "欢迎使用小紫爱抽卡!")
        self.result_label.tag_configure("center", justify='center')
        self.result_label.tag_add("center", 1.0, "end")
        self.result_label.pack(pady=20)
        self.result_label.config(width=50)

        button_style = {
            "font": ("Helvetica", 14),
            "bg": "#f0e68c",
            "fg": "#000000",
            "bd": 0,
            "highlightthickness": 0,
            "relief": "flat",
            "width": 10
        }

        self.draw_button = tk.Button(self.main_frame, text="单抽", command=self.draw_item, **button_style)
        self.draw_button.pack(pady=10)

        self.ten_draws_button = tk.Button(self.main_frame, text="十连", command=self.ten_draws, **button_style)
        self.ten_draws_button.pack(pady=10)

        self.reset_button = tk.Button(self.main_frame, text="重置", command=self.reset_stats, **button_style)
        self.reset_button.pack(pady=10)

        self.view_items_button = tk.Button(self.main_frame, text="图鉴", command=self.view_items, **button_style)
        self.view_items_button.pack(pady=10)

        self.stats_label = tk.Label(self.main_frame, text="", font=("Helvetica", 12), bg='#ffffff')
        self.stats_label.pack(pady=20)

        self.rarity_frame = tk.Frame(root, bg='#ffffff', bd=5)
        self.rarity_frame.place(relx=0.95, rely=0.05, anchor='ne')

        self.rarity_labels = {}
        for rarity in self.game.pool:
            label = tk.Label(self.rarity_frame, text=f"{rarity}: 0", font=("Helvetica", 12), bg='#ffffff')
            label.pack(anchor='e')
            self.rarity_labels[rarity] = label

        self.update_stats()

        self.items_frame = tk.Frame(root, bg='#ffffff', bd=5)

        # 让 main_frame 的宽度自适应内部组件的宽度
        self.main_frame.update_idletasks()  # 更新布局
        self.main_frame.config(width=self.result_label.winfo_width())  # 设置宽度为内部组件的宽度

    def draw_item(self):
        result = self.game.draw()
        self.result_frame.destroy()
        self.result_frame = tk.Frame(self.main_frame, bg='#ffffff')
        self.result_frame.pack(pady=30, before=self.draw_button)  # Place result_frame above buttons

        # Hide the result_label
        self.result_label.pack_forget()

        # 指定目标图片大小
        target_width = 50
        target_height = 50

        image_path = os.path.join("images", "background.png")
        
        # 使用 Pillow 打开并调整图片大小
        original_image = Image.open(image_path)
        resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)  # LANCZOS 高质量缩放
        
        # 转换为 Tkinter 可用的 PhotoImage
        image = ImageTk.PhotoImage(resized_image)
        
        image_label = tk.Label(self.result_frame, image=image, bg='#ffffff')
        image_label.image = image  # 保持引用，防止被垃圾回收
        image_label.pack()

        color = self.get_color(result)
        text_label = tk.Label(self.result_frame, text=result, font=("Helvetica", 10), bg='#ffffff', fg=color)
        text_label.pack()

        self.update_stats()

    def ten_draws(self):
        results = self.game.ten_draws()
        self.result_frame.destroy()
        self.result_frame = tk.Frame(self.main_frame, bg='#ffffff')
        self.result_frame.pack(pady=20, before=self.draw_button)  # Place result_frame above buttons

        row_frame = None
        for index, result in enumerate(results):
            if index % 5 == 0:
                row_frame = tk.Frame(self.result_frame, bg='#ffffff')
                row_frame.pack()

            frame = tk.Frame(row_frame, bg='#ffffff')
            frame.pack(side=tk.LEFT, padx=5)

            # 指定目标图片大小
            target_width = 50
            target_height = 50

            image_path = os.path.join("images", "background.png")
            
            # 使用 Pillow 打开并调整图片大小
            original_image = Image.open(image_path)
            resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)  # LANCZOS 高质量缩放
            
            # 转换为 Tkinter 可用的 PhotoImage
            image = ImageTk.PhotoImage(resized_image)
            
            image_label = tk.Label(frame, image=image, bg='#ffffff')
            image_label.image = image  # 保持引用，防止被垃圾回收
            image_label.pack()

            color = self.get_color(result)
            text_label = tk.Label(frame, text=result, font=("Helvetica", 10), bg='#ffffff', fg=color)
            text_label.pack()

        self.update_stats()

    def get_color(self, result):
        rarity_colors = {
            "普通": "blue",
            "稀有": "green",
            "史诗": "orange",
            "传奇": "red"
        }
        for rarity, brands in self.game.pool.items():
            if result in brands:
                return rarity_colors[rarity]
        return "black"

    def show_stats(self):
        stats = self.game.display_stats()
        stats_text = (
            f"总抽数: {stats['total_draws']}\n"
            f"平均传奇抽数: {stats['average_draws_for_legendary']:.2f}\n"
            f"抽中传奇概率: {stats['legendary_probability']:.2%}\n"
        )
        self.stats_label.config(text=stats_text)

    def update_stats(self):
        stats = self.game.display_stats()
        stats_text = (
            f"总抽数: {stats['total_draws']}\n"
            f"平均传奇抽数: {stats['average_draws_for_legendary']:.2f}\n"
            f"抽中传奇概率: {stats['legendary_probability']:.2%}\n"
        )
        self.stats_label.config(text=stats_text)

        for rarity, count in stats['rarity_counts'].items():
            self.rarity_labels[rarity].config(text=f"{rarity}: {count}")

    def reset_stats(self):
        self.game.reset_stats()
        self.result_frame.destroy()

        self.result_label.pack(pady=20, before=self.draw_button)  # Red, before=self.draw_buttonisplay the result_label
        self.result_label.config(state=tk.NORMAL)
        self.result_label.delete(1.0, tk.END)
        self.result_label.insert(tk.END, "统计数据已重置")
        self.result_label.tag_add("center", 1.0, "end")
        self.result_label.config(state=tk.DISABLED)
        self.update_stats()

    def view_items(self):
        self.main_frame.place_forget()
        self.rarity_frame.place_forget()
        self.items_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.7)

        rarity_colors = {
            "普通": "blue",
            "稀有": "green",
            "史诗": "orange",
            "传奇": "red"
        }

        for widget in self.items_frame.winfo_children():
            widget.destroy()

        for rarity, items in self.game.pool.items():
            rarity_label = tk.Label(self.items_frame, text=rarity, font=("Helvetica", 14, "bold"), bg='#ffffff', pady=10, fg=rarity_colors[rarity])
            rarity_label.pack(fill='x')
            for i in range(0, len(items), 5):
                item_text = "    ".join([f"{item} ({self.game.brand_counts[item]})" for item in items[i:i+5]])
                item_label = tk.Label(self.items_frame, text=item_text, font=("Helvetica", 12), bg='#ffffff', anchor='center', padx=10)
                item_label.pack(fill='x')

        return_button = tk.Button(self.items_frame, text="返回", command=self.show_main_frame, font=("Helvetica", 14), bg="#f0e68c", fg="#000000", bd=0, highlightthickness=0, relief="flat", width=10)
        return_button.pack(pady=20)

        self.items_frame.update_idletasks()

    def show_main_frame(self):
        self.items_frame.place_forget()
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.rarity_frame.place(relx=0.95, rely=0.05, anchor='ne')

if __name__ == "__main__":
    root = tk.Tk()
    app = XiaoziGUI(root)
    root.mainloop()
