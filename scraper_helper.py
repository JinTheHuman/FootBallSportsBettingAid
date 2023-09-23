from bs4 import BeautifulSoup
import requests


# Get Table Position of team
def get_table_pos(teamName):
    table_text = requests.get("https://www.skysports.com/premier-league-table").text
    table_soup = BeautifulSoup(table_text, "lxml")

    table = [
        cell["href"][1:]
        for cell in table_soup.find_all("a", class_="standing-table__cell--name-link")
    ]

    try:
        return table.index(teamName) + 1
    except:
        return -1


# Get This weeks fixtures
def get_curr_week_fixtures():
    game_week_fixtures_text = requests.get(
        "https://www.skysports.com/premier-league-fixtures"
    ).text

    game_week_fixtures_soup = BeautifulSoup(game_week_fixtures_text, "lxml")

    fixtures = [
        link
        for link in game_week_fixtures_soup.find_all(
            "a", class_="matches__item matches__link"
        )
    ]
    fixtures = fixtures[:10]

    fixture_names = []
    for fixture in fixtures:
        match = [
            name.text.lower().replace(" ", "-")
            for name in fixture.find_all(class_="swap-text__target")[:2]
        ]
        fixture_names.append(match)
    return fixture_names


# Constructs stats link from team link
def get_stats_link(link):
    splitLinks = link.split("/")
    newlink = (
        "https://www.skysports.com/football/"
        + splitLinks[4]
        + "/stats/"
        + splitLinks[5]
    )
    return newlink


# Gets stats from last five games
def get_last_five_game_stats(teamName):
    played_against = []

    results_html_text = requests.get(
        "https://www.skysports.com/" + teamName + "-results"
    ).text

    results_soup = BeautifulSoup(results_html_text, "lxml")

    fixtures = [
        get_stats_link(link["href"])
        for link in results_soup.find_all("a", class_="matches__item matches__link")
    ]

    fixture_stats = []

    for fixture in fixtures[:5]:
        # Holds stats as string for debugging
        stat_txt = ""

        stats_html_text = requests.get(fixture).text
        stats_soup = BeautifulSoup(stats_html_text, "lxml")

        # Calculate If Home Game
        names = stats_soup.find_all(
            "span", class_="sdc-site-match-header__team-name-block-target"
        )
        home = names[0].text.lower() == teamName.lower().replace("-", " ")

        if home:
            played_against.append(names[1].text.lower().replace(" ", "-"))
        else:
            played_against.append(names[0].text.lower().replace(" ", "-"))

        # Print Team Names
        # print(names[0].text, "vs", names[1].text)

        stats = stats_soup.find_all("div", class_="sdc-site-match-stats__stats")

        # Holds stats as numbers for processing
        num_stats = []
        first = True
        try:
            for stat in stats:
                # Create String
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

    return fixture_stats, played_against
