"""
This is the maine pipeline, that transforms the settings from "main.py" to the different functions.
The main variable is the created dictionary (in this code it is called json, because it is saved as a json).

The json is processed in every single function, returned and given to the next function.

You must not change anything here.

"""

from ohtm_pipeline.package_load import *


def ohtm_pipeline(
        working_folder: str = "", source: list = ["",""], source_path: str = "", stopword_file: str = "",
        allowed_postags_settings: list = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV'],
        save_name: str = "", load_file_name: str = "", mallet_path: str = "", interview_id: str = "",
        chunk_setting: int = 40, topics: int = 50, number_of_words: int = 50, chunk_number: int = 0,
        topic_search: int = 1, chunk_weight: float = 0.3, optimize_interval_mallet: int = 500,
        iterations_mallet: int = 5000, alpha: int = 50, random_seed: int = 100,
        save_json: bool = False, creat_json: bool = False, load_json: bool = False,
        use_preprocessing: bool = False, use_chunking: bool = False,
        use_topic_modeling: bool = False, use_correlation: bool = False, save_top_words: bool = False,
        print_json: bool = False, show_bar_graph_corpus: bool = False, show_heatmap_corpus: bool = False,
        show_heatmap_interview: bool = False,
        print_interview_chunk: bool = False, search_for_topics_in_chunks: bool = False,
        search_for_topics_in_interview: bool = False, by_particle: bool = False,
        by_list: bool = False, pos_filter_setting: bool = False, lemma: bool = False, save_model: bool = False,
        infer_new_documents: bool = False, trained_json_name: str = "",
        save_separate_json: bool = False, separate_json_name: str = "", speaker_txt: bool = True
):

    if not infer_new_documents:

        if creat_json:
            print("Starting to create the json-file")
            top_dic = json_creation_function(source=source, source_path=source_path, speaker_txt=speaker_txt)
            if save_json:
                save_json_function(top_dic=top_dic, working_folder=working_folder, save_name=save_name)

        if load_json:
            top_dic = load_json_function(load_file_name=load_file_name, working_folder=working_folder)
            if save_json:
                save_json_function(top_dic=top_dic, working_folder=working_folder,
                                   save_name=save_name)

        if top_dic == None:
            print("You have to create or load a .json file to use this pipeline")

        if use_preprocessing:
            print("Preprocessing started")
            top_dic = preprocessing(top_dic=top_dic, stoplist_path=stopword_file,
                                    allowed_postags_settings=allowed_postags_settings,
                                    by_list=by_list, lemma=lemma, by_particle=by_particle,
                                    pos_filter_setting=pos_filter_setting)

        if use_chunking:
            print("Chunking started with " + str(chunk_setting) + " chunks")
            top_dic = chunking(top_dic=top_dic, chunk_setting=chunk_setting)

        if use_topic_modeling:
            print("Topic Modeling started with " + str(topics) + " topics")
            top_dic = topic_training_mallet(corpus_dictionary=top_dic, working_folder=working_folder,
                                            save_name=save_name, topics=topics, mallet_path=mallet_path,
                                            optimize_interval_mallet=optimize_interval_mallet,
                                            iterations_mallet=iterations_mallet, random_seed_mallet=random_seed,
                                            alpha=alpha, save_model=save_model, save_json=save_json)

        if use_correlation:
            print("Function will be added")

        if save_top_words:
            save_topic_words(top_dic, working_folder, save_name, number_of_words)
            print("Top Words " + str(chunk_setting) + "was saved")

        if save_json:
            save_json_function(top_dic=top_dic, working_folder=working_folder, save_name=save_name)

    if infer_new_documents:
        # The new documents to be inferred are loaded:
        infer_dic = json_creation_function(source=source, source_path=source_path)

        # The original model is loaded and all variables are set from the model.
        model_dic = load_json_function(load_file_name=trained_json_name, working_folder=working_folder)
        if model_dic["settings"]["preprocessing"]["preprocessed"] == "True":
            print("Preprocessing new documents started")
            if model_dic["settings"]["preprocessing"]["by_list"] == "True":
                by_list = True
            if model_dic["settings"]["preprocessing"]["lemmatization"] == "True":
                lemma = True
            if model_dic["settings"]["preprocessing"]["by_particle"] == "True":
                by_particle = True
            if model_dic["settings"]["preprocessing"]["pos_filter"] == "True":
                pos_filter_setting = True
            stop_words = model_dic["stopwords"]

            # The settings are used, to preprocess the to be inferred documents the same way,
            # the original documents were preprocessed
            infer_dic = preprocessing(top_dic=infer_dic,
                                      allowed_postags_settings=model_dic
                                      ["settings"]["preprocessing"]["allowed_postags"],
                                      by_list=by_list, lemma=lemma, by_particle=by_particle,
                                      pos_filter_setting=pos_filter_setting,
                                      stop_words=stop_words,
                                      infer_new_documents=infer_new_documents)

        # The chunk settings from the original model are loaded and used:
        if model_dic["settings"]["preprocessing"]["chunked"] == "True":
            chunk_setting = model_dic["settings"]["preprocessing"]["chunk_setting"]
            print("Chunking started with " + str(chunk_setting) + " chunks")
            infer_dic = chunking(top_dic=infer_dic, chunk_setting=chunk_setting)

        if model_dic["settings"]["topic_modeling"]["trained"] == "True":
            print("Inferring started with " + str(topics) + " topics")

        infer_dic = topic_inferring(corpus_dictionary=infer_dic,
                                    model_name=trained_json_name,
                                    mallet_path=mallet_path,
                                    working_folder=working_folder,
                                    topics=int(model_dic["settings"]["topic_modeling"]["topics"]),
                                    iterations_mallet=int(model_dic["settings"]["topic_modeling"]["iterations_mallet"]),
                                    random_seed_mallet=int(
                                        model_dic["settings"]["topic_modeling"]["random_seed_mallet"])
                                    )

        if save_separate_json:
            save_json_function(top_dic=infer_dic,
                               working_folder=working_folder,
                               save_name=separate_json_name+"_" + save_name + "_inferred")
            print("Inferred json was saved")
            top_dic = infer_dic
        else:
            top_dic = combine_infer(top_dic=model_dic, infer_dic=infer_dic)
            save_json_function(top_dic=top_dic, working_folder=working_folder, save_name=trained_json_name)
            print("Combined json was saved")

    if print_json:
        if type(top_dic) is not dict:
            top_dic = json.loads(top_dic)
        else:
            top_dic = top_dic
        print(top_dic)

    if show_bar_graph_corpus:
        bar_graph_corpus(top_dic, show_fig=True, return_fig=False)

    if show_heatmap_corpus:
        heatmap_corpus(top_dic, option_selected="all", show_fig=True, return_fig=False, z_score=False)

    if show_heatmap_interview:
        heatmap_interview(top_dic, interview_id, show_fig=True, return_fig=False)

    if print_interview_chunk:
        print_chunk(top_dic, interview_id, chunk_number)

    if search_for_topics_in_chunks:
        print_chunk_with_weight_search(top_dic=top_dic, topic_search=topic_search, chunk_weight=chunk_weight)

    if search_for_topics_in_interview:
        print_chunk_with_interview_weight_search(top_dic=top_dic,
                                                 interview_id=interview_id,
                                                 topic_search=topic_search,
                                                 chunk_weight=chunk_weight)
