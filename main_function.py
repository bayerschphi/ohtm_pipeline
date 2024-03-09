from ohtm import topic_modeling_w2v
from settings import *


# Topic-Modeling Settings:
save_json = True
save_name = "OHD_complete_29_01_2024_pre_100C"

creat_json = False   # if you want to create a new json-file in the data-structure with your own interview-files.
json_file_name = "OHD_complete_raw"

load_json = True   # if you want to load an existing json-file, with the used data-structure
load_file_name = "OHD_complete_29_01_2024"

use_preprocessing = True

use_chunking = True
chunk_setting = 100

use_topic_modeling = False
use_w2v = False
topics = 100

use_corelation = False

save_top_words = True
number_of_words = 50

if __name__ == "__main__":
    if creat_json == True:
        print("Starting creating json")
        top_dic = json_creation(working_folder, source, Save = False)

    if load_json == True:
        print("File {" + load_file_name + "} was loaded")
        with open(working_folder + load_file_name) as f:
            top_dic = json.load(f)

    if use_preprocessing == True:
        print("Preprocessing started")
        top_dic = preprocessing(top_dic, stopword_file)

    if use_chunking == True:
        print("Chunking started with " + str(chunk_setting) + " chunks")
        top_dic = chunking(top_dic, chunk_setting)

    if use_topic_modeling == True:
        print("Topic Modeling started with " + str(topics) + " topics")
        top_dic = topic_training_mallet_new(top_dic, topics=topics, mallet_path=mallet_path, chunking=True)

    if use_w2v == True:
        print("Topic Modeling started with w2v")
        top_dic = topic_modeling_w2v(top_dic, topics=topics, chunking=True)

    if use_corelation == True:
        print("Topic Modeling entrichment started")
        horizontal_correlation_matrix(top_dic, enrich_json=True)
        for number in range(2, 4, 1):
            vertical_correlation_matrix(top_dic, gross_nr_correlations_per_chunk=number, enrich_json=True)

        print(top_dic["correlation"]["verical"])

    if save_top_words:
        out = open(working_folder + save_name + "top_words_" "50_words" + '.txt', 'w', encoding='UTF-8')
        number_of_words
        word_dic = {}
        for top_words in top_dic["words"]:
            out_line = []
            for i in range(number_of_words):
                out_line.append((top_dic["words"][top_words])[i][1])
            out.write("Topic " + "\n" + str(top_words) + "\n")
            out.write(str(out_line) + "\n")
            out.write("\n")
            word_dic[top_words] = out_line
        out.close
        print("Top Words " + str(chunk_setting) + "was saved" )

    if save_json == True:
        with open(working_folder + save_name, "w", encoding="utf-8") as f:
            json.dump(top_dic, f)
        print("Json was saved")

    #print(top_dic)
    #
    # bar_dic(top_dic)
    # value = "all"
    # heatmap_corpus(top_dic, option_selected=value)
    #
    # heatmap_interview(top_dic, "ADG0002")
    # chronology_matrix(top_dic,"ADG2674", print_fig = True )
    #
    # print(top_dic["korpus"]["ADG"]["ADG2674"])