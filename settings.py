import ohtm
from chunking import chunking
from json_creation import json_creation
from preprocessing_functions.stopwords import remove_stopwords_by_list, remove_particles, remove_stopwords_by_threshold
from ohtm.topic_evaluation.balkendiagram import bar_dic
from ohtm.topic_evaluation.heatmap_Interview import heatmap_interview
from ohtm.topic_evaluation.heatmap_corpus import heatmap_corpus
from topic_training_new_wrapper import topic_training_mallet_new
from preprocessing import preprocessing
import pickle
import os
import json
import mallet_wrapper


mallet_path = 'C:\\mallet-2.0.8\\bin\\mallet'
os.environ['MALLET_HOME'] = 'C:\\mallet-2.0.8'
working_folder = "C:\\Users\\phili\\FAUbox\\Oral History Digital\\Topic Modeling\\main test\\github_test\\"



#stopword_file = working_folder + "german_stopwords_standard.txt"
stopword_file = working_folder + "german_stopwords_custome.txt"

# Für der Erstellung eigener JSON aus .txt oder .csv Dateien

data_path = "C:\\Users\\phili\\"

source = [
              data_path+'FAUbox\\Oral History Digital\\Interviews\\Werkstatt der Erinnerungen\\gesamt',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Archiv Zwangsarbeit\\komplett',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Archiv Deutsches Gedächtnis\\komplett',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Archiv Deutsches Gedächtnis\\ADG Charge 2',
              data_path+'FAUbox\\Oral History Digital\\Interviews\\Museum Friedland\\Bereinigt',
              data_path+'FAUbox\\Oral History Digital\\Interviews\\Flucht Vertreibung Versöhnung\\Bereinigt',
              data_path+"FAUbox\\Oral History Digital\\Interviews\\Hannah Arendt Institut Dresden\\Bereinigt",
              #   data_path + "FAUbox\\Oral History Digital\\Interviews\\test"
              ]


