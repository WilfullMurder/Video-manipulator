import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from moviepy.video.io.VideoFileClip import VideoFileClip

class VideoProcessor:
    def convert_video(self, input_path, output_path, output_format):
        if input_path.contains(output_format):
            print("Input and output formats are the same. No conversion needed.")
            return
        clip = VideoFileClip(input_path)
        clip.write_videofile(f"{output_path}.{output_format}", codec='libx264')

    def compress_video(self, input_path, output_path, target_size_percentage):
        clip = VideoFileClip(input_path)
        if target_size_percentage == 100:
            clip.write_videofile(f"{output_path}.mp4", codec='libx264')
        else:
            target_bitrate = clip.reader.bitrate * (target_size_percentage / 100)
            clip.write_videofile(f"{output_path}.mp4", bitrate=f"{target_bitrate}k", codec='libx264')

class FileSelector:
    def __init__(self, listbox):
        self.listbox = listbox

    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
        if file_paths:
            for file_path in file_paths:
                self.listbox.insert(tk.END, file_path)

    def select_directory(self, output_directory_var):
        directory = filedialog.askdirectory()
        if directory:
            output_directory_var.set(directory)

class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Converter and Compressor")
        self.video_processor = VideoProcessor()
        self.output_format_var = tk.StringVar(value="mp4")
        self.compression_percentage_var = tk.StringVar(value="50")
        self.output_directory_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.listbox = tk.Listbox(self.root, width=50, height=10)
        self.listbox.pack(pady=20)

        file_selector = FileSelector(self.listbox)
        select_button = tk.Button(frame, text="Select Videos", command=file_selector.select_files)
        select_button.pack(side=tk.LEFT, padx=10)

        convert_button = tk.Button(frame, text="Convert and Compress", command=self.convert_selected_files)
        convert_button.pack(side=tk.LEFT, padx=10)

        tk.Label(self.root, text="Output Format:").pack()
        tk.Entry(self.root, textvariable=self.output_format_var).pack()

        tk.Label(self.root, text="Compression Percentage:").pack()
        tk.Entry(self.root, textvariable=self.compression_percentage_var).pack()

        tk.Label(self.root, text="Output Directory:").pack()
        tk.Entry(self.root, textvariable=self.output_directory_var).pack()
        tk.Button(self.root, text="Select Directory", command=lambda: file_selector.select_directory(self.output_directory_var)).pack()

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=20)

    def convert_selected_files(self):
        output_format = self.output_format_var.get()
        compression_percentage = int(self.compression_percentage_var.get())
        output_directory = self.output_directory_var.get()
        total_files = self.listbox.size()
        self.progress_bar['maximum'] = total_files
        for i in range(total_files):
            input_path = self.listbox.get(i)
            input_filename = os.path.basename(input_path)
            output_path = os.path.join(output_directory, os.path.splitext(input_filename)[0])
            self.video_processor.compress_video(input_path, output_path, compression_percentage)
            self.progress_bar['value'] = i + 1
            self.root.update_idletasks()
        messagebox.showinfo("Success", "Videos converted and compressed successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()