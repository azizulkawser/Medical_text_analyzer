import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import xmltodict
import json
import pandas as pd
import pandas as pd
import spacy
from nltk.tree import Tree
import nltk
#nltk.download('punkt')

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
        
        # # Create a button to load an XML file
        # load_button = tk.Button(self.root, text="Load XML", command=self.load_xmi_file)
        # load_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button to process the data and display the output
        process_data_button = tk.Button(self.root, text="Extract Clinical NE", command=self.process_data)
        process_data_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button to extract named entities from the text and display the output
        extract_entities_button = tk.Button(self.root, text="Extract Name Entities", command=self.extract_and_display_entities)
        extract_entities_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button
        tree_button = tk.Button(self.root, text="Visualize Trees", command=self.visualize_trees)
        tree_button.pack(side=tk.TOP, padx=10, pady=10)
        
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
        
    def process_data(self):
        # Clear the output viewer
        self.output_viewer.delete('1.0', tk.END)
        
        # Call the data_processing function
        result_df = data_processing()
        
        # Convert the result DataFrame to a string representation
        output_text = result_df.to_string(index=False)
        
        # Display the output in the output viewer
        self.output_viewer.insert(tk.END, output_text)
    
    def extract_and_display_entities(self):
        # Get the text from the text area
        text = self.text_area.get("1.0", tk.END)

        # Load the spaCy English model
        nlp = spacy.load("en_core_web_sm")

        # Process the text with spaCy
        doc = nlp(text)

        # Initialize lists to store entity types and names
        entity_types = []
        entity_names = []

        # Iterate over the entities in the processed document
        for ent in doc.ents:
            entity_types.append(ent.label_)  # Append the entity type
            entity_names.append(ent.text)    # Append the entity name

        # Create a dataframe from the entity types and names
        entity_df = pd.DataFrame({"Entity Type": entity_types, "Entity Name": entity_names})

        # Clear the output viewer
        self.output_viewer.delete("1.0", tk.END)

        # Display the entity dataframe in the output viewer
        self.output_viewer.insert(tk.END, entity_df.to_string())
    
    def visualize_trees(self):
        text = self.text_area.get("1.0", tk.END).strip()  # Get the text from the input field

        # Tokenize the text into sentences
        sentences = nltk.sent_tokenize(text)

        # Clear the output viewer
        self.output_viewer.delete("1.0", tk.END)

        # Iterate over each sentence
        for sentence in sentences:
            # Tokenize the sentence into words
            words = nltk.word_tokenize(sentence)

            # Perform part-of-speech tagging
            tagged_words = nltk.pos_tag(words)

            # Create a constituency parse tree
            cp = nltk.RegexpParser("NP: {<DT>?<JJ>*<NN>}")

            # Parse the tagged words
            result = cp.parse(tagged_words)

            # Display the constituency parse tree in the output viewer
            self.output_viewer.insert(tk.END, str(result))
            self.output_viewer.insert(tk.END, "\n\n")

def extract_ontology_concept_arr(data):
    ontology_concept_arr_values = []

    if isinstance(data, dict):
        ontology_concept_arr = data.get('@ontologyConceptArr')
        if ontology_concept_arr:
            values = ontology_concept_arr.split(' ')
            ontology_concept_arr_values.extend(values)
    elif isinstance(data, list):
        for item in data:
            ontology_concept_arr = item.get('@ontologyConceptArr')
            if ontology_concept_arr:
                values = ontology_concept_arr.split(' ')
                ontology_concept_arr_values.extend(values)

    return ontology_concept_arr_values

def create_dataframe(data, data_name):
    df_data = []
    
    if isinstance(data, dict):
        df_data.append({'Entity Type': data_name, '@begin': data.get('@begin'), '@end': data.get('@end')})
    elif isinstance(data, list):
        for item in data:
            df_data.append({'Entity Type': data_name, '@begin': item.get('@begin'), '@end': item.get('@end')})
    
    df = pd.DataFrame(df_data)
    return df

def append_normalized_form(df, data):
    normalized_forms = []
    
    for _, row in df.iterrows():
        begin = int(row['@begin'])
        
        normalized_form = None
        
        try:
            for item in data:
                item_begin = int(item['@begin'])
                
                if begin == item_begin:
                    normalized_form = item['@form']
                    break
        except KeyError:
            pass
        
        normalized_forms.append(normalized_form)
    
    df['Entity Name'] = normalized_forms
    return df

def data_processing():
    with open("C:/apache-ctakes-4.0.0.1/output/temp_input.txt.xmi") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    
    json_data = json.dumps(data_dict)

    with open("data_1.json", "w") as json_file:
        json_file.write(json_data)
    
    filename = "data_1.json"
    
    with open(filename, "r") as file:
        data = json.load(file)
    
    try:
        Medication_Mention = data['xmi:XMI']['textsem:MedicationMention']
    except KeyError:
        Medication_Mention = ''
    ontology_concept_arr_MM = extract_ontology_concept_arr(Medication_Mention)
    
    try:
        Procedure_Mention = data['xmi:XMI']['textsem:ProcedureMention']
    except KeyError:
        Procedure_Mention = ''
    ontology_concept_arr_PM = extract_ontology_concept_arr(Procedure_Mention)
    
    try:
        Sign_Symptom_Mention = data['xmi:XMI']['textsem:SignSymptomMention']
    except KeyError:
        Sign_Symptom_Mention = ''
    ontology_concept_arr_SSM = extract_ontology_concept_arr(Sign_Symptom_Mention)
    
    try:
        Disease_Disorder_Mention = data['xmi:XMI']['textsem:DiseaseDisorderMention']
    except KeyError:
        Disease_Disorder_Mention = ''
    ontology_concept_arr_DDM = extract_ontology_concept_arr(Disease_Disorder_Mention)
    
    try:
        Anatomical_Site_Mention = data['xmi:XMI']['textsem:AnatomicalSiteMention']
    except KeyError:
        Anatomical_Site_Mention = ''
    ontology_concept_arr_ASM = extract_ontology_concept_arr(Anatomical_Site_Mention)
    
    df_MM = create_dataframe(Medication_Mention, 'Medication_Mention')
    df_PM = create_dataframe(Procedure_Mention, 'Procedure_Mention')
    df_SSM = create_dataframe(Sign_Symptom_Mention, 'Sign_Symptom_Mention')
    df_DDM = create_dataframe(Disease_Disorder_Mention, 'Disease_Disorder_Mention')
    df_ASM = create_dataframe(Anatomical_Site_Mention, 'Anatomical_Site_Mention')
    
    concat_df = pd.concat([df_DDM, df_MM, df_ASM, df_PM, df_SSM], axis=0)
    
    input_data = data['xmi:XMI']['syntax:ConllDependencyNode']
    df = append_normalized_form(concat_df, input_data)
    return df[['Entity Type','Entity Name']]

if __name__ == '__main__':
    # Create a new instance of the Tkinter root window
    root = tk.Tk()
    
    # Create an instance of the TextViewer class, passing the root window as an argument
    text_viewer = TextViewer(root)
    
    # Start the Tkinter event loop to display the GUI and handle user interactions
    root.mainloop()
