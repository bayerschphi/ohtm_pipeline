import gensim
import pickle
import os
from topic_evaluation import *
from topic_training import *
from json_creation import *
from preprocessing_functions import *
from preprocessing import *
from chunking import *




mallet_path = 'C:\\mallet-2.0.8\\bin\\mallet'
os.environ['MALLET_HOME'] = 'C:\\mallet-2.0.8'
working_folder = "C:\\Users\\phili\\FAUbox\\Oral History Digital\\Topic Modeling\\main test\\github_test\\"

data_path = "C:\\Users\\phili\\"

stopword_file = working_folder + "german_stopwords_full_BE_MOD Topics - Kopie.txt"

save_doc = True



