# import our libraries
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Page variable and date input

date = input("Please enter a date in the following format MM/DD/YYYY: ")
Format = datetime.strptime(date, '%m/%d/%Y')


page = requests.get(
    f"https://www.yallakora.com/match-center?date={date}#days")
print(page.encoding)

# create our main function


def main(page):

    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    match_details = []
    championships = soup.find_all("div", {"class": "matchCard"})

    def get_match_info(championships):
        championship_title = championships.contents[1].find("h2").text.strip()
        all_matches = championships.contents[3].find_all("li")
        number_of_matches = len(all_matches)

        # for loop to get match details
        for i in range(number_of_matches):
            # get teams name
            team_A = all_matches[i].find(
                "div", {"class": "teamA"}).text.strip()
            team_b = all_matches[i].find(
                "div", {"class": "teamB"}).text.strip()

            # get match score
            match_result = all_matches[i].find(
                "div", {"class": "MResult"}).find_all("span", {"class": "score"})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
            # print(score)

            # get match time
            match_time = all_matches[i].find(
                "span", {"class": "time"}).text.strip()

            # get match round
            match_round = all_matches[i].find(
                "div", {"class": "date"}).text.strip()

            # add all the data in one list
            match_details.append({'Championship': championship_title, 'Match Round': match_round,
                                 'First Team': team_A, 'Second Team': team_b, 'Match Time': match_time, 'Score': score})

    for i in range(len(championships)):
        get_match_info(championships[i])

    keys = match_details[0].keys()

    with open("E:\Python File\Yallakora_data.py\Matches.csv", "w", encoding="utf-8")as myfile:
        dictwriter = csv.DictWriter(myfile, keys)
        dictwriter.writeheader()
        dictwriter.writerows(match_details)
    print("File Created")


main(page)
