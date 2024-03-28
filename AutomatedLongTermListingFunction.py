import glob
import pandas as pd

#Configuration 
def load_config():
    #need to add a file path correction here to automate finding the folder for the incorrect /\
    FolderLocation = input("Please Input the file path for the folder of the Long Term Listening Logs")
    FolderLocation = FolderLocation.replace("\\", "\\")
    ListeningLogLongTerm = pd.DataFrame()
    NamingConvention = 'Streaming_History_Audio_2020_*.json'  #This matches any file that starts with Streaming_History_Audio_2020_ and use the * as a wildcard operator to match the number. 
    FilePaths = glob.glob(f'{FolderLocation}/{NamingConvention}')
    for FilePath in FilePaths:
        LongTermJsonRead = pd.read_json(FilePath)
        ListeningLogLongTerm = pd.concat([ListeningLogLongTerm, LongTermJsonRead])
    return ListeningLogLongTerm      
        



# rename.py
def RenameAndRemoveColumns(ListeningLogLongTerm): #Renames Columns to more functional names, removes personal information columns 
    LLLT_DataRemove = ListeningLogLongTerm
    LLLT_DataRemove.rename(columns={'ts': 'Time Stamp', 'username' : 'Username','platform' : 'Platform' , 'ms_played' : 'Minutes Played', 'master_metadata_track_name' : 'Track Name' \
                                    ,'master_metadata_album_artist_name' : 'Artist Name'\
                                          , 'master_metadata_album_album_name' : 'Album Name', 'reason_start' : 'Reason Started', \
                                              'reason_end' : 'Reason Ended', 'shuffle' : 'Shuffle', 'skipped': 'Skipped', 'offline':'Offline'\
                                                ,'offline_timestamp' : 'Offline Timestamp' , 'incognito_mode' : 'Incognito Mode'}, inplace=True)
    LLLT_DataRemove = ListeningLogLongTerm.pd.drop(['user_agent_decrypted','ip_addr_decrypted', 'episode_name' , 'episode_show_name'	, 'spotify_episode_uri' , 'spotify_track_uri'], axis = 1)
    return LLLT_DataRemove


# correct.py
def correct_numeric_values(LLLT_DataRemove):
    LLLT_DataCorrect = LLLT_DataRemove
    #Convert ms_played to an integer, then convert to minutes from milliseconds
    LLLT_DataCorrect['Minutes Played'] = LLLT_DataCorrect['Minutes Played'].astype(int)
    LLLT_DataCorrect['Minutes Played'] = LLLT_DataCorrect['Minutes Played'] / 60000 
    return LLLT_DataCorrect
    

# cleanse.py
def cleanse_data(LLLT_DataCorrect):
    LLLT_DataCleanse = LLLT_DataCorrect
    WindowsAppStringLim = 11
    DataRow = () 
    for row in LLLT_DataCleanse:
        if LLLT_DataCleanse['Platform'][row] == "web_player windows 10;chrome **.*.****.***;desktop": 
            LLLT_DataCleanse['Platform'][row] = "Windows 10 Web Player"
        elif LLLT_DataCleanse['Platform'][row] == "Windows 10 (10.0.18362; x64; AppX)": 
            LLLT_DataCleanse['Platform'][row] = DataRow
            # Truncates Windows 10 app lines
            LLLT_DataCleanse['Platform'][row] = DataRow(DataRow, WindowsAppStringLim)
        elif LLLT_DataCleanse['Platform'][row] == "iOS **.*.* (iPhone11,2)":
            LLLT_DataCleanse['Platform'][row] = "iPhone 11"
        elif LLLT_DataCleanse['Platform'][row] == "iOS **.*.* (iPhone13,3)":
            LLLT_DataCleanse['Platform'][row] = "iPhone 13"
        elif LLLT_DataCleanse['Platform'][row] == "web_player windows 10;microsoft edge ***.*.****.**;desktop":
            LLLT_DataCleanse['Platform'][row] = "Windows 10 Web Player"
        elif LLLT_DataCleanse['Platform'][row] == "Partner roku_tv tcl;8105x;4916bf2fd1c54ff2bace038314d21f39;;tpapi":
            LLLT_DataCleanse['Platform'][row] = "Roku TV"
        else: 
            return LLLT_DataCleanse['Platform'][row]
    return LLLT_DataCleanse

       

           
    
     
# The below code would be used if each file is seperate
# # main.py
# from config import load_config
# from rename import rename_columns
# from correct import correct_numeric_values
# from cleanse import cleanse_data

def main():
    ListeningLogLongTerm = load_config()
    
    # Rename and remove columns
    LLLT_DataRemove = RenameAndRemoveColumns(ListeningLogLongTerm)
    
    # Correct numeric values
    LLLT_DataCorrect = correct_numeric_values(LLLT_DataRemove)
    
    # Cleanse the data
    LLLT_DataCleanse = cleanse_data(LLLT_DataCorrect)
    
    # Now LLLT_DataCleanse contains the final cleansed data
    return LLLT_DataCleanse

# Call the main function to execute the workflow
final_data = main()

if __name__ == "__main__":
    main()
