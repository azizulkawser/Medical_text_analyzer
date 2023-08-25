import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tree import Tree
from nltk.chunk import RegexpParser
from nltk import pos_tag, word_tokenize, sent_tokenize
import spacy
from spacy import displacy
import webbrowser
import threading
import os
import subprocess
import xmltodict
import json
from tkinter import PhotoImage
from IPython.display import SVG, display

def save_svg_visualizations(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentence_spans = list(doc.sents)

    current_sentence_index = 0
    saved_files = []
    dataframe_rows = []
    
    for sentence in sentence_spans:
        options = {"fine_grained": True, "arrow_stroke": 2, "arrow_width": 8}
        svg = displacy.render([sentence], style="dep", options=options, jupyter=False)
        filename = f"srl_visualization_sentence_{current_sentence_index + 1}.svg"
        saved_files.append(filename)
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(svg)
            
        # Perform semantic role labeling for each sentence
        semantic_role_labeling_output = semantic_role_labeling(sentence.text, doc)
        
        # Create a dataframe row for each sentence
        dataframe_row = {'file_name': filename, 'sentence': sentence.text, 'srl_output': semantic_role_labeling_output}
        dataframe_rows.append(dataframe_row)
        
        current_sentence_index += 1
    
    # Create a dataframe from the collected rows
    dataframe = pd.DataFrame(dataframe_rows)
    
    return saved_files, dataframe

def open_svg_in_browser(path):
    if path:
        webbrowser.open(path)

def open_svg_files_in_browser(dataframe):
    root = tk.Tk()
    root.title("SVG Viewer")

    for _, row in dataframe.iterrows():
        file_paths = row['file_name'].split(", ")  # Split the file_path string into individual paths
        srl_output = row['srl_output'].split("word")
        
        def display_output_thread(path):
            output_viewer = tk.Toplevel(root)
            output_viewer.title("Semantic Role Labeling Output")
            text = tk.Text(output_viewer)
            text.insert(tk.END, srl_output)
            text.pack()
            
        for file_path in file_paths:
            open_button = tk.Button(root, text=f"Open {file_path}", command=lambda path=file_path: threading.Thread(target=open_svg_in_browser(path)).start())
            open_button.pack(pady=5)
            output_button = tk.Button(root, text=f"View SRL Output {file_path}", command=lambda path=file_path: threading.Thread(target=display_output_thread(path)).start())
            output_button.pack(pady=5)

    root.mainloop()

def semantic_role_labeling(sentence, doc):
    # Process the sentence using the model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    # Store the SRL results in a list
    srl_results = []

    # Print the SRL results for each token (word) in the sentence
    for token in doc:
        srl_result = f"Word: {token.text}, SRL: {token.dep_}, Semantic Role: {token.head.text}"
        srl_results.append(srl_result)

    return "\n".join(srl_results)

def visualize_srl(text_area):
    nlp = spacy.load("en_core_web_sm")
    text = text_area.get("1.0", tk.END)
    sentence_token = sent_tokenize(text)

    current_sentence_index = 0
    saved_files = []
    dataframe_rows = []
    
    for sentence in sentence_token:
        doc = nlp(sentence)
        sentence_spans = list(doc.sents)
        options = {"fine_grained": True, "arrow_stroke": 2, "arrow_width": 8}
        svg = displacy.render(sentence_spans, style="dep", options=options, jupyter=False)
        filename = f"srl_visualization_sentence_{current_sentence_index + 1}.svg"
        saved_files.append(filename)
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(svg)
            
        # Perform semantic role labeling for each sentence
        semantic_role_labeling_output = semantic_role_labeling(sentence, doc)
        
        # Create a dataframe row for each sentence
        dataframe_row = {'file_name': filename, 'sentence': sentence, 'srl_output': semantic_role_labeling_output}
        dataframe_rows.append(dataframe_row)
        
        current_sentence_index += 1
    
    # Create a dataframe from the collected rows
    dataframe = pd.DataFrame(dataframe_rows)
    
    # Open SVG files in the browser
    open_svg_files_in_browser(dataframe)

    # Update the output viewer with the SRL output
    srl_output_text = "\n\n".join(dataframe['srl_output'].values)
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, srl_output_text)

class TextViewer:
    
    def __init__(self, root):
        # Setting the title of the GUI
        self.root = root
        self.root.title("Medical Text Ontology Analyzer")
        
        # Create a scrolled text area widget
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # ... Other buttons and widgets ...
        
        # Create an output viewer to display the output content
        self.output_viewer = tk.Text(self.root)
        self.output_viewer.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create a button to load a text file
        open_button = tk.Button(self.root, text="Open Text File", command=self.open_file)
        open_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button to run cTakes clinical pipeline
        run_clinical_pipeline_button = tk.Button(self.root, text="Run cTakes Clinical Pipeline", command=self.run_clinical_pipeline)
        run_clinical_pipeline_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button to process the data and display the output
        process_data_button = tk.Button(self.root, text="Extract Clinical NE", command=self.process_data)
        process_data_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button to extract named entities from the text and display the output
        extract_entities_button = tk.Button(self.root, text="Extract Name Entities", command=self.extract_and_display_entities)
        extract_entities_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a button to visualize trees
        self.current_sentence_index = 0
        tree_button = tk.Button(self.root, text="Chunk Viewer", command=self.visualize_trees)
        tree_button.pack(side=tk.TOP, padx=10, pady=10)
        
        
        # Create a button to visualize semantic role labeling
        SRL_button = tk.Button(self.root, text="Visualize Semantic Role Labeling", command=lambda: self.visualize_srl())
        SRL_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # ... Other buttons and widgets ...
    
    def visualize_srl(self):
        visualize_srl(self.text_area)
    
    # ... Other methods ...
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
            command = r'C:\apache-ctakes-4.0.0.1\bin\runClinicalPipeline -i C:\apache-ctakes-4.0.0.1\testdata\ --xmiOut C:\apache-ctakes-4.0.0.1\output\ --key ###############################'
            
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
    
    def extract_noun_phrases(self, sentence):
        word_tokens = word_tokenize(sentence)
        tagged_words = pos_tag(word_tokens)
        
        # grammar = "NP: {<DT>?<JJ>*<NN>}"
        grammar = r"""
        NP: {<DT|JJ|NN.*>+}          # Chunk sequences of determiners, adjectives, and nouns
        VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs followed by NP, PP, or CLAUSE
        PP: {<IN><NP>}               # Chunk prepositions followed by NP
        CLAUSE: {<NP><VP>}           # Chunk NP followed by VP
    """
        chunk_parser = RegexpParser(grammar)
        result = chunk_parser.parse(tagged_words)
        return result
    
    def visualize_trees(self):
        text = self.text_area.get("1.0", tk.END).strip()
        sentence_token = sent_tokenize(text)
        if self.current_sentence_index < len(sentence_token):
            sentence = sentence_token[self.current_sentence_index]
            self.current_sentence_index += 1
            self.output_viewer.delete(1.0, tk.END)
            result = self.extract_noun_phrases(sentence)
            self.output_viewer.insert(tk.END, f"Sentence {self.current_sentence_index}: {sentence}\n\n")
            result.draw()
    
    def visualize_srl(self):
        visualize_srl(self.text_area)

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
