import os
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk
import cv2

class Photoshop:
    def __init__(self):
        self.img = None
        self.original_img = None
        self.normalised_img = None
        self.new_img_PIL = None
        self.photo = None
        self.canvas = None
        self.slider_strength = None
        self.strength_value = 50
        self.path = None

        self.UI()

    def UI(self):
        # Display
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.geometry("800x800")
        self.root.title("Photoshop")

        self.pathFrame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.pathFrame.pack(pady=(30, 5))

        self.open_image()

        self.canvas = ctk.CTkCanvas(self.root, width=600, height=400)
        self.canvas.pack(pady=(30, 10))

        self.reset_to_original()

        self.buttonFrame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.buttonFrame.pack(side="bottom", pady=(10, 50))

        self.sliderFrame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.sliderFrame.pack(side="bottom", pady=(10, 10))

        self.create_slider()
        self.create_button()

        self.root.mainloop()

    # Getting the image path
    def open_image(self):
        def load_image():
            path = image_path.get().strip()
            if os.path.exists(path):
                self.img = Image.open(path).convert("RGB")
                status_label.configure(text="Path found!", text_color="green")

                # Store the original image
                self.original_img = np.array(self.img)
                self.normalised_img = self.original_img.astype(np.float32) / 255.0

                # Resize for display
                self.resize_for_display()

            else:
                status_label.configure(text="Path NOT found!", text_color="red")

        image_path = ctk.CTkEntry(self.pathFrame, width=200, placeholder_text="Enter image path...")
        image_path.pack(pady=5)

        status_label = ctk.CTkLabel(self.pathFrame, text="", text_color="white")
        status_label.pack(pady=5)
        
        button = ctk.CTkButton(self.pathFrame, text="Get Image Path", command=load_image)
        button.pack(pady=10)

    # Resize the image for display on the canvas
    def resize_for_display(self):
        if self.img is not None:
            width, height = self.img.size
            aspect_ratio = width / height
            new_width = 600
            new_height = int(new_width / aspect_ratio)

            # Resize for display
            self.new_img_PIL = self.img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.new_img_PIL)
            self.canvas.config(width=new_width, height=new_height)
            self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
            self.canvas.image = self.photo

    @staticmethod
    def convolution_matrix(image, kernel):
        return cv2.filter2D(image, -1, kernel)

    # Kernels
    @staticmethod
    def sharpen(strength):
        kernel_sharpen = np.array([
            [  0, -1,  0],
            [ -1,  5, -1],
            [  0, -1,  0]
        ], dtype=np.float32)
        return  kernel_sharpen * strength

    def blur(self, strength):
        kernel_blur = np.array([
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9]
        ], dtype=np.float32)
        self.multi_blurs(strength, kernel_blur)
        return kernel_blur

    def motionblur(self, strength):
        kernel_motionblur = np.zeros((5, 5), dtype=np.float32)
        kernel_motionblur[2, :] = 1 / 5
        self.multi_blurs(strength, kernel_motionblur)
        return kernel_motionblur

    def multi_blurs(self, strength, kernel):
        if self.normalised_img is not None:
            for _ in range(strength-1):
                image = self.normalised_img
                result = self.convolution_matrix(image, kernel)
                self.normalised_img = result

    @staticmethod
    def edge_detection(strength):
        kernel_edge_detection = np.array([
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ], dtype=np.float32)
        return kernel_edge_detection * strength

    # Updating image
    def update_image(self, kernel):
        if self.normalised_img is not None:
            # Apply filter to the original-sized image
            result = self.convolution_matrix(self.normalised_img, kernel)
            self.normalised_img = result
            output_img = np.clip(result * 255, 0, 255).astype(np.uint8)
            self.img = Image.fromarray(output_img)  # Update self.img with the filtered image

            # Resize for display
            self.resize_for_display()

    # Applying kernels to image
    def apply_filter(self, kernel_function):
        strength = max(int(self.strength_slider.get()/5), 5)  
        kernel = kernel_function(strength)
        self.update_image(kernel)

    # Resetting to initial image
    def reset_to_original(self):
        if self.original_img is not None:
            self.normalised_img = self.original_img.astype(np.float32) / 255.0
            self.img = Image.fromarray(self.original_img)  # Reset self.img to the original image
            self.resize_for_display()

    # Saving current version of image
    def save_image(self):
        save_window = ctk.CTkToplevel(self.root)
        save_window.geometry("300x200")
        save_window.title("Save Image")

        label = ctk.CTkLabel(save_window, text="Enter image name:")
        label.pack(pady=10)

        path_name_entry = ctk.CTkEntry(save_window, width=200)
        path_name_entry.pack(pady=5)

        status_label = ctk.CTkLabel(save_window, text="", text_color="white")
        status_label.pack(pady=5)

        def check_image_name():
            path_name = path_name_entry.get().strip()
            if not path_name:
                status_label.configure(text="Enter a valid name!", text_color="red")
                return
            
            self.path = f"Photoshop/{path_name}.jpg"

            if not os.path.exists("Photoshop"):  
                os.makedirs("Photoshop")  

            if os.path.exists(self.path):
                status_label.configure(text="Image already exists!", text_color="red")
            else:
                # Save the original-sized filtered image
                self.img.save(self.path)
                status_label.configure(text="Image saved!", text_color="green")

        save_button = ctk.CTkButton(save_window, text="Save", command=check_image_name)
        save_button.pack(pady=10)

    # Creating necessary buttons
    def create_button(self):
        sharpen_button = ctk.CTkButton(self.buttonFrame, text="Sharpen", command=lambda: self.apply_filter(self.sharpen))
        blur_button = ctk.CTkButton(self.buttonFrame, text="Blur", command=lambda: self.apply_filter(self.blur))
        edge_detection_button = ctk.CTkButton(self.buttonFrame, text="Edge Detection", command=lambda: self.apply_filter(self.edge_detection))
        motionblur_button = ctk.CTkButton(self.buttonFrame, text="Motion Blur", command=lambda: self.apply_filter(self.motionblur))
        reset_button = ctk.CTkButton(self.buttonFrame, text="Reset", command=self.reset_to_original)
        save_button = ctk.CTkButton(self.buttonFrame, text="Save", command=self.save_image)

        sharpen_button.grid(row=0, column=0, padx=5, pady=5)
        blur_button.grid(row=0, column=1, padx=5, pady=5)
        edge_detection_button.grid(row=0, column=2, padx=5, pady=5)
        motionblur_button.grid(row=1, column=0, padx=5, pady=5)
        reset_button.grid(row=1, column=1, padx=5, pady=5)
        save_button.grid(row=1, column=2, padx=5, pady=5)

    # Creating slider to control kernels
    def slider_callback(self, value):
        self.strength_value = int(value)
        self.strength_label.configure(text=f"Strength = {self.strength_value}")

    def create_slider(self):
        self.strength_slider = ctk.CTkSlider(self.sliderFrame, from_=1, to=100, command=self.slider_callback)
        self.strength_slider.pack()

        self.strength_label = ctk.CTkLabel(self.sliderFrame, text=f"Strength = {self.strength_value}")
        self.strength_label.pack()

if __name__ == "__main__":
    Photoshop()