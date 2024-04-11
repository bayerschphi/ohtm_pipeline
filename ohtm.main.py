from ohtm.package_load import *

mallet_path = 'C:\\mallet-2.0.8\\bin\\mallet'
os.environ['MALLET_HOME'] = 'C:\\mallet-2.0.8'
working_folder = "C:\\Users\\phili\\sciebo - Bayerschmidt, Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\\Interviews\\code_review\\"

stopword_file = working_folder + "german_stopwords_custome.txt"

source_path = "C:\\Users\\phili\\sciebo - Bayerschmidt, Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\\Interviews\\code_review\\"

source = [
              source_path+'Archiv Zwangsarbeit',
              source_path+'Archiv Deutsches Gedächtnis',
              source_path+"Hannah Arend Institut",
              ]


# Topic-Modeling Settings:
# if you want to load an existing json-file, with the used data-structure
load_json = False
load_file_name = "code_review_test_preprocessed_chunked_70"

save_json = True
save_name = "code_review_test_preprocessed_chunked_70_topic_40_test"

# if you want to create a new json-file in the data-structure with your own interview-files. They are loaded from source
creat_json = True

use_preprocessing = True

use_chunking = True
chunk_setting = 70

use_topic_modeling = True
use_w2v = False
topics = 40

use_corelation  = True

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

if __name__ == "__main__":
    ohtm_main_function(
            working_folder, source, stopword_file, save_name,load_file_name, mallet_path, interview_id,
            chunk_setting, topics, number_of_words,chunk_number, topic_search, chunk_weight,
            save_json, creat_json, load_json, use_preprocessing, use_chunking,
            use_topic_modeling, use_w2v, use_corelation, save_top_words, print_json,
            show_bar_graph_corpus,show_heatmap_corpus, show_heatmap_interview,print_interview_chunk,
            search_for_topics_in_chunks, search_for_topics_in_interview
    )