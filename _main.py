import time
import random, json
import _genetic

'''
CODE USED TO ADD CORPUSES : 
from collections import Counter
for corpus in ["discord", "english-1k", "english-200", "keymash", "mt", "my_discord"]:
    with open(f"corpus/{corpus}.txt", "r", encoding="utf-8", errors="replace") as file:
        text = file.read()

    text = text.replace("\n", " ")
    text = text.lower()


    text = ''.join([char for char in text if char in allowed])

    trigrams = []

    for i in range(len(text) - 2):
        group = text[i:i + 3]
        trigrams.append(group)

    result = {}
    for item, count in Counter(trigrams).items():
        result.setdefault(count, []).append(item)

    result = dict(sorted(result.items(), reverse=True))

    with open(f"corpus2/{corpus}.json", "w") as file:
        json.dump(result, file, indent=4)

exit()
'''

def evaluate(layouts, corpus="english-200"):
    with open(f"better_corpus/{corpus}.json", "r") as file:
        result = json.load(file)

    allowed = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', ',','.','?',';', " ", "!", "'", ":", '"']
    layoutscore = []
    heatmap = [
    [9.9, 2.1, 2.0, 3.0, 4.6, 4.6, 3.0, 2.0, 2.1, 9.9], 
    [1.6, 1.3, 1.1, 1.0, 3.4, 3.4, 1.0, 1.1, 1.3, 1.6], 
    [4.8, 4.8, 3.8, 1.2, 4.0, 4.0, 1.2, 3.8, 4.8, 4.8]]
    
    corpus_count = 2

    #USE THIS TO CUSTOMIZE THE PROGRAM:
    weights = {
        "SFB":        15.0, 
        "BadSfb":     30.0, 
        "SFS":        3.75, 
        "BadSfs":     7.5, 
        "Scissors":   0.0, 
        "BadScis":    30.0, 
        "Redirects":  1.2, 
        "BadRed"   :  3.0, 
        "Inrolls":    -10.0, 
        "Trinroll":   -10.0 * 1.5, 
        "Outrolls":   -5.0, 
        "Trioutroll": -5.0 * 1.5, 
        "Alt":        -0.4, 
        "LSB":        1.0
    }

    for layout in layouts:
        stats = {
            "SFB":        0.0, 
            "BadSfb":     0.0, 
            "SFS":        0.0, 
            "BadSfs":     0.0, 
            "Scissors":   0.0, 
            "BadScis":    0.0, 
            "Redirects":  0.0, 
            "BadRed":     0.0, 
            "Inrolls":    0.0, 
            "Trinroll":   0.0, 
            "Outrolls":   0.0, 
            "Trioutroll": 0.0, 
            "Alt":        0.0, 
            "LSB":        0.0
        }

        movement = 0
        pos = {' ': {'row': None,'collumn': None}}

        for letter in allowed:
            for i, row in enumerate(layout):
                if letter in row:
                    pos[letter] = {'row': i, 'collumn': row.index(letter)}

        for amount in result:
            for trigram in result[amount]:
                amount = int(amount)
                corpus_count += amount
                row0, row1, row2 = [
                    pos[trigram[0]].get('row') if trigram[0] in pos else None,
                    pos[trigram[1]].get('row') if trigram[1] in pos else None,
                    pos[trigram[2]].get('row') if trigram[2] in pos else None
                ]
                col0, col1, col2 = [
                    pos[trigram[0]].get('collumn') if trigram[0] in pos else None,
                    pos[trigram[1]].get('collumn') if trigram[1] in pos else None,
                    pos[trigram[2]].get('collumn') if trigram[2] in pos else None
                ]

                # SFS
                if col2 is not None:
                    movement += heatmap[row2][col2] * amount

                    if col0 is not None and trigram[0] != trigram[2]:
                        if col0 == col2 or (col0 in [3, 4] and col2 in [3, 4]) or (col0 in [5, 6] and col2 in [5, 6]):
                            if row0 == 1 or row2 == 1: stats['SFS'] += amount
                            else: stats['BadSfs'] += amount

                    # Alternates
                    if col1 is not None:
                        if (col1 > 4) != (col2 > 4): 
                            if col0 is not None and (col1 > 4) != (col0 > 4):
                                stats["Alt"] += amount
                        else:
                            # LSB
                            if (col1, col2) in [(4, 2), (2, 4), (5, 7), (7, 5)]: stats["LSB"] += amount  

                            # Redirects
                            if (col0 is not None and (col0 > 4) == (col1 > 4) and col2 != col0) and ((col2 > col1 and col1 < col0) or (col2 < col1 and col1 > col0)):
                                if col2 not in [3, 4, 5, 6] and col1 not in [3, 4, 5, 6] and col0 not in [3, 4, 5, 6]:
                                    stats["BadRed"] += amount
                                else:
                                    stats["Redirects"] += amount
                                        
                            #Scissors
                            if (col1 in [col2 + 1, col2 - 1]) and (row1, row2) in [(0, 2), (2, 0)]:
                                if (col1, col2) in [(2, 3), (3, 2), (6, 7), (7, 6)] : stats["Scissors"] += amount
                                else: stats["BadScis"] += amount

                            # SFB
                            if trigram[1] != trigram[2] and (col1 == col2 or (col1, col2) in [(3, 4), (4, 3), (5, 6), (6, 5)]):
                                if row1 == 1 or row2 == 1: stats['SFB'] += amount
                                else: stats['BadSfb'] += amount
                            
                            # ROLLS:
                            elif row1 == row2 and col2 not in [4, 5] and col1 not in [4, 5]:
                                # LEFT TO RIGHT
                                if col2 - 1 == col1:
                                    if col2 <= 4:
                                        if col0 not in [4, 5] and col1 - 1 == col0 and row0 == row1: 
                                            stats["Trinroll"] += amount
                                            
                                        elif col0 is not None and (col0 > 4) != (col2 > 4): 
                                            stats["Inrolls"] += amount
                                    else:
                                        if col0 not in [4, 5] and col1 - 1 == col0 and row0 == row1: 
                                            stats["Trioutroll"] += amount

                                        elif col0 is not None and (col0 > 4) != (col2 > 4): 
                                            stats["Outrolls"] += amount

                                # RIGHT TO LEFT
                                elif col2 + 1 == col1:
                                    if col2 <= 4:
                                        if col0 not in [4, 5] and col1 + 1 == col0 and row0 == row1: 
                                            stats["Trioutroll"] += amount

                                        elif col0 is not None and (col0 > 4) != (col2 > 4): 
                                            stats["Outrolls"] += amount
                                    else:
                                        if col0 not in [4, 5] and col1 + 1 == col0 and row0 == row1: 
                                            stats["Trinroll"] += amount

                                        elif col0 is not None and (col0 > 4) != (col2 > 4): 
                                            stats["Inrolls"] += amount
        
        
        for j in stats:
            movement += stats[j]*weights[j]

        #if sorted(layout[2][7:]) != ",.?" and layout[0][7:] != "ou;": 
        #    movement += 500000

        layoutscore.append([layout, round(movement, 1)])

    if len(layouts) == 1: 
        return stats, weights, corpus_count, movement

    sorted_data = sorted(layoutscore, key=lambda x: x[1])[:30]
    return sorted_data

