import tkinter as tk
import cv2
from PIL import Image, ImageTk
import easyocr
import numpy as np
import json

class ImageAnnotator:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Image Annotator")
        
        # Load the image
        self.load_image(image_path)
        
        # Create a canvas to display the image
        self.canvas = tk.Canvas(root, width=self.image_pil.width, height=self.image_pil.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        
        # Bind mouse events to the canvas
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        # Initialize variables
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.keys_texts = {}
    
    def load_image(self, image_path):
        self.image = cv2.imread(image_path)
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image_pil = Image.fromarray(self.image_rgb)
        self.image_tk = ImageTk.PhotoImage(self.image_pil)
    
    def on_button_press(self, event):
        # Save the starting point
        self.start_x = event.x
        self.start_y = event.y
        # Create a rectangle
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")
    
    def on_mouse_drag(self, event):
        # Update the rectangle as the mouse is dragged
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
    
    def on_button_release(self, event):
        # Finalize the rectangle and prompt for a key
        end_x, end_y = event.x, event.y
        self.show_form(self.start_x, self.start_y, end_x, end_y)
    
    def show_form(self, x1, y1, x2, y2):
        form = tk.Toplevel(self.root)
        form.title("Enter Key for Selected Area")
        
        tk.Label(form, text="Key:").grid(row=0, column=0)
        key_entry = tk.Entry(form)
        key_entry.grid(row=0, column=1)
        
        def submit():
            key = key_entry.get()
            if key:
                self.keys_texts[key] = (x1, y1, x2, y2)
            form.destroy()
        
        tk.Button(form, text="Submit", command=submit).grid(row=1, columnspan=2)
    
    def get_annotations(self):
        return self.keys_texts
    
    def extract_texts(self):
        reader = easyocr.Reader(['en'])
        texts = {}
        for key, (x1, y1, x2, y2) in self.keys_texts.items():
            # Convert PIL image to NumPy array
            image_array = np.array(self.image_pil)
            # Crop the image to the specified area
            cropped_image = image_array[y1:y2, x1:x2]
            # Perform OCR on the cropped area
            results = reader.readtext(cropped_image)
            # Extract text from the OCR results
            extracted_text = ' '.join([text for (_, text, _) in results])
            texts[key] = extracted_text
        return texts
    
    def save_texts_to_json(self, texts, filename):
        with open(filename, 'w') as json_file:
            json.dump(texts, json_file, indent=4)
    
    def save_form_data(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.keys_texts, json_file, indent=4)
    
    def load_form_data(self, filename):
        with open(filename, 'r') as json_file:
            self.keys_texts = json.load(json_file)