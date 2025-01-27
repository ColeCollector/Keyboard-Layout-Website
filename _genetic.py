from itertools import combinations

def dna(layouts):
    allnew = []
    combos = list(combinations(layouts, 2))
    
    for i in combos:
        #print(i[0],i[1])
        first = layouts.index(i[0])
        second = layouts.index(i[1])

        if layouts[first] not in allnew:
            allnew.append(layouts[first])

        if layouts[second] not in allnew:
            allnew.append(layouts[second])

        for x in range(4,7):

            new = []
            
            new.append(layouts[first][0][:x])
            new.append(layouts[first][1][:x])
            new.append(layouts[first][2][:x])

            number = 0
            for collumn in range(10):
                for row in range(3):
                    if layouts[second][row][collumn] not in new[0]+new[1]+new[2]:
                        new[number]+=layouts[second][row][collumn]
                        number+=1
                        if number == 3:
                            number = 0
            
            assert [len(new[0]),len(new[1]),len(new[2])] == [10,10,10]
            if new not in allnew:
                allnew.append(new)

        #layouts.pop(first)
        #layouts.pop(second-1)
        #print(layouts)
    return allnew

def smartdna(layouts):
    allnew = []
    combos = list(combinations(layouts, 2))
    
    for i in combos:
        #print(i[0],i[1])
        first = layouts.index(i[0])
        second = layouts.index(i[1])

        if layouts[first] not in allnew:
            allnew.append(layouts[first])

        if layouts[second] not in allnew:
            allnew.append(layouts[second])

        for x in range(4,6):

            new = []
            
            new.append(layouts[first][0][:x])
            new.append(layouts[first][2][:x])

            number = 0
            for collumn in range(10):
                for row in range(3):
                    if layouts[second][row][collumn] not in new[0]+layouts[first][1]+new[1]:
                        new[number]+=layouts[second][row][collumn]
                        number+=1
                        if number == 2:
                            number = 0
            
            #assert [len(new[0]),len(layouts[first][1]),len(new[1])] == [10,10,10]

            if [new[0]]+[layouts[first][1]]+[new[1]] not in allnew:
                allnew.append([new[0]]+[layouts[first][1]]+[new[1]])

    return allnew

def scramble(layout):
    switches = []

    #switching across the first row
    for i in range(10):
        for j in range(i + 1, 10):
            switched_string = list(layout[0])
            switched_string[i], switched_string[j] = switched_string[j], switched_string[i]
            switches.append([''.join(switched_string),layout[1],layout[2]])

    switched_string = list(layout[1])
    switched_string[4], switched_string[5] = switched_string[5], switched_string[4]
    switches.append([layout[0],''.join(switched_string),layout[2]])

    #switching across the third row
    for i in range(10):
        for j in range(i + 1, 10):
            switched_string = list(layout[2])
            switched_string[i], switched_string[j] = switched_string[j], switched_string[i]
            switches.append([layout[0],layout[1],''.join(switched_string)])
        
    #switching between first and third row
    for i in range(10):
        for j in range(10):
            new_str1 = layout[0][:i] + layout[2][j] + layout[0][i+1:]
            new_str2 = layout[2][:j] + layout[0][i] + layout[2][j+1:]
            switches.append([new_str1,layout[1],new_str2])
    
    #switching between the first and second row
    for i in range(10):
        for j in range(4,7):
            new_str1 = layout[0][:i] + layout[1][j] + layout[0][i+1:]
            new_str2 = layout[1][:j] + layout[0][i] + layout[1][j+1:]
            switches.append([new_str1,new_str2,layout[2]])

    #switching between the second and third row
    for i in range(4,7):
        for j in range(10):
            new_str1 = layout[1][:i] + layout[2][j] + layout[1][i+1:]
            new_str2 = layout[2][:j] + layout[1][i] + layout[2][j+1:]
            switches.append([layout[0],new_str1,new_str2])

    i = 0
    for j in range(10):
        new_str1 = layout[1][:i] + layout[2][j] + layout[1][i+1:]
        new_str2 = layout[2][:j] + layout[1][i] + layout[2][j+1:]
        switches.append([layout[0],new_str1,new_str2])
    
    for i in range(10):
        j = 0
        new_str1 = layout[0][:i] + layout[1][j] + layout[0][i+1:]
        new_str2 = layout[1][:j] + layout[0][i] + layout[1][j+1:]
        switches.append([new_str1,new_str2,layout[2]])
        
    return switches


    """
    allnew = []
    for _ in range(5):
        shuffled_layout = [
            ''.join(random.sample(layout[0], len(layout[0]))),
            layout[1],
            ''.join(random.sample(layout[2], len(layout[2])))
        ]
        allnew.append(shuffled_layout)
    return allnew
    """

def bigmix(layout):
    switches = []
    vowel = ['a','e','i','o','u']

    def vowels(addition):
        counter = 0
        for i in addition[1][6:]:
            if i in vowel:counter+=1

        for i in addition[0][6:]:
            if i in vowel:counter+=1

        if counter>=5:
            switches.append(addition)


    #switching across the first row
    for i in range(10):
        for j in range(i + 1, 10):
            switched_string = list(layout[0])
            switched_string[i], switched_string[j] = switched_string[j], switched_string[i]
            vowels([''.join(switched_string),layout[1],layout[2]])

    #switching across the second row
    for i in range(10):
        for j in range(i + 1, 10):
            switched_string = list(layout[1])
            switched_string[i], switched_string[j] = switched_string[j], switched_string[i]
            vowels([layout[0],''.join(switched_string),layout[2]])

    #switching across the third row
    for i in range(10):
        for j in range(i + 1, 10):
            switched_string = list(layout[2])
            switched_string[i], switched_string[j] = switched_string[j], switched_string[i]
            vowels([layout[0],layout[1],''.join(switched_string)])
        
    #switching between first and third row
    for i in range(10):
        for j in range(10):
            new_str1 = layout[0][:i] + layout[2][j] + layout[0][i+1:]
            new_str2 = layout[2][:j] + layout[0][i] + layout[2][j+1:]
            vowels([new_str1,layout[1],new_str2])
    
    #switching between the first and second row
    for i in range(10):
        for j in range(10):
            new_str1 = layout[0][:i] + layout[1][j] + layout[0][i+1:]
            new_str2 = layout[1][:j] + layout[0][i] + layout[1][j+1:]
            vowels([new_str1,new_str2,layout[2]])

    #switching between the second and third row
    for i in range(10):
        for j in range(10):
            new_str1 = layout[1][:i] + layout[2][j] + layout[1][i+1:]
            new_str2 = layout[2][:j] + layout[1][i] + layout[2][j+1:]
            vowels([layout[0],new_str1,new_str2])

    return switches

if __name__ == "__main__":
    number = 0
    for i in bigmix(['xylbmjwouq', 'rsthgvnaei', ',;cdfkpz?.']):
        print(i,number+1)
        number +=1