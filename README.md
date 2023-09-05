# Medical Text Ontology Analyzer

The **Medical Text Ontology Analyzer** is a graphical user interface (GUI) application designed to analyze medical text using various natural language processing (NLP) techniques and tools. This application provides functionalities for processing medical documents, extracting entities, parsing sentences, and more, all within an easy-to-use interface.

## Features

- Load and analyze medical text files in various formats.
- Integrated support for the cTakes clinical pipeline for advanced medical text analysis
- Perform General NLP Analysis
  - Extract general named entities
  - Perform chunk parsing
  - Conduct constituency parsing
  - Perform dependency parsing
  - Perform semantic role labeling
- Perform Medical NLP Analysis
  - Extract clinical named entities
  - Analyze clinical negation
  - Analyze clinical polarity
- Provide a comprehensive graphical illustration of complex text entity relationships
- Highlight negated words in the text

## GUI
**Medical Text Ontology Analyzer UI**:
![Medical Text Ontology Analyzer](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%201.png)
**Extract Text from weblink**:
![Extract Text from weblink](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%202.png)
**Extract general named entitiese**:
![Extract general named entities](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%203.png)
**Perform chunk parsing**:
![Perform chunk parsing](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%204.png)
**Conduct constituency parsing**:
![Conduct constituency parsing](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%205.png)
**Perform dependency parsing**:
![Perform dependency parsing](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%206.png)
![Perform dependency parsing 1](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%207.png)
**Perform semantic role labeling**:
![Perform semantic role labeling](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%208.png)
**Extract clinical named entities**:
![Extract clinical named entities](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%209.png)
**Analyze clinical negation**:
![Analyze clinical negation](https://github.com/azizulkawser/Medical_text_analyzer/blob/e017ed9321c39fed2c914bfb27608d4238f5d6c3/GUI%2010-Analyze%20clinical%20negation.png)
**Analyze clinical polarity**:
![Analyze clinical polarity](https://github.com/azizulkawser/Medical_text_analyzer/blob/e017ed9321c39fed2c914bfb27608d4238f5d6c3/GUI%2012-Analyze%20clinical%20polarity.png)
**Help**:
![Help](https://github.com/azizulkawser/medical_text_analyzer/blob/33dbcf596f37a28d845aa0b90e8e227e9e36b0a6/GUI%2011.png)

#########################
**Installation Guide for Medical Text Ontology Analyzer**

*Note: This guide assumes that you are using a Windows operating system.*
**Step 1: Clone the repository to your local machine.**
**Step 2: Install Python**

1. If you don't already have Python installed, download the latest Python version (at least Python 3.11) from the official Python website: [Python Downloads](https://www.python.org/downloads/).

2. Run the Python installer and make sure to check the box that says "Add Python to PATH" during installation. This will make it easier to run Python from the command line.

3. Follow the installation wizard's instructions to complete the Python installation.

**Step 3: Install Required Libraries**

Open a command prompt or terminal window and run the following commands to install the necessary Python libraries:

```bash
pip install spacy
pip install nltk
pip install webbrowser
pip install requests
pip install beautifulsoup4
pip install stanza
pip install spacy-stanza
pip install negspacy
pip install pyyaml
```

**Step 4: Download and Install Stanford Parser**

1. Download the Stanford Parser JAR file and models JAR file from the official website: [Stanford Parser](https://stanfordnlp.github.io/CoreNLP/download.html).

2. Create a directory for the Stanford Parser on your system. You can choose any location you prefer.

3. Place the downloaded JAR files (`stanford-parser.jar` and `stanford-parser-3.x.x-models.jar`) into the directory you created in step 2.

**Step 5: Configure Paths in `config.yaml`**

1. Open the `config.yaml` file in a text editor.

2. Configure the following paths in the `config.yaml` file:

   - `ctakes/installation_dir`: Set this to the directory where cTakes Clinical Pipeline is installed.
   - `ctakes/input_dir`: Set this to the directory where input data will be processed.
   - `ctakes/output_dir`: Set this to the directory where cTakes output will be saved.
   - `ctakes/pipeline_key`: Set this to your cTakes pipeline key.

   - `stanford_parser/path_to_jar`: Set this to the path of the Stanford Parser JAR file.
   - `stanford_parser/path_to_models_jar`: Set this to the path of the Stanford Parser models JAR file.

3. Save the `config.yaml` file with your changes.

**Step 6: Run the Application**

1. Navigate to the directory where the script (`medical_text_analyzer.py`) is located.

2. Open a command prompt or terminal window in that directory.

3. Run the application by executing the following command:

   ```bash
   python medical_text_analyzer.py
   ```

4. The Medical Text Ontology Analyzer GUI should open, and you can start using the application to analyze medical text data.

**Step 7: Using the Application**

1. **Run the Application**:
  Run the program by executing the following command:

   ```sh
   python medical_text_ontology_analyzer.py
   ```

2. **Open a Document**:
   
   - After launching the application, a graphical user interface (GUI) window will appear.
   - Click the "Open Text File" button to load a medical text document that you want to analyze.
   - The contents of the selected document will be displayed in the text area within the GUI.

3. **Run cTakes Clinical Pipeline**:
   - Once the text document is loaded, click on the "Run cTakes Clinical Pipeline" button.
   - This action will initiate the cTakes clinical pipeline to process the loaded medical text.
     
4. **Perform Analysis**:
   
   - The application offers a variety of analysis options under different categories. Use these buttons to perform specific analysis tasks:
   
     - **General NLP Analysis**:
       - Click on "General Name Entity" to extract and display general named entities (NE) from the loaded text.
       - Use "Chunk Parsing" to parse sentences and identify chunks like noun phrases (NP), verb phrases (VP), and more. This also visualize the parsed trees for chunk.
       - "Constituency Parsing" helps analyze sentence structure through constituency parsing and visualize the parsed trees.
       - "Dependency Parsing" reveals the grammatical relationships between words and display the realtion. For "Dependency Parsing," the application generates SVG files illustrating dependency relations for each sentence.
       - "Semantic Role Labeling" uncovers relationships and roles between words in sentences.
     
     - **Medical NLP Analysis**:
       - "Clinical Name Entity" extracts specialized clinical named entities.
       - "Clinical Negation" identifies and highlights negated terms for enhanced comprehension.
     
   - Each analysis result will be displayed in the "Output" area of the GUI.

## Dependencies

Make sure to install these dependencies before running the program:

1. **Python**:
   - The application is written in Python, so you need to have Python installed on your system.
   - You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/)

2. **Tkinter**:
   - Tkinter is the standard GUI library for Python, and it's used for creating the graphical user interface of the application.
   - Tkinter usually comes bundled with Python installations, so no separate installation is required.

3. **NLTK**:
   - NLTK (Natural Language Toolkit) is a powerful library for working with human language data and performing various NLP tasks.
   - You can install NLTK using the following command:
     ```
     pip install nltk
     ```

4. **spaCy**:
   - spaCy is a popular NLP library that provides efficient text processing capabilities.
   - Install spaCy using:
     ```
     pip install spacy
     ```
   - Download the English model for spaCy:
     ```
     python -m spacy download en_core_web_sm
     ```

5. **xmltodict**:
   - xmltodict is used to convert XML data into a dictionary format.
   - Install it with:
     ```
     pip install xmltodict
     ```

6. **pandas**:
   - pandas is a data manipulation and analysis library.
   - Install it using:
     ```
     pip install pandas
     ```

7. **Stanford NLP Parser**:
   - If you intend to use the constituency parsing feature, you'll need the Stanford NLP Parser.
   - Download the parser from the official website: [Stanford NLP Parser](https://stanfordnlp.github.io/CoreNLP/index.html#download)
   - Extract the downloaded files and provide the paths in the application.

8. **cTakes**:
   - For using the "Run cTakes Clinical Pipeline" feature, you'll need to install cTakes and provide relevant paths in the application.
   - Download cTakes from the official website: [cTakes Downloads](https://ctakes.apache.org/downloads.cgi)
   - Extract the downloaded files and configure the paths in the application.


These dependencies are essential for running the "Medical Text Ontology Analyzer" application and utilizing its various features. Make sure to install them before using the application for seamless functionality.

## Contributors

- [Mohammad Azizul Kawser](https://github.com/azizulkawser)

## License

This program is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to modify and distribute the code as per the terms of the license.
