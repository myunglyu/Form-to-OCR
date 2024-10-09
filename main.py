import tkinter as tk
from ImageAnnotation import ImageAnnotator

def main():
    # Create the main window
    root = tk.Tk()
    
    # Open file dialog to select an image
    image_path = tk.filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    
    if image_path:
        annotator = ImageAnnotator(root, image_path)
    
    # Run the Tkinter event loop
    root.mainloop()
    
    # Output the annotations
    annotations = annotator.get_annotations()
    print("Annotations:", annotations)
    
    # Extract and output the texts from the annotated areas
    texts = annotator.extract_texts()
    print("Extracted Texts:", texts)
    
    # Save the texts to a JSON file
    annotator.save_texts_to_json(texts, 'extracted_texts.json')
    print("Texts saved to extracted_texts.json")
    
    # Save the form data to a JSON file
    annotator.save_form_data('form_data.json')
    print("Form data saved to form_data.json")

if __name__ == "__main__":
    main()
