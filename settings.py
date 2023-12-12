import gensim
import pickle
import os
from topic_evaluation import *
from topic_training import *
from json_creation import *
from preprocessing_functions import *
from topic_training_new_wrapper import *
from preprocessing import *
from chunking import *
import json
import mallet_wrapper


mallet_path = 'C:\\mallet-2.0.8\\bin\\mallet'
os.environ['MALLET_HOME'] = 'C:\\mallet-2.0.8'
working_folder = "C:\\Users\\phili\\FAUbox\\Oral History Digital\\Python\\Project\\bayerschmidt_topic_modeling\\Oral History Topic Modeling\\"



#stopword_file = working_folder + "german_stopwords_standard.txt"
stopword_file = working_folder + "german_stopwords_custome.txt"

# Für der Erstellung eigener JSON aus .txt oder .csv Dateien

data_path = "C:\\Users\\phili\\"

source = [
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Werkstatt der Erinnerungen\\gesamt',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Archiv Zwangsarbeit\\Bereinigt',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Archiv Deutsches Gedächtnis\\komplett',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Archiv Deutsches Gedächtnis\\ADG Charge 2',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Museum Friedland\\Bereinigt',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Flucht Vertreibung Versöhnung\\Bereinigt',
              # data_path+"FAUbox\\Oral History Digital\\Interviews\\Hannah Arendt Institut Dresden\\Bereinigt",
                data_path + "FAUbox\\Oral History Digital\\Interviews\\test"
              ]


