from bs4 import BeautifulSoup
import requests
import copy
import numpy as np
from DataModels.pigeon_data_model import make_away_predictions
from DataModels.pigeon_data_model import make_home_predictions

teamNames = [
    "newcastle-united",
    "manchester-united",
    "manchester-city",
    "tottenham-hotspur",
    "liverpool",
    "arsenal",
    "brighton-and-hove-albion",
    "crystal-palace",
    "brentford",
    "nottingham-forest",
    "burnley",
    "luton-town",
    "everton",
    "wolverhampton-wanderers",
    "sheffield-united",
    "bournemouth",
    "fulham",
    "aston-villa",
    "chelsea",
    "west-ham-united",
]


def getStatsLink(link):
    splitLinks = link.split("/")
    newlink = (
        "https://www.skysports.com/football/"
        + splitLinks[4]
        + "/stats/"
        + splitLinks[5]
    )
    return newlink


def getStats(teamName):
    results_html_text = requests.get(
        "https://www.skysports.com/" + teamName + "-results"
    ).text

    results_soup = BeautifulSoup(results_html_text, "lxml")

    fixtures = [
        getStatsLink(link["href"])
        for link in results_soup.find_all("a", class_="matches__item matches__link")
    ]

    fixture_stats = []

    for fixture in fixtures[:5]:
        stat_txt = ""

        stats_html_text = requests.get(fixture).text
        stats_soup = BeautifulSoup(stats_html_text, "lxml")

        names = stats_soup.find_all(
            "span", class_="sdc-site-match-header__team-name-block-target"
        )

        home = names[0].text.lower() == teamName.lower().replace("-", " ")

        print(names[0].text, "vs", names[1].text)
        stats = stats_soup.find_all("div", class_="sdc-site-match-stats__stats")
        num_stats = []
        first = True
        try:
            for stat in stats:
                comma = ","
                if first:
                    comma = ""
                    first = False

                home_stat = stat.find(
                    "div", class_="sdc-site-match-stats__stats-home"
                ).span.text
                away_stat = stat.find(
                    "div", class_="sdc-site-match-stats__stats-away"
                ).span.text

                stat_txt += comma + home_stat
                stat_txt += "," + away_stat
                if home:
                    num_stats.append(float(home_stat))
                else:
                    num_stats.append(float(away_stat))
        except:
            print("error encountered")

        fixture_stats.append(num_stats)
        print(num_stats)
        print(stat_txt)
    return fixture_stats


def getaverage(statsList):
    totalStats = copy.deepcopy(statsList[0])
    for stats in statsList[1:]:
        for idx, stat in enumerate(stats):
            totalStats[idx] += stat

    length = len(statsList)

    averageStats = [round(x / length, 1) for x in totalStats]
    return averageStats


def clean_stats(stats):
    cleanStats = []
    for idx, stat in enumerate(stats):
        if idx not in [0, 1, 10, 11, 18, 19, 20, 21]:
            cleanStats.append(round(stat))
        else:
            cleanStats.append(stat)

    cleanStats[2] = cleanStats[4] + cleanStats[6] + cleanStats[8]
    cleanStats[3] = cleanStats[5] + cleanStats[7] + cleanStats[9]
    return cleanStats


def make_prediction(homeTeam, awayTeam):
    print("GETTING HOME STATS")
    homeStats = getaverage(getStats(homeTeam))
    print("GETTING AWAY STATS")
    awayStats = getaverage(getStats(awayTeam))

    lists = [homeStats, awayStats]
    gameStats = [val for tup in zip(*lists) for val in tup]

    # gameStats = clean_stats(gameStats)

    statNames = [
        "HomePos",
        "AwayPos",
        "hShots",
        "aShots",
        "hOnt",
        "aOnt",
        "hOft",
        "aOft",
        "hBlock",
        "aBlcok",
        "hPass",
        "aPass",
        "hClear",
        "aClear",
        "hCorners",
        "aCorners",
        "hOff",
        "aOff",
        "hTackles",
        "aTackles",
        "hAerial",
        "aAerial",
        "hSaves",
        "aSaves",
        "hFouls",
        "aFouls",
        "hFoulsW",
        "aFoulsW",
        "hYellow",
        "aYellow",
        "hRed",
        "aRed",
    ]

    if (gameStats[0] + gameStats[1]) != 100:
        difference = 100 - (gameStats[0] + gameStats[1])
        print(difference)
        gameStats[0] += difference / 2
        gameStats[1] += difference / 2
        gameStats[0] = round(gameStats[0], 1)
        gameStats[1] = round(gameStats[1], 1)
        print(gameStats[0], gameStats[1])
        if (gameStats[0] + gameStats[1]) != 100:
            gameStats[0] += 100 - (gameStats[0] + gameStats[1])
            gameStats[0] = round(gameStats[0], 1)

    if (gameStats[20] + gameStats[21]) != 100:
        difference = 100 - (gameStats[20] + gameStats[21])

        gameStats[20] += difference / 2
        gameStats[21] += difference / 2
        gameStats[20] = round(gameStats[20], 1)
        gameStats[21] = round(gameStats[21], 1)

        if (gameStats[20] + gameStats[21]) != 100:
            gameStats[20] += 100 - (gameStats[20] + gameStats[21])
            gameStats[20] = round(gameStats[20], 1)

    home_dataset = [x for i, x in enumerate(gameStats) if i != 23]
    away_dataset = [x for i, x in enumerate(gameStats) if i != 22]

    for idx in range(0, len(statNames), 2):
        h = str(gameStats[idx])
        a = str(gameStats[idx + 1])

        print(
            f"{idx:{2}} {statNames[idx]:{10}}{h:{30}} {idx + 1:{2}} {statNames[idx+1]:{10}}{a}"
        )

    homeGoals = make_home_predictions([np.array(home_dataset).reshape(1, -1)])
    awayGoals = make_away_predictions([np.array(away_dataset).reshape(1, -1)])

    print(homeTeam, homeGoals[0], awayGoals[0], awayTeam)

    return f"{homeTeam:>{24}}{round(homeGoals[0], 3):{6}}{round(awayGoals[0], 3):{6}} {awayTeam}"


if __name__ == "__main__":
    scores = []
    while True:
        homeTeam = input("Give me home team: ")
        awayTeam = input("Give me away team: ")

        if homeTeam == "a" or awayTeam == "a":
            break

        scores.append(make_prediction(homeTeam, awayTeam))

    print()
    for score in scores:
        print(score)
