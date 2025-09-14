# OHTM Pipeline - Version 0.8
(Oral History Topic Modeling Pipeline)

# Overview
This pipeline presents a complete function set to perform lda mallet topic modeling. With a simple main hub, all options
relating different topic modeling variables can be controlled and used. The pipeline offers the possibility to
analyse your results by searching for topics with weight, printing the topic-list word or analysing the results with
bar_graph oder a heatmap for the corpus or single interviews.
The corpus and all the results are saved in
a special structured ohtm_file. This is the base of the code. The file will be created at the start and then
processed in the different steps of the pipeline.
Import is to mention, that this pipeline is spezialiced for the export format, a .csv file, of oral-history.de
an online archive for oral history interviews. Because of this spezification, all variables in the code are
created around the structure of interviews.

But this pipeline can also be used with other sources, if they based on plane .txt files. How to use the pipeline with
those files, you can see in 5.10.

`Mallet` is neccesarry, if you want to perfom topic modeling.

`Spacy` is required, if you want to use lemmatization or stopword removal with a spacy model.
Other stopword removal otpions can be used without spacy. 

## 1. ohtm_file
The main part of this pipeline is the `ohtm_file`. This is a nested dictionary that contains all the necessary information
and saves the output of topic modeling.
The data structure contains 6 main levels.

- `ohtm_file["corpus"]`: contains all the documents
- `ohtm_file["weight"]`: contains the probability results of the topic modeling process
- `ohtm_file["words"]`: contains the topic_lists for each topic of the topic modeling process
- `ohtm_file["stopwords"]`: contains the list of stopwords that were removed
- `ohtm_file["correlation"]`: will be added later
- `ohtm_file["settings"]`: contains information about all the selected options

The corpus level contains the archive or collection and all the documents within this archive or collection.
The documents are separated to the level of a single sentence that can be enriched with metadata. This lowest level was
the main idea of this structure because it contains the raw sentence and the sentence after the preprocessing.
So we can redirect the results of topic modeling, that are calculated on the chunks of preprocesses sentence back
to the original sentence of the document.

Corpus structure:
```plantext
ohtm_file["corpus"]
    - ["archive_1"]
    - ["archive_2"]
    - ["archive_3"]
        - ["interview_1"]
        - ["interview_2"]
        - ["interview_3"]
        - ["interview_4"]
            - ["model_base"]
            - ["sent"]
                - ["0"]
                - ["1"]
                - ["2"]
                    - ["raw"]
                    - ["cleand"]
                    - ["time"]
                    - ["tape"]
                    - ["speaker"]
                    - ["chunk"]
```
weight structure:
```plaintext
ohtm_file["weight"]
    - ["archive_1"]
    - ["archive_2"]
    - ["archive_3"]
        - ["interview_1"]
        - ["interview_2"]
        - ["interview_3"]
        - ["interview_4"]
            - ["0"] -> chunk number of this interview
            - ["1"]
            - ["2"]
                - ["0"] -> topic Number
                - ["1"]
                - ["2"]
                    - ["weight"] -> weight of this topic in this chunk
```
words structure:
```plaintext
ohtm_file["words"]
    - ["0"]
    - ["1"]
    - ["2"] -> Topic number
        - [0.0, 'word'] -> value of the word in this topic list and the word
```
settings structure:
```plaintext
ohtm_file["settings"]
    - ["interviews"]
        - ["archive_1"]
        - ["archive_2"]
            - Number of documents in this archive
    - ["preprocessing"]
        - ["preprocessed"] -> True or False, if this setting was used
        - ["stopwords_removed"] -> True or False, if this setting was used
        - ["chunked"] -> True or False, if this setting was used
        - ["chunk_setting"] -> Number of words per chunk, that were selected
        - ["allowed_postags"] -> List of postags for the lemmatization
        - ["cleaned_length"] -> information about the cleaned sentences in this corpus
            - ["max_length"]
            - ["min_length"]
            - ["ave_length"]
        - ["threshold_stopwords"] -> threshold for the stopword removal
        - ["lemmatization"] -> True or False, if this setting was used
        - ["pos_filter_setting"] -> True or False, if this setting was used
        - ["stop_words_by_particle"] -> True or False, if this setting was used
        - ["stopwords_by_list"] -> True or False, if this setting was used
        - ["stop_words_by_threshold"] -> True or False, if this setting was used
        - ["stop_words_by_spacy"] -> True or False, if this setting was used
    - ["topic_modeling"]
        - ["trained"] -> True of False, if the corpus is trained or not
        - ["inferred"] -> True of False, if the corpus is inferred or not
        - ["model"] -> Name of the model, that was used for inference
        - ["topics"] -> number of topics of this topic model
        - ["alpha"] -> alpha value of the topic model
        - ["optimize_interval_mallet"] -> setting for the topic model
        - ["iterations_mallet"] -> setting for the topic model
        - ["random_seed_mallet"] -> setting for the topic model
        - ["coherence"] -> C_V coherence score of the topic model
        - ["average_weight"]
        - ["min_weight"]
        - ["max_weight"]
    - ["interviews_trained"] -> list of all archives and interviews, that were used for the model
        - ["archive_1"]
        - ["archive_2"]
            - Number of documents in this archive
    - ["interviews_inferred"]
        - ["archive_1"]  -> list of all archives and interviews, that were inferred by the model
        - ["archive_2"]
            - Number of documents in this archive
```
You can access the different levels and entry by adding ohtm_file["entry1"]["entry2"]. You need all keys as a string.
Some keys are set and orther are variables, depending on the archive and intervie name.

