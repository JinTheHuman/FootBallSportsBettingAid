from bs4 import BeautifulSoup
import requests
import copy
import numpy as np
from data_model import make_away_predictions
from data_model import make_home_predictions


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

        home = names[0] == teamName

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

                if home:
                    num_stats.append(float(home_stat))
                    stat_txt += comma + home_stat
                else:
                    stat_txt += comma + away_stat
                    num_stats.append(float(away_stat))
        except:
            print("error encountered")

        fixture_stats.append(num_stats)
        print(stat_txt)
    return fixture_stats


def getaverage(statsList):
    totalStats = copy.deepcopy(statsList[0])
    for stats in statsList[1:]:
        for idx, stat in enumerate(stats):
            totalStats[idx] += stat

    length = len(statsList)

    averageStats = [round(x / length, 2) for x in totalStats]
    return averageStats


if __name__ == "__main__":
    homeTeam = input("Give me home team: ")
    awayTeam = input("Give me away team: ")

    homeStats = getaverage(getStats(homeTeam))
    awayStats = getaverage(getStats(awayTeam))

    lists = [homeStats, awayStats]
    gameStats = [val for tup in zip(*lists) for val in tup]

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

    for idx, statName in enumerate(statNames):
        print(str(statName) + ": " + str(gameStats[idx]))

    print(gameStats)

    homeGoals = make_home_predictions([np.array(gameStats).reshape(1, -1)])
    awayGoals = make_away_predictions([np.array(gameStats).reshape(1, -1)])

    print(homeTeam, homeGoals[0], awayGoals[0], awayTeam)
