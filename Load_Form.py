import tkinter as tk
from ImageAnnotation import ImageAnnotator

def main():
    # Create the main window
    root = tk.Tk()
    
    # Open file dialog to select an image
    image_path = tk.filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    
    if image_path:
        annotator = ImageAnnotator(root, image_path)
        
        # Load the form data from a JSON file
        form_data_path = tk.filedialog.askopenfilename(title="Select Form Data", filetypes=[("JSON Files", "*.json")])
        if form_data_path:
            annotator.load_form_data(form_data_path)
            print("Form data loaded from", form_data_path)
            
            # Extract and output the texts from the annotated areas
            texts = annotator.extract_texts()
            print("Extracted Texts:", texts)
            
            # Save the texts to a JSON file
            annotator.save_texts_to_json(texts, 'extracted_texts.json')
            print("Texts saved to extracted_texts.json")
    
    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
