import os, requests, configparser, sys
from datetime import date, datetime, timedelta
from utils.constants import HACKATIME_URL
from pathlib import Path

class Client:
    def __init__(self):
        wakatime_config_path = Path.home() / ".wakatime.cfg"

        if not os.path.exists(wakatime_config_path):
            print("Wakatime config file doesnt exist, so we cant connect to Hackatime. Exiting...")
            sys.exit(1)

        self.config = configparser.ConfigParser()
        with open(wakatime_config_path, encoding="utf-8-sig") as f:
            self.config.read_file(f)

        self.api_url = HACKATIME_URL
        self.api_key = self.config["settings"]["api_key"]
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def get_date(self):
        return date.today().strftime("%Y-%m-%d")

    def add_day(self, date_str):
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        next_day = dt + timedelta(days=1)
        return next_day.strftime("%Y-%m-%d")
    
    def request(self, path):
        response = requests.get(f"{self.api_url}{path}", headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code

    def get_stats(self, start_date="2025-09-01", end_date="2025-12-01"):
        response = self.request(f"/users/my/stats?start_date={start_date}&end_date={end_date}&features=projects,languages")["data"]

        if not response.get("languages"): # no time for range, prevent crash
            return None, 0

        top_language = response["languages"][0]["name"]
        top_project = response["projects"][0]["name"]
        total_time = response["human_readable_total"]
        total_time_seconds = response["total_seconds"]
        daily_average = response["human_readable_daily_average"]
        daily_average_seconds = response["daily_average"]

        return top_language, \
               [(language_dict["name"], language_dict["text"], language_dict["percent"]) for language_dict in response["languages"]], \
               top_project, \
               [(language_dict["name"], language_dict["text"], language_dict["percent"]) for language_dict in response["projects"]], \
               total_time, \
               total_time_seconds, \
               daily_average, \
               daily_average_seconds
    
    def get_stats_for_day(self, date="2025-09-01"):
        return self.get_stats(date, self.add_day(date))
    
    def get_stats_for_today(self):
        return self.get_stats_for_day(self.get_date())