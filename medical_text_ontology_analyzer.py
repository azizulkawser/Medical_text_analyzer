import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os

class TextViewer:
    
    def __init__(self, root):
        # Setting the title of the GUI
        self.root = root
        self.root.title("Medical Text Ontology Analyzer")
        
        # Create a scrolled text area widget
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create an output viewer to display the output content
        self.output_viewer = tk.Text(self.root)
        self.output_viewer.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create a button to load an text file
        open_button = tk.Button(self.root, text="Open Text File", command=self.open_file)
        open_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button to run cTakes clinical pipeline
        run_clinical_pipeline_button = tk.Button(self.root, text="Run cTakes Clinical Pipeline", command=self.run_clinical_pipeline)
        run_clinical_pipeline_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button to load an XML file
        load_button = tk.Button(self.root, text="Load XML", command=self.load_xmi_file)
        load_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button to clear the text area and output viewer
        clear_button = tk.Button(self.root, text="Clear Viewer", command=self.clear_viewer)
        clear_button.pack(side=tk.TOP, padx=10, pady=10)
                
    def open_file(self):
        # Open a file dialog to prompt the user to select a file
        file_path = filedialog.askopenfilename()
        
        # Check if a file was selected
        if file_path:
            # If a file was selected, open it in read mode
            with open(file_path, "r") as file:
                # Read the contents of the file
                text_content = file.read()
            
            # Clear the existing text in the text area widget
            self.text_area.delete("1.0", tk.END)
            
            # Insert the contents of the file into the text area widget at the end
            self.text_area.insert(tk.END, text_content)
            
    def run_clinical_pipeline(self):
        # Get the text from the text area
        text = self.text_area.get("1.0", tk.END).strip()
        
        # Check if the text is empty
        if not text:
            # Display a warning message if no text is found
            messagebox.showwarning("No Text", "No text input found.")
            return
        
        # Save the text to a temporary file
        temp_file = r"C:\apache-ctakes-4.0.0.1\testdata\temp_input.txt"
        with open(temp_file, "w") as file:
            # Write the text content to the temporary file
            file.write(text)
        
        try:
            # Call the cTakes clinical pipeline to process the text
            command = r'C:\apache-ctakes-4.0.0.1\bin\runClinicalPipeline -i C:\apache-ctakes-4.0.0.1\testdata\ --xmiOut C:\apache-ctakes-4.0.0.1\output\ --key efd9c726-5226-43c1-8cb1-c5ac40bae98c'
            
            # Run the command as a subprocess, using the cTakes directory as the current working directory
            subprocess.run(command, shell=True, cwd=r'C:\apache-ctakes-4.0.0.1')
            
            # Delete the temporary input file
            os.remove(temp_file)
            
            # Show a success message indicating that the text was processed successfully
            messagebox.showinfo("Text Processed", "Text processed successfully!")
        except subprocess.CalledProcessError:
            # Display an error message if an error occurs during text processing
            messagebox.showerror("Error", "An error occurred while processing the text.")
            
    def display_content(self, content):
        # Clear the existing text in the text area widget
        self.text_area.delete("1.0", tk.END)
        
        # Insert the given content into the text area widget at the end
        self.text_area.insert(tk.END, content)
        
    def load_xmi_file(self):
        # Open a file dialog to prompt the user to select an XMI file
        file_path = filedialog.askopenfilename(filetypes=[("XMI Files", "*.xmi")])

        # Check if a file was selected
        if file_path:
            try:
                # Perform operations to load and process the XMI file
                # Clear the output viewer
                self.output_viewer.delete("1.0", tk.END)
                
                # Read the content of the XML file
                with open(file_path, "r") as file:
                    xmi_content = file.read()
                
                # Display the XML content in the output viewer
                self.output_viewer.insert(tk.END, xmi_content)
                
                # Show a message indicating that the XMI file was loaded successfully
                messagebox.showinfo("File Loaded", "XMI file loaded successfully!")
            except Exception as e:
                # Display an error message if an error occurs while loading the XMI file
                messagebox.showerror("Error", f"An error occurred while loading the XMI file:\n{str(e)}")
        else:
            # Display a message indicating that no file was selected
            messagebox.showinfo("No File Selected", "No XMI file selected.")
            
    def clear_viewer(self):
        # Clear the text area widget
        self.text_area.delete("1.0", tk.END)
        
        # Clear the output viewer widget
        self.output_viewer.delete("1.0", tk.END)


if __name__ == '__main__':
    # Create a new instance of the Tkinter root window
    root = tk.Tk()
    
    # Create an instance of the TextViewer class, passing the root window as an argument
    text_viewer = TextViewer(root)
    
    # Start the Tkinter event loop to display the GUI and handle user interactions
    root.mainloop()
