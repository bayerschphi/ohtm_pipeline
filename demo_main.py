"""
OHTM-Pipeline:

With this board you can select every option for your topic model.
You can set the different options on and off via "True" and "False".

First set the required paths.
    - the first "mallet_path" to your mallet directory. (see ....)
    - the second one to your working folder. This folder is your working environment.
      All models are saved there and can be loaded from this folder.
    - your stopword file must be stored in this working folder.
"""

"""
This demo is used to test, if the code runs proper and is linked to the demo folder and its demo files.
- You can test importing the text files and preprocessing them. 
- You can print the prepared ohmt_files or create the graphs for this file or use the search functions
- Topic modeling is not able, because you need to install mallet first.
"""

from ohtm.pipeline import ohtm_pipeline_function
import os

''' Path Settings: '''
# Path to your mallet folder.
os.environ['MALLET_HOME'] = r'C:\\mallet-2.0.8'
mallet_path: str = r'C:\mallet-2.0.8\bin\mallet'


# Path to your output_folder.
output_folder: str = (r"Demo")

# Set the path for your stop_word list.
stopword_file_name = "german_stopwords_standard.txt"

# Set the path to your sources. This must be the folder, where your documents are stored in another folder.
source_path: str = (r"Demo\demo_interviews")

source_folder = ["txt_files_without_speaker"]

""" Topic Modeling Settings: """

load_ohtm_file = True
load_file_name = "demo_ohtm_file_2"

create_ohtm_file = False
save_ohtm_file = False
save_name = "demo_ohtm_file"

# You need to set a save_name and set the option save_json to True to save the model
save_model = False

use_preprocessing = False

# If you don't want to chunk your documents, set use_chunking to True and chunk_setting to 0
use_chunking = False
chunk_setting = 20

use_topic_modeling = False
topics = 0

save_top_words = False
number_of_words = 0

print_ohtm_file = True
print_ohtm_file_settings = True
show_bar_graph_corpus = False
show_heatmap_corpus = False

interview_id = "...."
chunk_number = 0
show_heatmap_interview = False
print_interview_chunk = False
search_for_topics_in_chunks = False
topic_search = 0
chunk_weight = 0
search_for_topics_in_interview = False

''' advanced options: '''

# topic_modeling
optimize_interval_mallet = 50
iterations_mallet = 500
alpha = 5
random_seed = 80

# ohtm_file creation
speaker_txt = False
folder_as_archive = True

# preprocessing
# Select just one of those two:
stopword_removal_by_stop_list = True
stopword_removal_by_spacy = False

use_lemmatization = False
lemmatization_model_spacy = "...."
use_pos_filter = False

# possible settings: 'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV', 'PRON', 'ADP', 'DET', 'AUX', 'NUM', 'SCONJ', 'CCONJ', 'X'
allowed_postags_settings_lemmatization = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV']

''' Inferring new documents with an trained topic model'''

infer_new_documents = False
trained_ohtm_file = "...."  # load the trained json and the model to train that json
save_separate_ohtm_file = True  # save the inferred documents as a new json
separate_ohtm_file_name = "...."


if __name__ == "__main__":
    ohtm_pipeline_function(
        output_folder=output_folder, source_folder=source_folder, source_path=source_path,
        stopword_file_name=stopword_file_name, allowed_postags_settings=allowed_postags_settings_lemmatization,
        save_name=save_name, load_file_name=load_file_name, mallet_path= mallet_path, interview_id=interview_id,
        chunk_setting=chunk_setting, topics=topics, number_of_words=number_of_words, chunk_number=chunk_number,
        topic_search=topic_search, chunk_weight=chunk_weight, optimize_interval_mallet=optimize_interval_mallet,
        iterations_mallet=iterations_mallet, alpha=alpha, random_seed=random_seed, save_ohtm_file=save_ohtm_file,
        create_ohtm_file=create_ohtm_file, load_ohtm_file=load_ohtm_file, use_preprocessing=use_preprocessing,
        use_chunking=use_chunking, use_topic_modeling=use_topic_modeling, save_top_words=save_top_words,
        print_ohtm_file=print_ohtm_file, show_bar_graph_corpus=show_bar_graph_corpus,
        show_heatmap_corpus=show_heatmap_corpus, show_heatmap_interview=show_heatmap_interview,
        print_interview_chunk=print_interview_chunk, search_for_topics_in_chunks=search_for_topics_in_chunks,
        search_for_topics_in_interview=search_for_topics_in_interview,
        by_list=stopword_removal_by_stop_list, pos_filter_setting=use_pos_filter, lemma=use_lemmatization,
        save_model=save_model, infer_new_documents=infer_new_documents, trained_ohtm_file=trained_ohtm_file,
        save_separate_ohtm_file=save_separate_ohtm_file, separate_ohtm_file_name=separate_ohtm_file_name,
        speaker_txt=speaker_txt, folder_as_archive=folder_as_archive,
        print_ohtm_file_settings=print_ohtm_file_settings, spacy_model_name=lemmatization_model_spacy,
        stopword_removal_by_spacy=stopword_removal_by_spacy
    )
