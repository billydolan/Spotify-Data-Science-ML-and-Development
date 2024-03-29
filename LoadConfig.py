import glob
import pandas as pd

#Configuration 
def load_config():
    #need to add a file path correction here to automate finding the folder for the incorrect /\
    FolderLocation = input(r"Please Input the file path for the folder of the Long Term Listening Logs")
    ListeningLogLongTerm = pd.DataFrame()
    NamingConvention = 'Streaming_History_Audio_202*_*.json'  #This matches any file that starts with Streaming_History_Audio_2020_ and use the * as a wildcard operator to match the number. 
    FilePaths = glob.glob(f'{FolderLocation}/{NamingConvention}')
    for FilePath in FilePaths:
        LongTermJsonRead = pd.read_json(FilePath)
        ListeningLogLongTerm = pd.concat([ListeningLogLongTerm, LongTermJsonRead])
    return ListeningLogLongTerm      
        