def top():
    file = open("data/data15.txt", "r")
    info = file.read().split("\n")

    layouts = []
    past = []

    for i in info:
        if info.index(i)%2:
            pass
        elif i!="":
            if i not in past:
                past.append(i)
                layouts.append(eval(i))          

    
    counter = [0, 0]
    evaluated = evaluate(layouts)

    homerows = []
    for i in evaluated:
        
        if counter[0] == evaluated.index(i) and [i[0][1][:4], i[0][1][6:]] not in homerows:
            print("\n")
            print(i[0])
            print(i[1])
            homerows.append([i[0][1][:4], i[0][1][6:]])
            counter[1] += 1
        counter[0] += 1
        if counter[1] == 5:
            break

    print("The program ran for", round(time.time()-start, 3), "Seconds")
    evaluate([evaluated[0][0]])
    exit()

def check(layout):
    charcount = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0, ',': 0, '.': 0, ';':0, '?':0}
    for i in layout:
        for j in i:
            charcount[j] += 1
    for i in charcount:
        if charcount[i]!=1:
            print(i, charcount[i])
    print(layout, len(layout[0]), len(layout[1]), len(layout[2]))
    exit()

def generate():
    layouts = []
    for _ in range(1000):
        letters = ['b', 'd', 'f', 'g', 'z', 'k', 'm', 'p', 'v', 'w', 'c', 'o', 'u']
        common = ['n', 'l', 'y', 's', 'r']

        random.shuffle(letters)
        random.shuffle(common)

        right = [common[2], 'a', 'e', 'i']
        left = [common[0], common[1], 't', 'h']

        layout = [
            ''.join(['q', letters[9], letters[10], letters[0]] + letters[1:4] + [letters[11], letters[12], ';']),  # First row
            ''.join(left + letters[4:6] + right),  # Second row
            ''.join(letters[6:9] + [common[3], 'x', 'j', common[4]] + [',', '.', '?'])  # Third row
        ]
        layouts.append(layout)

        #check(layout)

    return layouts

start = time.time()

if __name__ == "__main__":
    for iteration in range(60):
        round1 = evaluate(generate())
        print("\n")
        print(round1[:3])
        raw = [sublist[0] for sublist in round1]

        past = [0, 1]
        for _ in range(2):
            dna = _genetic.smartdna(raw)
            round2 = evaluate(dna)
            past.append(round2[:3])
            print(round2[:3])

            raw = [sublist[0] for sublist in round2]

        layout = round2[0][0]
        new = evaluate(_genetic.bigmix(layout))[:3]
        print(f"\nSwtiching from smartdna to bigmix\n\n{new}")
        
        while True:
            new1 = evaluate(_genetic.bigmix(new[0][0]))[:3]
            print(new1)
            if new[0][1] <= new1[0][1]:
                file = open("data/data15.txt", "a")
                file.write(f'\n\n\n["{new[0][0][0]}", "{new[0][0][1]}", "{new[0][0][2]}"]')
                file.write(f"\n{new[0][1]}")
                break
            new = new1

        print(f"{iteration + 1}/30")

    print(round(time.time()-start, 2))