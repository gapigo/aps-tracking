import requests
import json
import files
from dotenv import dotenv_values
env = dotenv_values(".env")


def get_comments_in_a_card(card_id: str) -> list:
    url = f"https://api.trello.com/1/cards/{card_id}/actions"

    headers = {
    "Accept": "application/json"
    }

    query = {
        'key': env['TRELLO_API_KEY'],
        'secret': env['TRELLO_API_TOKEN'],
        'filter': 'commentCard'
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )
    
    return json.loads(response.text)
    

def get_cards_in_a_board(board_id: str) -> list:
    url = f"https://api.trello.com/1/boards/{board_id}/cards/"

    headers = {
    "Accept": "application/json"
    }

    query = {
        'key': env['TRELLO_API_KEY'],
        'secret': env['TRELLO_API_TOKEN']
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )
    return json.loads(response.text)    
    
def get_card_updates(board_id:str, card_id: str) -> list:
    url = f"https://api.trello.com/1/cards/{card_id}/actions"
    
    headers = {
    "Accept": "application/json"
    }

    query = {
        'key': env['TRELLO_API_KEY'],
        'secret': env['TRELLO_API_TOKEN'],
        'filter': 'createCard,updateCard',
        'fields': 'idMemberCreator',
        'idModels': card_id
    }
    
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )
    return json.loads(response.text)

def get_user_actions(reversedTrelloMap: dict):
    boards = [
        '640df89476a920c927196647'
    ]
    
    for key, value in reversedTrelloMap.items():
        reversedTrelloMap[key] = {'name': value, 'cardsCreated': 0, 'commentsCreated': 0}
    
    index = 0
    for board_id in boards:
        cards = get_cards_in_a_board(board_id)
        for card in cards:
            cardId = card.get('id')
            print('Analysing card ' + cardId + '...')
            cardUpdates = get_card_updates(board_id, cardId)
            cardCreator = ''
            if (cardUpdates):
                cardCreator = cardUpdates[-1].get('idMemberCreator')
            if reversedTrelloMap.get(cardCreator):
                reversedTrelloMap[cardCreator]['cardsCreated'] += 1
                
            commentsNumber = card.get('badges').get('comments')
            if commentsNumber > 0:
                comments = get_comments_in_a_card(cardId)
                for comment in comments:
                    commentCreator = comment.get('idMemberCreator')
                    if reversedTrelloMap.get(commentCreator):
                        reversedTrelloMap[commentCreator]['commentsCreated'] += 1
            index += 1
            if (index >= 5):
                break
    # trelloMap = files.reverseMap(reversedTrelloMap)
    trelloMap = {}
    for value in reversedTrelloMap.values():
        trelloMap[value['name']] = {'cardsCreated': value['cardsCreated'], 'commentsCreated': value['commentsCreated']}
    print(trelloMap)
            
# get_user_actions()
