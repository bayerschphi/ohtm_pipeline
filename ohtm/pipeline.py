"""
This is the maine pipeline, that transforms the settings from "main.py" to the different functions.
The main variable is the created dictionary (in this code it is called json, because it is saved as a json).

The json is processed in every single function, returned and given to the next function.

You must not change anything here.

"""

from ohtm.basic_functions.ohtm_file_inferred_combination import combine_infer
from ohtm.basic_functions.save_load import save_json_function
from ohtm.basic_functions.save_load import load_json_function
from ohtm.preprocessing_functions.chunking import chunking
from ohtm.basic_functions.ohtm_file_creation import ohtm_file_creation_function
from ohtm.topic_evaluation.bar_graph import bar_graph_corpus
from ohtm.topic_evaluation.heatmaps import heatmap_interview
from ohtm.topic_evaluation.heatmaps import heatmap_corpus
from ohtm.topic_modeling_functions.topic_training_mallet import topic_training_mallet
from ohtm.topic_modeling_functions.topic_inferring import topic_inferring
from ohtm.preprocessing_functions.preprocessing import preprocessing
from ohtm.basic_functions.save_load import save_topic_words
from ohtm.topic_evaluation.topics_prints import print_chunk
from ohtm.topic_evaluation.topics_prints import print_chunk_with_weight_search
from ohtm.topic_evaluation.topics_prints import print_chunk_with_interview_weight_search
from ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file


