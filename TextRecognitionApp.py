# ocr_app.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from ImageProcessor import ImageProcessor

class TextRecognitionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Detection App")
        self.geometry("600x400")

        # Initialize Image Processor
        self.processor = ImageProcessor()

        # Adding widgets
        self.create_widgets()

        self.processed_images = []

    def create_widgets(self):
        """Create and place all widgets in the application."""

        # File selection label
        self.file_label = tk.Label(self, text="Files:")
        self.file_label.pack(pady=10)

        # Entry for file paths
        self.file_entry = tk.Entry(self)
        self.file_entry.pack(pady=10)

        # Browse button
        self.browse_button = tk.Button(self, text="Browse", command=self.select_files)
        self.browse_button.pack(pady=10)

        # Process button
        self.process_button = tk.Button(self, text="Process Images", command=self.process_images)
        self.process_button.pack(pady=10)

        # Save button
        self.save_button = tk.Button(self, text="Save Images", command=self.save_images)
        self.save_button.pack(pady=10)

        # Exit button
        self.exit_button = tk.Button(self, text="Exit", command=self.quit_application)
        self.exit_button.pack(pady=10)

    def select_files(self):
        """Allows users to select image files."""
        filetypes = [("Image files", "*.png *.jpg *.jpeg")]
        files = filedialog.askopenfilenames(filetypes=filetypes)

        if files:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, " ".join(files))

    def process_images(self):
        """Processes selected images and displays them."""
        files = self.file_entry.get().split()

        if not files or not any(os.path.isfile(f) for f in files):
            messagebox.showerror("No Files", "Please select valid image files.")
            return

        try:
            self.processed_images = self.processor.process_images(files)
            for i, image in enumerate(self.processed_images):
                cv2.imshow(f"Processed Image {i + 1}", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            messagebox.showinfo("Processing Complete", "Images have been processed.")

        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

    def save_images(self):
        """Saves processed images to a selected directory."""
        if not self.processed_images:
            messagebox.showerror("No Images", "No images have been processed yet.")
            return

        save_dir = filedialog.askdirectory(title="Select save directory")

        if save_dir:
            for i, image in enumerate(self.processed_images):
                filename = f"processed_image_{i + 1}.png"
                cv2.imwrite(os.path.join(save_dir, filename), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Images Saved", f"Images saved to {save_dir}")

    def quit_application(self):
        """Exits the application."""
        self.destroy()
