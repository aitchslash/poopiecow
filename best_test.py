import pickle

top_scores = [[1, 4, 13, 3000],
                [26, 4, 13, 2800], 
                [1, 26, 13, 500],
                [1, 4, 26, 300],
                [1, 1, 1, 0]]
'''
ts2 = "1,4,13,3000/27,4,13,2800/1,27,13,2600/1,4,27,2400/1,1,1,2200"

with open("high_scores.txt", "w") as out_file:
    out_file.write(ts2)

atad = ''
with open('high_scores.txt', 'r') as hs:
    atad = hs.readline()

scores_array = atad.split('/')
sa2 = []
for score in scores_array:
    score = score.split(',')
    for item in score:
        item = int(item)
    sa2.append(score)
'''
with open('pickled_scores', 'wb') as pt:
    pickle.dump(top_scores, pt, protocol=2)

with open('pickled_scores', 'rb') as pt:
    foo = pickle.load(pt)
