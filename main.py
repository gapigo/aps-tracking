import weights
import pandas as pd
import files

compute = weights.Weights()

ranking = {}
whatsRanking = compute.weight_whatsapp()
trelloRanking = compute.weight_trello()
#files.generate_cache([whatsRanking, whatsRanking])
classifications = [(whatsRanking, 30), (trelloRanking, 70)]

totalWeights = 0
for classification, weight in classifications:      
    totalWeights += weight
    for player in classification.keys():
        maxValue = max(whatsRanking.values())
        playerPoints = classification[player] 
        if (not ranking.get(player)):
            ranking[player] = 0
        ranking[player] += playerPoints * weight

for player, playerPoints in ranking.items():
    ranking[player] = playerPoints / totalWeights

# print(ranking)
ranking = dict(sorted(ranking.items(), key=lambda item: item[1], reverse=True))
df = pd.DataFrame({'Nome':ranking.keys(), 'Pontos':ranking.values()})
df = df[df['Nome'] != 'gapigo']
df['Posição'] = range(1, len(df) + 1)
df.reset_index()
print(df.to_string(index=False))
