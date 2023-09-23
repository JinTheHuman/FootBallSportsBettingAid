import copy
from constants import STATNAMES


# Prints Stats of a game prettily
def pretty_print_stats(gameStats):
    for idx in range(0, len(STATNAMES), 2):
        h = str(gameStats[idx])
        a = str(gameStats[idx + 1])

        print(
            f"{idx:{2}} {STATNAMES[idx]:{10}}{h:{30}} {idx + 1:{2}} {STATNAMES[idx+1]:{10}}{a}"
        )


# Averages stats from multiple games
def get_average(statsList):
    totalStats = copy.deepcopy(statsList[0])
    for stats in statsList[1:]:
        for idx, stat in enumerate(stats):
            totalStats[idx] += stat

    length = len(statsList)

    averageStats = [round(x / length, 1) for x in totalStats]
    return averageStats


# Makes stats whole numbers and also makes total shots and things add up
def clean_stats(stats):
    cleanStats = []
    for idx, stat in enumerate(stats):
        # if idx not in [0, 1, 10, 11, 18, 19, 20, 21]:
        #     cleanStats.append(round(stat))

        cleanStats.append(stat)

    cleanStats[2] = cleanStats[4] + cleanStats[6] + cleanStats[8]
    cleanStats[3] = cleanStats[5] + cleanStats[7] + cleanStats[9]
    return cleanStats


def make_sum_100(num1, num2):
    # Calculate the sum of the two numbers
    total = num1 + num2

    # Calculate the ratio of each number to the sum
    ratio1 = num1 / total
    ratio2 = num2 / total

    # Calculate the new values that sum up to 100
    new_num1 = round(ratio1 * 100, 1)
    new_num2 = round(ratio2 * 100, 1)

    # Adjust one of the numbers to make the sum exactly 100
    if new_num1 + new_num2 != 100:
        if new_num1 > new_num2:
            new_num1 -= new_num1 + new_num2 - 100
        else:
            new_num2 -= new_num1 + new_num2 - 100

    return new_num1, new_num2


def get_weighted_average(statsList, weights):
    totalStats = copy.deepcopy(statsList[0])

    totalStats = [stat * weights[0] for stat in totalStats]
    curr_weight_index = 1
    for stats in statsList[1:]:
        for idx, stat in enumerate(stats):
            totalStats[idx] += stat * weights[curr_weight_index]
        curr_weight_index += 1

    length = sum(weights)

    averageStats = [round(x / length, 1) for x in totalStats]
    return averageStats


def calculate_weights(h_played_against, a_played_against):
    h_weights = [1, 1, 1, 1, 1]
    a_weights = [1, 1, 1, 1, 1]

    index_pairs = []

    for i in range(len(h_played_against)):
        for j in range(len(a_played_against)):
            if h_played_against[i] == a_played_against[j]:
                if (j, i) not in index_pairs:
                    index_pairs.append((i, j))

    print(index_pairs)

    for h_index, a_index in index_pairs:
        h_weights[h_index] = 3
        a_weights[a_index] = 3

    return h_weights, a_weights


# Played Same Team     Make average for that game more weighted
# Played similar level team      Make average for that game little more weighted
# Played Harder teams   Give better stats
# Played easier teams     give worse stats
