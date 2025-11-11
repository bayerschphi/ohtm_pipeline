"""
OHTM-Pipeline:

With this board you can select every option for your topic model.
You can set the different options on and off via "True" and "False".

First set the required paths.
    - the first "mallet_path" to your mallet directory.
     (see https://programminghistorian.org/en/lessons/topic-modeling-and-mallet)
    - the second one to your output_folder. This folder is your working environment.
      All models are saved there and can be loaded from this folder.
    - your stopword file must be stored in this output_folder.
"""

import os
from ohtm_pipeline.pipeline_function.pipeline import ohtm_pipeline_function

''' Path Settings: '''
# Path to your mallet folder.
os.environ['MALLET_HOME'] = r'C:\\mallet-2.0.8'
mallet_path: str = r'C:\mallet-2.0.8\bin\mallet'

# Path to your output_folder.
output_folder: str = (r"C:\Users\phili\sciebo - Bayerschmidt,"
                       r" Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\Topic Modeling\ohtm_files")

# Set the path for your stop_word list.
stopword_file_name = r"german_stopwords_adoption.txt"
# stopword_file_name = r"german_stopwords_custome.txt"

# Set the path to your sources. This must be the folder, where your documents are stored in another folder.
source_path: str = r"C:\Users\phili\sciebo - Bayerschmidt, Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\Interviews\inferring test\interviews"

source_folder =  ["cd","eg", "ev", "ifu", "mog", "stsg", "za"]

""" Topic Modeling Settings: """

load_ohtm_file = False
load_file_name = "OHD_final_100c_100T_A5_final_label_test"

create_ohtm_file = True
save_ohtm_file = True
save_name = "inferr_test_large"

# You need to set a save_name and set the option save_json to True to save the model
save_model = False

use_preprocessing = True

# If you don't want to chunk your documents, set use_chunking to True and chunk_setting to 0
use_chunking = True
chunk_setting = 100

use_topic_modeling = True
topics = 45


save_topic_words = False
print_topic_words = False
number_of_words = 100

print_ohtm_file = False
print_ohtm_file_settings = False
show_bar_graph_corpus = False
show_heatmap_corpus = False

z_score_filter = False
filter_heatmap_corpus = False
archive_selected = "MFL"

interview_id = "MFL20006"
chunk_number = 1
show_heatmap_interview = False
print_interview_chunk = False
search_for_topics_in_chunks = False
topic_search = 44
chunk_weight = 0.4
search_for_topics_in_interview = False

''' advanced options: '''

# topic_modeling
optimize_interval_mallet = 500
iterations_mallet = 5000
alpha = 5
random_seed = 100

# ohtm_file creation
speaker_txt = True
folder_as_archive = True

# preprocessing
# Select just ONE of those two:
stopword_removal_by_stop_list = True
stopword_removal_by_spacy = False

use_lemmatization = True
lemmatization_model_spacy = "de_core_news_lg"
use_pos_filter = True
# possible settings: 'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV', 'PRON', 'ADP', 'DET', 'AUX', 'NUM', 'SCONJ', 'CCONJ', 'X'
allowed_postags_settings_lemmatization = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV']

anonymize = False
# List of interviews, that should not be anonymized
exceptions = []

#Processing

topic_words_with_weight = True




''' Inferring new documents with an trained topic model'''

infer_new_documents = True
trained_ohtm_file = "OHD_final_100c_100T_A5_remade"  # load the trained json and the model to train that json
save_separate_ohtm_file = True  # save the inferred documents as a new json
separate_ohtm_file_name = "inferr_test_large"

if __name__ == "__main__":
    ohtm_pipeline_function(
        output_folder=output_folder,
        source_folder=source_folder,
        source_path=source_path,
        stopword_file_name=stopword_file_name,
        allowed_postags_settings=allowed_postags_settings_lemmatization,
        save_name=save_name,
        load_file_name=load_file_name,
        mallet_path= mallet_path,
        interview_id=interview_id,
        chunk_setting=chunk_setting,
        topics=topics,
        number_of_words=number_of_words,
        chunk_number=chunk_number,
        topic_search=topic_search,
        chunk_weight=chunk_weight,
        optimize_interval_mallet=optimize_interval_mallet,
        iterations_mallet=iterations_mallet,
        alpha=alpha,
        random_seed=random_seed,
        save_ohtm_file=save_ohtm_file,
        create_ohtm_file=create_ohtm_file,
        load_ohtm_file=load_ohtm_file,
        use_preprocessing=use_preprocessing,
        use_chunking=use_chunking,
        use_topic_modeling=use_topic_modeling,
        save_top_words=save_topic_words,
        print_topic_words=print_topic_words,
        print_ohtm_file=print_ohtm_file,
        show_bar_graph_corpus=show_bar_graph_corpus,
        show_heatmap_corpus=show_heatmap_corpus,
        filter_heatmap_corpus=filter_heatmap_corpus,
        archive_selected=archive_selected,
        z_score_filter=z_score_filter,
        show_heatmap_interview=show_heatmap_interview,
        print_interview_chunk=print_interview_chunk,
        search_for_topics_in_chunks=search_for_topics_in_chunks,
        search_for_topics_in_interview=search_for_topics_in_interview,
        by_list=stopword_removal_by_stop_list,
        pos_filter_setting=use_pos_filter,
        lemma=use_lemmatization,
        save_model=save_model,
        infer_new_documents=infer_new_documents,
        trained_ohtm_file=trained_ohtm_file,
        save_separate_ohtm_file=save_separate_ohtm_file,
        separate_ohtm_file_name=separate_ohtm_file_name,
        speaker_txt=speaker_txt,
        folder_as_archive=folder_as_archive,
        print_ohtm_file_settings=print_ohtm_file_settings,
        spacy_model_name=lemmatization_model_spacy,
        stopword_removal_by_spacy=stopword_removal_by_spacy,
        anonymize=anonymize,
        exceptions=exceptions,
        show_links = False,
        topic_words_with_weight=topic_words_with_weight
    )