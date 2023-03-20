import glob
import os.path

def identify_most_recent_file(folder_path: str, type: str='') -> str:
    file_type = r'\*' + type
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)
    return max_file

def reverseMap(givenMap: dict) -> dict:
    '''
        Faz os valores virarem keys e as keys virarem valores
    '''
    reversedMap = {}
    for key, value in givenMap.items():
        reversedMap[str(value)] = key
    return reversedMap
