from bs4 import BeautifulSoup
import requests
import numpy as np
from DataModels.pigeon_data_model import make_away_predictions
from DataModels.pigeon_data_model import make_home_predictions
from scraper_helper import (
    get_table_pos,
    get_curr_week_fixtures,
    get_stats_link,
    get_last_five_game_stats,
)
from processing_helper import (
    calculate_weights,
    clean_stats,
    get_average,
    get_weighted_average,
    pretty_print_stats,
    make_sum_100,
)
from constants import TEAMNAMES
import itertools


def make_prediction(homeTeam, awayTeam):
    h_fixtures, h_played_against = get_last_five_game_stats(homeTeam)
    a_fixtures, a_played_against = get_last_five_game_stats(awayTeam)

    h_weights, a_weights = calculate_weights(h_played_against, a_played_against)

    # thomeStats = get_average(h_fixtures)
    # tawayStats = get_average(a_fixtures)

    # tlists = [thomeStats, tawayStats]
    # tgameStats = [val for tup in zip(*tlists) for val in tup]

    # tgameStats[0], tgameStats[1] = make_sum_100(tgameStats[0], tgameStats[1])
    # tgameStats[20], tgameStats[21] = make_sum_100(tgameStats[20], tgameStats[21])

    homeStats = get_weighted_average(h_fixtures, h_weights)
    awayStats = get_weighted_average(a_fixtures, a_weights)

    lists = [homeStats, awayStats]
    gameStats = [val for tup in zip(*lists) for val in tup]

    gameStats[0], gameStats[1] = make_sum_100(gameStats[0], gameStats[1])
    gameStats[20], gameStats[21] = make_sum_100(gameStats[20], gameStats[21])

    # Printing Stats
    # print("UNWEIGHTED AVERAGE")
    # pretty_print_stats(tgameStats)

    gameStats = clean_stats(gameStats)
    print("WEIGHTED AVERAGE")
    pretty_print_stats(gameStats)

    home_dataset = [x for i, x in enumerate(gameStats) if i != 23]
    away_dataset = [x for i, x in enumerate(gameStats) if i != 22]

    homeGoals = make_home_predictions([np.array(home_dataset).reshape(1, -1)])
    awayGoals = make_away_predictions([np.array(away_dataset).reshape(1, -1)])

    # Printing Prediction
    # print(homeTeam, homeGoals[0], awayGoals[0], awayTeam)

    return f"{homeTeam:>{24}}{round(homeGoals[0], 3):{6}}{round(awayGoals[0], 3):{6}} {awayTeam}"


if __name__ == "__main__":
    scores = []
    for match in get_curr_week_fixtures():
        homeTeam = match[0]
        awayTeam = match[1]
        print("processing:", homeTeam, "vs", awayTeam)
        scores.append(make_prediction(homeTeam, awayTeam))

    print()
    for score in scores:
        print(score)
