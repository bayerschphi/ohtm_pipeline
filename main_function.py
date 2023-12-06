from settings import *

source = [
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Werkstatt der Erinnerungen\\csv_test',
              data_path+'FAUbox\\Oral History Digital\\Interviews\\Archiv Zwangsarbeit\\test',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Archiv Deutsches Gedächtnis\\komplett',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Archiv Deutsches Gedächtnis\\ADG Charge 2',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Museum Friedland\\Bereinigt',
              # data_path+'FAUbox\\Oral History Digital\\Interviews\\Flucht Vertreibung Versöhnung\\Bereinigt',
              # data_path+"FAUbox\\Oral History Digital\\Interviews\\Hannah Arendt Institut Dresden\\Bereinigt"
              ]

if __name__ == "__main__":

    top_dic = json_creation(working_folder, source, name = "ohne_preprocess", Save = True)
    top_dic = preprocessing(top_dic, stopword_file)
    top_dic = chunking(top_dic, chunk_setting = 50)
    top_dic = topic_training_mallet(top_dic, mallet_path, topics=80, chunking=True)
    print(top_dic)