## 2. Features
With this pipeline you can process this options and settings:
- import your documents from a `.csv`, `.odt` or `.txt` file into the `ohtm_file` structure with metadata for your interviews
    -  time_code, tape_numer (ohd), speaker
    - choose if the archives is named after the file or the folder
    - if you have no speaker in `.txt` you can set the option to not have a speaker
- load and save the `ohtm_file`
- preprocess your documents for topic modeling
    - tokenization of the strings
    - lowering the text
    - remove stopwords with different settigsn:
        - with a custome stoplist
        - with a threshold (will be added in future)
        - with a particle system (will be added in future)
        - with spacy models stopwordlist
- lemmatization with spacy models and postag filtering
- chunking of the documents with words per chunk method
- use topic modeling on your corpus
  - set the topic number
  - set the optimize-interval number
  - set the iterations number
  - set the alpha value
  - set the random_seed
- save the topic model itself for inferring
- save the topic words from the topic_lists to a text file
- view your results on a bar chart to see, how the topic weight distributes over the corpus
- view a heatmap of the corpus to see, how the results distributes over the corpus on a detailed level per interview
- view a heatmap of a single interview, to see the weights of the topics in every chunk
- you can print a special chunk of a single interview
- you can search all the chunks of an interview for a special topic with a special weight
- you can search all chunks of the corpus for a special topic with a special weight
- infer new documents with an already trained model, save the `ohtm_file` separately or combine them

## 3. Installation
This pipeline runs on every system. Windows/ Os/ and Linux. Just insert the direct string of your file_path into the
`r"insert_text"`. The pipeline will create the correct file_path with `os.path.join()`

Install all the necessary packages in the requirements.txt

After downloading the repro and added it to your python environment you can start the pipeline
via the main_template.py file. Copy the main_template.py file and rename it to main.py.
Start the pipeline from this main.py file. With this usage, you can update the `ohtm_pipeline` without rearranging
your path files all the time.

First you have to install mallet. Follow the instructions in this step-by-step guide:
https://programminghistorian.org/en/lessons/topic-modeling-and-mallet.
You need the Java developer’s kit in the Version 20.0.2 or higher.

Set the path to your mallet folder. Just insert the file_path: `r'C:\mallet-2.0.8\bin\mallet'` like this.

Chose a folder, where you want to save your files and load them from. this is your output_folder. Set the path
to your output_folder as a simple string.
The custome stop_word file has to be in this folder.

Set the name of your custome stop_word file.