def ohtm_pipeline_function(
        working_folder: str = "", source: list = ["",""], source_path: str = "", stopword_file: str = "",
        allowed_postags_settings: list = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV'],
        save_name: str = "", load_file_name: str = "", mallet_path: str = "", interview_id: str = "",
        chunk_setting: int = 40, topics: int = 50, number_of_words: int = 50, chunk_number: int = 0,
        topic_search: int = 1, chunk_weight: float = 0.3, optimize_interval_mallet: int = 500,
        iterations_mallet: int = 5000, alpha: int = 50, random_seed: int = 100,
        save_ohtm_file: bool = False, create_ohtm_file: bool = False, load_ohtm_file: bool = False,
        use_preprocessing: bool = False, use_chunking: bool = False,
        use_topic_modeling: bool = False, use_correlation: bool = False, save_top_words: bool = False,
        print_ohtm_file: bool = False, show_bar_graph_corpus: bool = False, show_heatmap_corpus: bool = False,
        show_heatmap_interview: bool = False,
        print_interview_chunk: bool = False, search_for_topics_in_chunks: bool = False,
        search_for_topics_in_interview: bool = False, by_particle: bool = False,
        by_list: bool = False, pos_filter_setting: bool = False, lemma: bool = False, save_model: bool = False,
        infer_new_documents: bool = False, trained_ohtm_file: str = "",
        save_separate_ohtm_file: bool = False, separate_ohtm_file_name: str = "", speaker_txt: bool = True,
        folder_as_archive: bool = False, print_ohtm_file_settings: bool = False,
        spacy_model_name: str = "de_core_news_lg", stopword_removal_by_spacy: bool = False
):

    if not infer_new_documents:

        if create_ohtm_file:
            print("Starting to create the ohtm_file")
            ohtm_file = ohtm_file_creation_function(source=source, source_path=source_path, speaker_txt=speaker_txt,
                                                    folder_as_archive=folder_as_archive)
            if save_ohtm_file:
                save_json_function(ohtm_file=ohtm_file, working_folder=working_folder, save_name=save_name)

        if load_ohtm_file:
            ohtm_file = load_json_function(load_file_name=load_file_name, working_folder=working_folder)
            if save_ohtm_file:
                save_json_function(ohtm_file=ohtm_file, working_folder=working_folder,
                                   save_name=save_name)

        if ohtm_file == None:
            print("You have to create or load a ohtm_file to use this pipeline")

        if use_preprocessing:
            print("Preprocessing started")
            ohtm_file = preprocessing(ohtm_file=ohtm_file, stoplist_name=stopword_file,
                                      allowed_postags_settings=allowed_postags_settings,
                                      by_list=by_list, lemma=lemma, by_particle=by_particle,
                                      pos_filter_setting=pos_filter_setting, spacy_model=spacy_model_name,
                                      stopword_removal_by_spacy=stopword_removal_by_spacy,
                                      working_folder=working_folder)

        if use_chunking:
            print("Chunking started with " + str(chunk_setting) + " chunks")
            ohtm_file = chunking(ohtm_file=ohtm_file, chunk_setting=chunk_setting)

        if use_topic_modeling:
            print("Topic Modeling started with " + str(topics) + " topics")
            ohtm_file = topic_training_mallet(ohtm_file=ohtm_file, working_folder=working_folder,
                                              save_name=save_name, topics=topics, mallet_path=mallet_path,
                                              optimize_interval_mallet=optimize_interval_mallet,
                                              iterations_mallet=iterations_mallet, random_seed_mallet=random_seed,
                                              alpha=alpha, save_model=save_model, save_json=save_ohtm_file)

        if save_ohtm_file:
            save_json_function(ohtm_file=ohtm_file, working_folder=working_folder, save_name=save_name)

    if infer_new_documents:
        # The new documents to be inferred are loaded:
        infer_dic = ohtm_file_creation_function(source=source, source_path=source_path, speaker_txt=speaker_txt,
                                                    folder_as_archive=folder_as_archive)

        # The original model is loaded and all variables are set from the model.
        model_dic = load_json_function(load_file_name=trained_ohtm_file, working_folder=working_folder)
        if model_dic["settings"]["preprocessing"]["preprocessed"] == "True":
            print("Preprocessing new documents started")
            if model_dic["settings"]["preprocessing"]["stopwords_by_list"] == "True":
                by_list = True
            if model_dic["settings"]["preprocessing"]["lemmatization"] == "True":
                lemma = True
            if model_dic["settings"]["preprocessing"]["stop_words_by_particle"] == "True":
                by_particle = True
            if model_dic["settings"]["preprocessing"]["pos_filter_setting"] == "True":
                pos_filter_setting = True
            if model_dic["settings"]["preprocessing"]["stop_words_by_threshold"] == "Ture":
                by_threshold = True
            if model_dic["settings"]["preprocessing"]["stop_words_by_spacy"] == "True":
                stopword_removal_by_spacy = True
            stop_words = model_dic["stopwords"]

            # The settings are used, to preprocess the to be inferred documents the same way,
            # the original documents were preprocessed
            infer_dic = preprocessing(ohtm_file=infer_dic,
                                      allowed_postags_settings=model_dic
                                      ["settings"]["preprocessing"]["allowed_postags"],
                                      by_list=by_list, lemma=lemma, by_particle=by_particle,
                                      pos_filter_setting=pos_filter_setting,
                                      stop_words=stop_words,
                                      infer_new_documents=infer_new_documents,
                                      spacy_model=spacy_model_name,
                                      stopword_removal_by_spacy=stopword_removal_by_spacy,
                                      working_folder=working_folder)

        # The chunk settings from the original model are loaded and used:
        if model_dic["settings"]["preprocessing"]["chunked"] == "True":
            chunk_setting = model_dic["settings"]["preprocessing"]["chunk_setting"]
            print("Chunking started with " + str(chunk_setting) + " chunks")
            infer_dic = chunking(ohtm_file=infer_dic, chunk_setting=chunk_setting)

        if model_dic["settings"]["topic_modeling"]["trained"] == "True":
            print("Inferring started with " + str(topics) + " topics")

        infer_dic = topic_inferring(ohtm_file=infer_dic,
                                    model_name=trained_ohtm_file,
                                    mallet_path=mallet_path,
                                    working_folder=working_folder,
                                    topics=int(model_dic["settings"]["topic_modeling"]["topics"]),
                                    iterations_mallet=int(model_dic["settings"]["topic_modeling"]["iterations_mallet"]),
                                    random_seed_mallet=int(
                                        model_dic["settings"]["topic_modeling"]["random_seed_mallet"])
                                    )

        if save_separate_ohtm_file:
            save_json_function(ohtm_file=infer_dic,
                               working_folder=working_folder,
                               save_name=separate_ohtm_file_name + "_" + save_name + "_inferred")
            print("Inferred ohtm_file was saved")
            ohtm_file = infer_dic
        else:
            ohtm_file = combine_infer(ohtm_file=model_dic, infer_dic=infer_dic)
            save_json_function(ohtm_file=ohtm_file, working_folder=working_folder, save_name=trained_ohtm_file)
            print("Combined json was saved")

    if use_correlation:
        try:
            from interview_chronology_analysis.Narrative_o_Meter \
            import (vertical_correlation_matrix, horizontal_correlation_matrix)
            print("Topic Modeling enrichment started")
            horizontal_correlation_matrix(ohtm_file, enrich_json = True)
            vertical_correlation_matrix(ohtm_file, gross_nr_correlations_per_chunk = 2, enrich_json= True)
            vertical_correlation_matrix(ohtm_file, gross_nr_correlations_per_chunk = 3, enrich_json= True)
            vertical_correlation_matrix(ohtm_file, gross_nr_correlations_per_chunk = 4, enrich_json= True)
        except:
            print("Correlation_function will be added")

    if save_top_words:
        save_topic_words(ohtm_file=ohtm_file, working_folder=working_folder,
                         save_name=save_name, number_of_words=number_of_words)
        print("Topic Words Top " + str(number_of_words) + " was saved.")

    if print_ohtm_file:
        ohtm_file = convert_ohtm_file(ohtm_file=ohtm_file)
        print(ohtm_file)

    if print_ohtm_file_settings:
        ohtm_file = convert_ohtm_file(ohtm_file=ohtm_file)
        print(ohtm_file["settings"]["interviews"])
        print(ohtm_file["settings"]["interviews_trained"])
        print(ohtm_file["settings"]["interviews_inferred"])
        print(ohtm_file["settings"]["topic_modeling"])
        print(ohtm_file["settings"]["preprocessing"])

    if show_bar_graph_corpus:
        bar_graph_corpus(ohtm_file, show_fig=True, return_fig=False)

    if show_heatmap_corpus:
        heatmap_corpus(ohtm_file, option_selected="all", show_fig=True, return_fig=False, z_score=False)

    if show_heatmap_interview:
        heatmap_interview(ohtm_file, interview_id, show_fig=True, return_fig=False)

    if print_interview_chunk:
        print_chunk(ohtm_file, interview_id, chunk_number)

    if search_for_topics_in_chunks:
        print_chunk_with_weight_search(ohtm_file=ohtm_file, topic_search=topic_search, chunk_weight=chunk_weight)

    if search_for_topics_in_interview:
        print_chunk_with_interview_weight_search(ohtm_file=ohtm_file,
                                                 interview_id=interview_id,
                                                 topic_search=topic_search,
                                                 chunk_weight=chunk_weight)
