import json
import files
import re
import trello_api
WHATSAPP_FOLDER = './whatsapp'

class Weights:
    def __init__(self):
        with open('./user-map.json', encoding="utf8") as f:
            self.map: dict = json.load(f)
            self.reverseWhatsMap = files.reverseMap(self.map.get('whatsapp'))
            self.reverseTrello = files.reverseMap(self.map.get('trello'))
            print('reverseTrello')
            print(self.reverseTrello)
            # self.reverseWhatsMap = {}
            # for key, value in self.map.get('whatsapp').items():
            #     self.reverseWhatsMap[str(value)] = key
        self.whatsappFile = files.identify_most_recent_file(WHATSAPP_FOLDER, 'txt')
    
    def weight_whatsapp(self):
        print('Running whatsapp weights...')
        with open(self.whatsappFile, encoding="utf8") as f:
            whatsRanking = {}
            for keys in self.map.get('whatsapp').keys():
                whatsRanking[keys] = 0
            for line in f.readlines():
                pattern = r"^\d{4}\/\d{2}\/\d{2} (?:2[0-3]|[01]?\d):[0-5]\d - .*?:"
                dateAndName = re.compile(pattern).search(line.strip())
                if (dateAndName):
                    message = re.sub(pattern, '', line).split()
                    dateAndName = dateAndName.group()
                    name = re.compile(r" - .*:").search(dateAndName).group().replace(' - ', '').replace(':', '')
                    nickname = self.reverseWhatsMap[name]
                    whatsRanking[nickname] += len(message)
            return whatsRanking
    
    def weight_trello(self):
        trelloRanking = {}
        trelloPointedActionsMap: dict = trello_api.get_user_actions(self.reverseTrello)
        for key, actions in trelloPointedActionsMap.items():
            trelloRanking[key] = actions['cardsCreated'] * 30 + actions['commentsCreated'] * 20 
        return trelloRanking
