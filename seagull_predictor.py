from bs4 import BeautifulSoup
import requests
import numpy as np
from DataModels.seagull_data_model import make_away_predictions
from DataModels.seagull_data_model import make_home_predictions
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
)
from constants import TEAMNAMES, STATNAMES


def make_prediction(homeTeam, awayTeam):
    h_fixtures, h_played_against = get_last_five_game_stats(homeTeam)
    a_fixtures, a_played_against = get_last_five_game_stats(awayTeam)

    h_weights, a_weights = calculate_weights(h_played_against, a_played_against)

    homeStats = get_weighted_average(h_fixtures, h_weights)
    awayStats = get_weighted_average(a_fixtures, a_weights)

    # homeStats = get_average(h_fixtures)
    # awayStats = get_average(a_fixtures)

    homeGoals = make_home_predictions([np.array(homeStats).reshape(1, -1)])
    awayGoals = make_away_predictions([np.array(awayStats).reshape(1, -1)])

    print(homeTeam, homeGoals[0], awayGoals[0], awayTeam)
    return f"{homeTeam:>{24}}{round(homeGoals[0], 3):{6}} {round(awayGoals[0], 3):{6}} {awayTeam}"


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
