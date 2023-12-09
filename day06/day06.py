data = '''
Time:        46     82     84     79
Distance:   347   1522   1406   1471
'''

def get_distance(hold_time, speed, max_time):
    return (hold_time * speed) * max(0, max_time - hold_time)

data = list(map(str.split, data.strip().split('\n')))


# PART 1
stats = list(zip(data[0][1:], data[1][1:]))

total = 1
for s in stats:
    total *= len(list(filter(lambda d: d[1] > int(s[1]), [(i, get_distance(i, 1, int(s[0]))) for i in range(int(s[0]))])))

print(total)


# PART 2
time, distance = int("".join(data[0][1:])), int("".join(data[1][1:]))

nb_possibilite = 0
prev_percent = -1
for i in range(int(time)):
    d = get_distance(i, 1, int(time))
    percent = int(i / int(time) * 100)
    
    if d > distance:
        nb_possibilite += 1

    if percent != prev_percent:
        print(f"{percent}%", i, d)
        prev_percent = percent

print(f"{nb_possibilite=}")

