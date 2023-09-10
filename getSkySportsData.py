from bs4 import BeautifulSoup
import requests

file = open("PL_Statistics.csv", "w")
file.write(
    (
        "homeTeam,awayTeam,HomeGoals,awayGoals,HomePos,AwayPos,hShots,aShots,hOnt,aOnt,hOft,aOft,hBlock,aBlcok,hPass,aPass"
        ",hClear,aClear,hCorners,aCorners,hOff,aOff,hTackles,aTackles,hAerial,aAerial,hSaves,aSaves,hFouls,aFouls,hFoulsW,aFoulsW,"
        "hYellow,aYellow,hRed,aRed\n"
    )
)

seasons = ["2019-20", "2020-21", "2021-22", "2022-23"]

for season in seasons:
    scores_html_text = requests.get(
        "https://www.skysports.com/premier-league-results/" + season
    ).text
    scores_soup = BeautifulSoup(scores_html_text, "lxml")

    script = scores_soup.select_one('[type="text/show-more"]')
    script.replace_with(BeautifulSoup(script.contents[0], "html.parser"))

    fixtures = scores_soup.find_all("div", class_="fixres__item")
    count = 0

    for fixture in fixtures:
        score = fixture.find_all("span", class_="matches__teamscores-side")

        home_goals = score[0].text.strip()
        away_goals = score[1].text.strip()

        home_team = fixture.find(
            "span",
            class_="matches__item-col matches__participant matches__participant--side1",
        ).text.strip()
        away_team = fixture.find(
            "span",
            class_="matches__item-col matches__participant matches__participant--side2",
        ).text.strip()

        file.write(home_team + "," + away_team + "," + home_goals + "," + away_goals)

        game_link = fixture.a["href"]
        game_html_text = requests.get(game_link).text
        game_soup = BeautifulSoup(game_html_text, "lxml")
        game_tabs = game_soup.find_all("li", class_="sdc-site-localnav__item")

        stats_link = "https://www.skysports.com/"

        for tab in game_tabs:
            if "\nStats\n" == tab.text:
                stats_link += tab.a["href"]
                break

        stats_html_text = requests.get(stats_link).text
        stats_soup = BeautifulSoup(stats_html_text, "lxml")

        stats = stats_soup.find_all("div", class_="sdc-site-match-stats__stats")

        try:
            for stat in stats:
                file.write(
                    ","
                    + stat.find(
                        "div", class_="sdc-site-match-stats__stats-home"
                    ).span.text
                )
                file.write(
                    ","
                    + stat.find(
                        "div", class_="sdc-site-match-stats__stats-away"
                    ).span.text
                )
            file.write("\n")

        except:
            print("error encountered")

        count += 1
        print(f"{count} of {len(fixtures)} games analysed.")

file.close()
