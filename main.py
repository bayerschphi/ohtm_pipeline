from ohtm_pipeline.package_load import *

'''
With this board you can select every option for your topic model. 
You can set the different options on and off via "True" and "False".
All the paths to the folders are set here.
'''


# Path to your mallet folder.
mallet_path: str = r'C:\mallet-2.0.8\bin\mallet'

# All files for the process should be stored in the working_folder.
working_folder: str =  r"C:\Users\phili\Nextcloud2\Python\Topic_Modeling"


# Set the path for your stop_word list.
stopword_file = os.path.join(working_folder + "\german_stopwords_custome.txt")

source_path: str = r"C:\Users\phili\sciebo - Bayerschmidt, Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\Interviews"

source = [
           # "Archiv Zwangsarbeit\komplett",
           # "Archiv Deutsches Gedächtnis\ADG_komplett",
           # "Hannah Arendt Institut Dresden\Bereinigt",
           # "Flucht Vertreibung Versöhnung\Bereinigt",
           # "Museum Friedland\Bereinigt",
           # "Werkstatt der Erinnerungen\gesamt",
           # "Colonia Dignidad\komplett_de"
    "cord"

    ]


# Topic-Modeling Settings:


# if you want to create a new json-file in the data-structure with your own interview-files. They are loaded from source
creat_json = True

# if you want to load an existing json-file, with the used data-structure
load_json = False
load_file_name = "OHD_final_100c_100T_A5_remade"

save_json = True
save_name = "Test"
save_model = True

use_preprocessing = True

use_chunking = True
chunk_setting = 100

use_topic_modeling = True
topics = 100

use_corelation  = False

save_top_words = False
number_of_words = 50

print_json = False
show_bar_graph_corpus = False
show_heatmap_corpus = False

interview_id = "ADG0002"
chunk_number = 0
show_heatmap_interview = False
print_interview_chunk = False

search_for_topics_in_chunks = False
topic_search = 1
chunk_weight = 0.3
search_for_topics_in_interview= False


# advanced options:
#topic_modeling

optimize_interval_mallet= 50
iterations_mallet= 500
alpha= 5

# preprocessing
by_particle = False
by_list = True
lemma = True
pos_filter_setting = True
allowed_postags_settings = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV']

# Inferring new Documents

infer_new_documents = True
trained_json_name = "Test"  # load the trained json and the model to train that json
save_separate_json = True # save the inferred documents as a new json
separate_json_name = "richtig"


if __name__ == "__main__":
    ohtm_pipeline(
            working_folder=working_folder, source= source, source_path = source_path, stopword_file=stopword_file,
            allowed_postags_settings= allowed_postags_settings, save_name= save_name, load_file_name=load_file_name, mallet_path= mallet_path, interview_id=interview_id,
            chunk_setting=chunk_setting, topics=topics, number_of_words=number_of_words, chunk_number=chunk_number,
            topic_search=topic_search, chunk_weight=chunk_weight, optimize_interval_mallet=optimize_interval_mallet,
            iterations_mallet=iterations_mallet, alpha=alpha,
            save_json=save_json, creat_json=creat_json, load_json=load_json, use_preprocessing=use_preprocessing,
            use_chunking=use_chunking, use_topic_modeling=use_topic_modeling, use_corelation=use_corelation,
            save_top_words=save_top_words, print_json=print_json,
            show_bar_graph_corpus=show_bar_graph_corpus, show_heatmap_corpus=show_heatmap_corpus,
            show_heatmap_interview=show_heatmap_interview, print_interview_chunk=print_interview_chunk,
            search_for_topics_in_chunks=search_for_topics_in_chunks,
            search_for_topics_in_interview=search_for_topics_in_interview, by_particle=by_particle, by_list=by_list,
            pos_filter_setting=pos_filter_setting, lemma=lemma, save_model = save_model, infer_new_documents = infer_new_documents, trained_json_name = trained_json_name,
            save_separate_json = save_separate_json, separate_json_name = separate_json_name
    )