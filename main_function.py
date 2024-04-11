
from ohtm.package_load import *



def ohtm_main_function(
        working_folder: str="", source: list = ["",""], stopword_file:str = "", allowed_postags_settings: list =['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV'], save_name: str="",load_file_name: str="", mallet_path:str="", interview_id: str = "",
        chunk_setting:int=40, topics:int = 50, number_of_words: int = 50,chunk_number: int=0, topic_search:int=1, chunk_weight:float=0.3,optimize_interval_mallet: int = 500,
        iterations_mallet: int = 5000, alpha: int = 50,
        save_json: bool = False, creat_json: bool = False, load_json: bool = False, use_preprocessing: bool = False, use_chunking: bool = False,
        use_topic_modeling:bool = False, use_w2v:bool=False, use_corelation:bool = False, save_top_words: bool =False, print_json:bool=False,
        show_bar_graph_corpus:bool = False,show_heatmap_corpus:bool = False, show_heatmap_interview: bool = False,print_interview_chunk: bool = False, search_for_topics_in_chunks:bool = False,
        search_for_topics_in_interview:bool = False, by_particle: bool = False, by_list:bool = False, pos_filter_setting: bool = False, lemma: bool=False,
):
    if creat_json == True:
        print("Starting creating json")
        top_dic = dictionary_creation(source)

    if load_json == True:
        print("File {" + load_file_name + "} was loaded")
        with open(working_folder + load_file_name) as f:
            top_dic = json.load(f)

    if use_preprocessing == True:
        print("Preprocessing started")
        top_dic = preprocessing(top_dic, stopword_file, allowed_postags_settings=allowed_postags_settings, by_list=by_list, lemma=lemma, by_particle=by_particle, pos_filter_setting=pos_filter_setting)

    if use_chunking == True:
        print("Chunking started with " + str(chunk_setting) + " chunks")
        top_dic = chunking(top_dic, chunk_setting)

    if use_topic_modeling == True:
        print("Topic Modeling started with " + str(topics) + " topics")
        top_dic = topic_training_mallet(top_dic, topics=topics, mallet_path=mallet_path, optimize_interval_mallet=optimize_interval_mallet, iterations_mallet=iterations_mallet, alpha = alpha)

    if use_w2v == True:
        print("Topic Modeling started with w2v")
        top_dic = topic_modeling_w2v(top_dic, topics=topics, chunking=True)

    if use_corelation == True:
        try:
            print("Topic Modeling enrichment started")
            horizontal_correlation_matrix(top_dic, enrich_json = True)
            vertical_correlation_matrix(top_dic, gross_nr_correlations_per_chunk = 2, enrich_json= True)
            vertical_correlation_matrix(top_dic, gross_nr_correlations_per_chunk = 3, enrich_json= True)
            vertical_correlation_matrix(top_dic, gross_nr_correlations_per_chunk = 4, enrich_json= True)

        except NameError or ImportError:
            print("------ERROR------")
            print("Not able to enrich the model, because the neceserry pipeline is not installed")
            print("Install >>Interview Chronologie Analyses by Dennis Möbus<< from Github")

    if save_top_words:
        save_topic_words(top_dic, working_folder, save_name,number_of_words)
        print("Top Words " + str(chunk_setting) + "was saved" )

    if save_json == True:
        if type(top_dic) is not dict:
            top_dic = json.loads(top_dic)
        else:
            top_dic = top_dic
        with open(working_folder + save_name, "w", encoding="utf-8") as f:
            json.dump(top_dic, f)
        print("Json was saved")

    if print_json == True:
        if type(top_dic) is not dict:
            top_dic = json.loads(top_dic)
        else:
            top_dic = top_dic
        print(top_dic)

    if show_bar_graph_corpus == True:
        bar_graph_corpus(top_dic, show_fig = True, return_fig = False)

    if show_heatmap_corpus == True:
        heatmap_corpus(top_dic, option_selected = "all", show_fig=True, return_fig=False, z_score = False)

    if show_heatmap_interview == True:
        heatmap_interview(top_dic, interview_id, show_fig= True, return_fig = False)

    if print_interview_chunk == True:
        print_chunk(top_dic, interview_id, chunk_number)

    if search_for_topics_in_chunks == True:
        print_chunk_with_weight_search(top_dic, topic_search, chunk_weight)

    if search_for_topics_in_interview == True:
        print_chunk_with_interview_weight_search(top_dic, interview_id, topic_search, chunk_weight)