from ohtm.package_load import *

mallet_path = 'C:\\mallet-2.0.8\\bin\\mallet'
os.environ['MALLET_HOME'] = 'C:\\mallet-2.0.8'
working_folder = "C:\\Users\\bayerschmidt\\sciebo - Bayerschmidt, Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\\Interviews\\code_review\\"

stopword_file = working_folder + "german_stopwords_custome.txt"

source_path = "C:\\Users\\bayerschmidt\\sciebo - Bayerschmidt, Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\\Interviews\\code_review\\"

source = [
              source_path+'Archiv Zwangsarbeit',
              source_path+'Archiv Deutsches Gedächtnis',
              source_path+"Hannah Arend Institut",
              ]


# Topic-Modeling Settings:
# if you want to load an existing json-file, with the used data-structure
load_json = True
load_file_name = "ohd_complete_70_80_vortrag"

save_json = False
save_name = "code_review_preprocessed_chunked_70_topic_20"

# if you want to create a new json-file in the data-structure with your own interview-files. They are loaded from source
creat_json = False

use_preprocessing = False

use_chunking = False
chunk_setting = 70

use_topic_modeling = False
topics = 30
use_w2v = False


use_corelation  = False

save_top_words = True
number_of_words = 50

print_json = True
show_bar_graph_corpus = True
show_heatmap_corpus = True

interview_id = "ADG0002"
chunk_number = 0
show_heatmap_interview = True
print_interview_chunk = True

search_for_topics_in_chunks = True
topic_search = 1
chunk_weight = 0.3
search_for_topics_in_interview= True


# advanced options:
#topic modeling

optimize_interval_mallet= 500
iterations_mallet= 5000
alpha= 50

# preprocessing
by_particle = False
by_list = True
lemma = True
pos_filter_setting = True
allowed_postags_settings = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV']




if __name__ == "__main__":
    ohtm_main_function(
            working_folder=working_folder, source= source, stopword_file=stopword_file,
            allowed_postags_settings= allowed_postags_settings, save_name= save_name, load_file_name=load_file_name, mallet_path= mallet_path, interview_id=interview_id,
            chunk_setting=chunk_setting, topics=topics, number_of_words=number_of_words, chunk_number=chunk_number,
            topic_search=topic_search, chunk_weight=chunk_weight, optimize_interval_mallet=optimize_interval_mallet,
            iterations_mallet=iterations_mallet, alpha=alpha,
            save_json=save_json, creat_json=creat_json, load_json=load_json, use_preprocessing=use_preprocessing,
            use_chunking=use_chunking, use_topic_modeling=use_topic_modeling, use_w2v=use_w2v, use_corelation=use_corelation,
            save_top_words=save_top_words, print_json=print_json,
            show_bar_graph_corpus=show_bar_graph_corpus, show_heatmap_corpus=show_heatmap_corpus,
            show_heatmap_interview=show_heatmap_interview, print_interview_chunk=print_interview_chunk,
            search_for_topics_in_chunks=search_for_topics_in_chunks,
            search_for_topics_in_interview=search_for_topics_in_interview, by_particle=by_particle, by_list=by_list,
            pos_filter_setting=pos_filter_setting, lemma=lemma
    )