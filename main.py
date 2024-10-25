import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageAnimatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Аниматор красок")

        self.image_path = None
        self.image = None
        self.frames = []
        self.animation_running = False
        self.current_frame = 0
        self.canvas_image = None

        self.btn_select_image = tk.Button(root, text="Выбрать изображение", command=self.select_image)
        self.lbl_image_size = tk.Label(root, text="Размер изображения:")
        self.lbl_image_size_value = tk.Label(root, text="0x0")
        self.lbl_frame_size = tk.Label(root, text="Размер кадра:")
        self.entry_frame_size = tk.Entry(root)
        self.lbl_frame_count = tk.Label(root, text="Количество кадров:")
        self.entry_frame_count = tk.Entry(root)
        self.lbl_fps = tk.Label(root, text="ФПС:")
        self.entry_fps = tk.Entry(root)
        self.btn_animate = tk.Button(root, text="Старт", command=self.start_animation)
        self.btn_stop_animate = tk.Button(root, text="Стоп", command=self.stop_animation)

        self.btn_select_image.grid(row=0, column=0, sticky="w", padx=10)
        self.lbl_image_size.grid(row=1, column=0, sticky="w", padx=10)
        self.lbl_image_size_value.grid(row=2, column=0, sticky="w", padx=10)
        self.lbl_frame_size.grid(row=3, column=0, sticky="w", padx=10)
        self.entry_frame_size.grid(row=4, column=0, sticky="w", padx=10)
        self.lbl_frame_count.grid(row=5, column=0, sticky="w", padx=10)
        self.entry_frame_count.grid(row=6, column=0, sticky="w", padx=10)
        self.lbl_fps.grid(row=7, column=0, sticky="w", padx=10)
        self.entry_fps.grid(row=8, column=0, sticky="w", padx=10)
        self.btn_animate.grid(row=9, column=0, sticky="w", padx=10)
        self.btn_stop_animate.grid(row=10, column=0, sticky="w", padx=10)

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.grid(row=0, column=1, rowspan=11)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.webp")])
        if file_path:
            try:
                img = Image.open(file_path)
                if img.width != img.height:
                    messagebox.showerror("Ошибка", f"Картинка должна быть квадратной.\nРазмер: {img.width}x{img.height}")
                    return
                self.image_path = file_path
                self.image = img
                self.lbl_image_size_value.config(text=f"{img.width}x{img.height}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def validate_inputs(self):
        try:
            frame_size = int(self.entry_frame_size.get())
            if frame_size < 1 or self.image.width % frame_size != 0:
                raise ValueError("Размер изображения должен быть кратным размеру кадра")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверный размер кадра: {e}")
            return None

        try:
            frame_size = int(self.entry_frame_size.get())
            frame_count = int(self.entry_frame_count.get())
            if frame_count < 1:
                raise ValueError("Кадров должно минимум 1")
            if frame_count > (self.image.width // frame_size) ** 2:
                raise ValueError("Количество кадров превышает возможное для данного изображения")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверное количество кадров: {e}")
            return None

        try:
            fps = int(self.entry_fps.get())
            if fps < 1:
                raise ValueError("ФПС должен быть минимум 1")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверный ФПС: {e}")
            return None

        return frame_count, frame_size, fps

    def start_animation(self):
        if self.animation_running:
            return

        if not self.image:
            messagebox.showerror("Ошибка", "Сначала выберите изображение")
            return

        result = self.validate_inputs()
        if result:
            frame_count, frame_size, fps = result
            self.prepare_frames(frame_size, frame_count)
            self.animate(fps)

    def prepare_frames(self, frame_size, frame_count):
        self.frames = []
        num_frames_per_row = self.image.width // frame_size
        total_frames = min(frame_count, num_frames_per_row * num_frames_per_row)

        for i in range(total_frames):
            x = (i % num_frames_per_row) * frame_size
            y = (i // num_frames_per_row) * frame_size
            frame = self.image.crop((x, y, x + frame_size, y + frame_size))
            self.frames.append(ImageTk.PhotoImage(frame))

    def animate(self, fps):
        self.animation_running = True
        frame_interval = 1000 // fps
        self.current_frame = 0
        self.display_next_frame(frame_interval)

    def display_next_frame(self, frame_interval):
        if not self.animation_running or not self.frames:
            return
        self.canvas.delete("all")
        self.canvas_image = self.canvas.create_image(200, 200, image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(frame_interval, lambda: self.display_next_frame(frame_interval))

    def stop_animation(self):
        if not self.animation_running:
            return
        self.animation_running = False
        self.canvas.delete("all")


root = tk.Tk()
app = ImageAnimatorApp(root)
root.mainloop()