Set the path to the folder, where your interviews/documents are in. Inside the folder you direct to, have to be another
folder, with the documents in it. Each folder in your source_path can be used as an archive.

Set the folders inside your source_path inside the source. Just add the names of the folder intot the list.
```plaintext
source = ["folder_1", "folder_2", "folder_3"]
```

If you want to use spacy for lemmatization or stopword removal, you have to install a spacy model and insert the
spacy model name in  `"lemmatization_model_spacy: "`

## 4. file structure of your interviews/documents

### `.csv file`
 The standard import file, that works best with this pipeline and all the sentence_meta_data is the .csv file with this
 colum structure:

|   A    |    B    |    C    |     D      |
|--------|---------|---------|------------|
| Tape   | Timecode| Speaker | sentences  |

 - Tape: a fragment of interviews split over multiple tapes. So we track the tape number.
 - Timecode: Timecodes of the sentences
 - Speaker: Speaker of the sentence
 - Sentences: The transcript should be in this row as sentences combined with the time codes.

### `.ods file`

|      A       |    B     |      C       |
|--------------|----------|--------------|
| Timecode     | Speaker  | sentences    |

 - Timecode: Timecodes of the sentences
 - Speaker: Speaker of the sentence
 - Sentences: The transcript should be in this row as sentences combined with the time codes.

### `.txt file`

For the best results, your .txt documents should be structured like this. Each speaker should have his only line and at
the start of the line, the speaker should be masked with two stars: *speaker*. The lines will be imported, the speaker
will be logged and assigned to every sentence in this line.

If you don't have any speaker in your texts, and you just want to upload the .txt file, just set the option speaker_txt
to False. The file will be split to the single sentences.

# 5. Usage

`os.environ["MALLET_Home"] = r"....."`
- set your environment for mallet. Follow the instructions on the mallet website:
- Example: `os.environ['MALLET_HOME'] = r'C:\\mallet-2.0.8'`

`mallet_path: = r"......"`
- set the fail path to your mallet folder inside the main mallet folder inside the bin folder.
- Example: `mallet_path: str = r'C:\mallet-2.0.8\bin\mallet'`

`output_folder: r"...."`
- set the path to the folder, you want to save and load your ohtm_files, and stop_word_lists

`stopword_file = r".....txt"`
- enter the name of your stopword file in a .txt file. Each row should be a new word.

`source_path: r"....."`
- set the path to the folder, that contains the folders with the interviews.

`source = ["...", "..."]`
- set the list for the folders, that are in the source_path. Each folder will be opened and the documents imported.
- Example: `source = [ "folder_1", "folder_2"]`

`create_ohtm_file = True/False`
- True: Import the files frorm source and source_path and create a ohtm_file out of them.
- False: No files are imported.
 -If you want to use new douments, you need to run this function.

`load_ohtm_file: True/False`
- True: load an ohtm_file from the output_folder.
- False: nothing happens.
- Just add the name, not the ending .ohtm. Use it wihtout the .ohtm.
- If you have `create_ohtm_file` and load on True, the new files will be created but loaded file will be processed
    in the later steps of the code.

`ohtm_file_load_name: "...."`
- insert the name of the ohtm_file you want to load.

`save_ohtm_file: True/False`
- True: save an ohtm_file you have processed. On different stepts within in the code, the save function is run.

`ohtm_file_save_name`
- save name of the ohtm_file you want to save. If you have loaded an ohtm_file, you can set this with a different name,
and a new file will be saved. Otherwise, it will be overwritten.

`save_model = False/True`
- `True`: Save the model you processed in the topic-modeling, the model will be saved inside a model folder with the same,
name as the ohtm_file. You can load it in the inferr section to enrich new documents.

