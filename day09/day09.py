import os

test_data = '''
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''

data = test_data
data = open(os.path.dirname(__file__) + "/data.txt").read()

data_lines = data.strip().split("\n")

history = [[int(n) for n in l.split()] for l in data_lines]

extrapolated_values_post = []
extrapolated_values_pre = []

for curr_history_line in history:
    history_line_delta_list = [curr_history_line]

    while not all([v == 0 for v in curr_history_line]):
        history_line_delta_list.append([curr_history_line[i] - curr_history_line[i-1] for i in range(1, len(curr_history_line))])
        curr_history_line = history_line_delta_list[-1]

    for i in range(len(history_line_delta_list)-2, -1, -1):
        history_line_delta_list[i].append(history_line_delta_list[i][-1] + history_line_delta_list[i+1][-1])
        history_line_delta_list[i].insert(0, history_line_delta_list[i][0] - history_line_delta_list[i+1][0])

    extrapolated_values_pre.append(history_line_delta_list[0][0])
    extrapolated_values_post.append(history_line_delta_list[0][-1])

print(sum(extrapolated_values_pre))
print(sum(extrapolated_values_post))
