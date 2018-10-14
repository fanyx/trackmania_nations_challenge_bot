import configparser
import time
import os

from utils import load_data, load_medal_times, get_last_SQL_update
from calculations import get_individual_records, substitute_missing_times, sort_by_track_and_tracks_by_date, get_standings
from plots import plot_total_standings


def update_data():
    raw_data = load_data()
    individual_records = get_individual_records(raw_data)
    data = substitute_missing_times(individual_records, nadeo_medals)
    data = sort_by_track_and_tracks_by_date(data)
    return data

def renew_plot(data):
    year, week = data.dropna()["Date"].max().isocalendar()[0:2]
    plot_total_standings(data, f"Meisterschaftsstand_y{year}_w{week}")




if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")

    PLOT_DIR = config["SAVE_POINTS"]["PLOT_DIR"]
    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)

    nadeo_medals = load_medal_times()

    data = update_data()
    renew_plot(data)


    last_SQL_update = get_last_SQL_update()

    while True:
        time.sleep(1)

        if last_SQL_update == get_last_SQL_update():
            continue

        print("A new time was set!")
        last_SQL_update = get_last_SQL_update()

        data = update_data()
        renew_plot(data)