`use_preprocessing: True/False`
- `Ture`: The preprocessing pipeline will be startet, and the ohtm_file, createt or loaded will be processed.
- In the advanced settings you can set options for different steps inside the preprocessing function:
    - `by_particle`
        - this function will be added later
    - `stopword_removal_by_stop_list = True/False`
        - use the stopword removal by the custome stopword_list.txt file
    - `stopword_removal_by_spacy = True/False`
        - removes stopwords with the spacy list of the used spacy model
    - `use_lemmatization = True`
        - activate the lemmatization function of spacy with the used spacy model
    - `lemmatization_model_spacy = "de_core_news_lg"` (str)
        - set the spacy models name you want to use for stopword_removal and lemmatization
    - `use_pos_filter = True/False`
        - set this to True, if you want to use postag filtering
    - `allowed_postags_settings_lemmatization = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV']`
        - possible settings: `'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV', 'PRON',
                                'ADP', 'DET', 'AUX', 'NUM', 'SCONJ', 'CCONJ', 'X'`
- the sentences in raw will be cleaned and then written in the cleaned section inside the ohtm_file

`use_chunking = False/True`
- `True`: Use chunking, that adds up the different cleaned sentences with the max wort count, set. The chunk does not split,
single sentences, but keeps the together.

`chunk_setting = int`
- set the max wordcount of the chunks.
- set this option to 0 to use no chunking.

`use_topic_modeling = True/False`
- set to True, to use the topic_modeling pipeline, and calculate a topic model with lda mallet.
- in the advanced settings, you can specify single variables.
    - `optimize_interval_mallet = int`
    - `iterations_mallet = int`
    - `alpha = int`
    - `random_seed = int`

`topics = int`
- set the numbers of topics for the topic-modeling calculation

`save_top_words = True/False`
- `True`: saves a .txt file with the top words of the topic lists. It will be saved with the ohtm_file_save_name inside
the working folder.

`numer_of_words = int`
- sets the options for save_top_words to how many words are printed of the topic_lists.

`print_ohtm_file = False/True`
- `True`: prints the ohtm_file inside the console

`print_ohtm_file_settings = False/True`
- `True`: prints the ohtm_file["settings"] inside the console

`show_bar_graph_corpus = False/True`
- creates a bar graph, that shows the weight of each topic for the hole corpus. It will be opened inside your browser

`show_heatmap_corpus = False/True`
- creates a heat map, that shows the weight of each topic for each interview inside the corpus.
 It will be opened inside your browser

`search_for_topics_in_chunks = False/True`
- `True`: You can search every chunk for a special weight of topic. The results will be printed inside the console.

`topic_search = int`
- sets the topic, that will be searched in search for topics in chunks or in interview

`chunk_weight = int`
- sets the weight the topic will be searched for. all results above will be printed.

`interview_id = "interview_id"` (str)
- if you want so search in the chunks of a single intervivew/document, you can name it here.

`print_interview_chunk = False/True`
- `True`: You can print a special chunk of a single interview/document

`chunk_number = 10`
- if you want to print a special chunk from one interview, you can set it here

`search_for_topics_in_chunks = True/False`
- `True`: If you not want to search in the hole corpus for a topic with a special weight, but in one interview/document,
you can set it here.

`show_heatmap_interview = False/True`
- True`: shows a heat map of a single interview and the topic weights of each chunk.

`speaker_txt = False/True`
- `True`: Your `.txt file` has a speaker marked with `*` and will be read like this as speaker.
- `False`: Your `.txt file` has no speaker.

`folder_as_archive = True/False`
- `True`: The archive name for your `ohtm_file` will be taken from the folder, where the interviews/documents are inside.
- `False`: The archive will be named after the first 3 letters from the filename of the interviews/docuemnts. That is
standard for the ohd-files.

`infer_new_documents = False/True`
- `True`: if you want to enrich new docuemnts with a trained model.

`trained_ohtm_file = "trained_ohtm_file_name"`
- name of the model you want to load for the inferring process. Make sure, you saved the model before.

`save_separate_ohtm_file = True/False`
- `True`: The new documents, you want to enrich, will be saved as a new `ohtm_file`
- `False`: The new documents, you inferred, will be added to the existing `ohtm_file` of the loaded model

`separate_ohtm_file_name = "inferred_ohmt_file_name"`
- if you want to save the inferred documents as a new `ohtm_file` you have to set the name here.


created by Philipp Bayerschmidt 20.02.2025

