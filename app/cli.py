from utils.utils import slow_print, getchar, is_valid_date, siege_week
from utils.hackatime import Client

from rich.console import Console
from rich.table import Table

from datetime import date

import sys, os, json

class CLI():
    def __init__(self):
        self.hackatime_client = Client()

        if os.path.exists("data.json"):
            with open("data.json", "r") as file:
                self.data = json.load(file)
        else:
            self.data = {"goals": {}, "coffers": 0, "bought_items": [], "projects": {}}

    def wait_for_input(self, text):
        print(text)
        return getchar()
    
    def wait_for_exit(self):
        print()
        self.wait_for_input("Press any key to exit ")
        os.system('cls' if os.name == 'nt' else 'clear')

    def command_wait(self, text, options: dict):
        selected_option = ''
        
        while selected_option not in options:
            slow_print(text)
            selected_option = self.wait_for_input("Select an option: ")
            os.system('cls' if os.name == 'nt' else 'clear')

        options[selected_option]()

    def render_logo(self):
        from utils.constants import LOGO_ASCII_ART, PROJECT_INFO
        slow_print(LOGO_ASCII_ART, 0.01)
        slow_print(PROJECT_INFO)

    def home(self, start=False):
        os.system('cls' if os.name == 'nt' else 'clear')

        if start:
            self.render_logo()

        from utils.constants import HOME_SCREEN
        self.command_wait(HOME_SCREEN.format(siege_week=siege_week()), {"q": sys.exit, "t": lambda: self.stats_screen(True), "a": self.stats_screen, "p": self.projects, "g": self.goals, "h": self.shop, "s": self.statistics, "c": self.calendar})

    def statistics(self):
        slow_print("Comming Soon!")
        self.wait_for_exit()
        self.home()

    def calendar(self):
        slow_print("Comming Soon!")
        self.wait_for_exit()
        self.home()

    def projects(self):
        slow_print("Due to platform limitations, you have to add your projects from Hackatime manually. Sorry about this.")
        
        print("Loading Hackatime stats...")
        data = self.hackatime_client.get_stats()

        if self.data["projects"]:
            console = Console()

            table = Table(title=f"Top Project: {data[2]} | Total time: {data[4]}")

            table.add_column("Project", style="cyan", no_wrap=True)
            table.add_column("Time", style="magenta")
            table.add_column("Percent", justify="right", style="green")

            for project, time, percent in data[3]:
                if project in self.data["projects"]:
                    table.add_row(project, str(time), f"{percent}%")

            console.print(table)
        else:
            slow_print("You dont have any Siege projects.")

        self.command_wait("""You can do the following:
a - Add project from Hackatime
c - Create ship event to add coffers
q - Exit to home""", {"a": self.add_project, "q": self.home, "c": self.create_ship_event})

    def create_ship_event(self):
        print("Loading Hackatime stats...")
        data = self.hackatime_client.get_stats()

        if self.data["projects"]:
            console = Console()

            table = Table(title=f"Top Project: {data[2]} | Total time: {data[4]}")

            table.add_column("Project", style="cyan", no_wrap=True)
            table.add_column("Time", style="magenta")
            table.add_column("Percent", justify="right", style="green")

            for project, time, percent in data[3]:
                if project in self.data["projects"]:
                    table.add_row(project, str(time), f"{percent}%")

            console.print(table)
        else:
            slow_print("You dont have any Siege projects.")
            self.wait_for_exit()
            self.projects()
            return
        
        valid_project_names = [project_data[0] for project_data in data[3]]
        
        project_name = ''
        while project_name not in valid_project_names:
            project_name = input("To add a ship event, please put the project's name here: ")

        coffer_amount = ''
        while not coffer_amount.isnumeric():
            coffer_amount = input("Please enter the amount of coffers you got for the ship: ")
        coffer_amount = int(coffer_amount)

        ship_date = ''
        while not ship_date.isnumeric():
            ship_date = input("Please enter the date of ship (format YYYY-MM-DD): ")
        ship_date = int(ship_date)

        self.data["projects"][project_name]["ship_events"].append((ship_date, coffer_amount))
        self.data["projects"][project_name]["total_coffers"] += coffer_amount
        self.data["coffers"] += coffer_amount

        slow_print(f"Project {project_name} succesfully added to Siege projects!")

        self.wait_for_exit()
        self.projects()

    def add_project(self):
        slow_print("Here are your Hackatime projects starting from September 1th, 2025.")
        print("Loading Hackatime stats...")
        data = self.hackatime_client.get_stats()

        console = Console()

        table = Table(title=f"Top Project: {data[2]} | Total time: {data[4]}")

        table.add_column("Project", style="cyan", no_wrap=True)
        table.add_column("Time", style="magenta")
        table.add_column("Percent", justify="right", style="green")

        for project, time, percent in data[3]:
            table.add_row(project, str(time), f"{percent}%")

        console.print(table)

        valid_project_names = [project_data[0] for project_data in data[3]]
        project_name = ''
        
        while project_name not in valid_project_names:
            project_name = input("To add a project, please put its name here: ")

        self.data["projects"][project_name] = {"ship_events": {}, "total_coffers": 0}

        slow_print(f"Project {project_name} succesfully added to Siege projects!")

        self.wait_for_exit()
        self.projects()

    def add_coffers(self, project_name):
        coffers = ''
        while not coffers.isnumeric():
            coffers = input("Amount of coffers: ")

        hours = ''
        while not hours.isnumeric():
            hours = input("Amount of hours: ")

        self.data["coffers"] += int(coffers)

        slow_print(f"Multiplier: {round(int(coffers) / int(hours), 2)}x")
        slow_print(f"Date: {self.hackatime_client.get_date()}")
        slow_print(f"You are now the proud owner of {self.data['data']['coffers']} coffers!")

        self.wait_for_exit()
        self.home()

    def stats_screen(self, today=False):
        print("Loading Hackatime stats...")
        data = self.hackatime_client.get_stats_for_today() if today else self.hackatime_client.get_stats()
        
        console = Console()

        table = Table(title=f"Top Language: {data[0]} | Total time: {data[4]}")

        table.add_column("Language", style="cyan", no_wrap=True)
        table.add_column("Time", style="magenta")
        table.add_column("Percent", justify="right", style="green")

        for lang, time, percent in data[1]:
            table.add_row(lang, str(time), f"{percent}%")

        console.print(table)

        table2 = Table(title=f"Top Project: {data[2]} | Total time: {data[4]}")

        table2.add_column("Project", style="cyan", no_wrap=True)
        table2.add_column("Time", style="magenta")
        table2.add_column("Percent", justify="right", style="green")

        for project, time, percent in data[3]:
            table2.add_row(project, str(time), f"{percent}%")

        console.print(table2)

        self.wait_for_exit()
        self.home()

    def goals(self):
        from utils.constants import GOALS_SCREEN
        self.command_wait(GOALS_SCREEN.format(goals=self.data["goals"]), {"a": self.add_goal, "r": self.remove_goal, "q": self.home})

    def add_goal(self):
        print("Loading Hackatime stats...")
        stats = self.hackatime_client.get_stats(end_date=self.hackatime_client.get_date())

        goal_name = None
        while goal_name in self.data["goals"] or goal_name == None:
            goal_name = input("Goal Name (Cant exist already): ")

        goal_type = ''
        while goal_type not in ["coffers", "hours"]:
            goal_type = input("Goal Type (coffers/hours): ")
        
        goal_date = ''
        while not is_valid_date(goal_date):
            goal_date = input("Date to complete goal in (format: YYYY-MM-DD): ")
        
        goal_number = ''
        while not goal_number.isnumeric():
            goal_number = input(f"Amount of {goal_type}: ")
        goal_number = int(goal_number)
        
        os.system('cls' if os.name == 'nt' else 'clear')

        remaining_days = (date(*map(int, goal_date.split("-"))) - date.today()).days
        slow_print(f"You have {remaining_days} remaining days of siege to complete this goal!")

        if goal_type == "coffers":
            if self.data["coffers"] > goal_number:
                slow_print("Goal already completed, skipping...")
                return
            
            slow_print(f"You need {goal_number - self.data['data']['coffers']} more coffers to complete this goal!")

        elif goal_type == "hours":
            if stats[3] / 3600 > goal_number:
                slow_print("Goal already completed, skipping...")
                return
            
            difference = goal_number - (stats[5] / 3600)
            daily_average_hours = (stats[7] / 3600)

            slow_print(f"You need {round(difference, 1)} more hours to complete this goal!")
            slow_print(f"Your daily average time is {stats[6]}")

            if difference > remaining_days * daily_average_hours:
                slow_print(f"If you don't hurry up, you cant complete this goal!\nWith your current daily average, you would complete it in {round(difference / daily_average_hours, 1)} days!")
            else:
                slow_print(f"With your daily average time, you can complete this goal this in {round(difference / daily_average_hours, 1)} days!")

        self.data["goals"][goal_name] = [goal_date, goal_type, goal_number]

        self.wait_for_exit()
        self.home()

    def remove_goal(self):
        goal_name = ''
        while goal_name not in self.data["goals"]:
            goal_name = input("Goal Name To Remove: ")

        del self.data["goals"][goal_name]

    def shop(self):
        from utils.constants import SHOP_SCREEN, shop_items
        slow_print(SHOP_SCREEN)

        console = Console()

        table = Table(title=f"Shop | Coffers: {self.data['coffers']}")

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Price", style="magenta")
        table.add_column("Comment", justify="right", style="green")
        table.add_column("Stock", justify="right", style="yellow")

        n = 0
        for name, comment, price, stock in shop_items:
            table.add_row(str(n), name, str(price), comment, str(stock))
            n += 1

        console.print(table)

        self.command_wait("""Please press one of the following keys to interact!
b - Buy item
q - Exit to home""", {"b": self.buy_item, "q": self.home})

    def buy_item(self):
        from utils.constants import shop_items
        console = Console()

        table = Table(title=f"Shop | Coffers: {self.data['coffers']}")

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Price", style="magenta")
        table.add_column("Comment", justify="right", style="green")
        table.add_column("Stock", justify="right", style="yellow")

        n = 0
        for name, comment, price, stock in shop_items:
            table.add_row(str(n), name, str(price), comment, str(stock - self.data["bought_items"].count(name)))
            n += 1

        console.print(table)

        item_id = ""
        while not item_id.isnumeric() or not int(item_id) <= len(shop_items):
            item_id = input("Enter an item ID to buy: ")
        item_id = int(item_id)

        if shop_items[item_id][3] < 1:
            slow_print("There is no stock left for the item.")
            self.wait_for_exit()
            self.shop()
            return
        
        if not self.data["coffers"] >= shop_items[item_id][2]:
            slow_print("You don't have enough coffers to buy this item.")
            slow_print(f"You need {shop_items[item_id][2] - self.data['coffers']} more coffers!")
            self.wait_for_exit()
            self.shop()
            return
        
        slow_print(f"You successfully bought the {shop_items[item_id][0]} item!")

        self.data["coffers"] -= shop_items[item_id][2]
        self.data["bought_items"].append(shop_items[item_id][0])

        slow_print(f"You now have {self.data['coffers']} remaining coffers!")

def run_cli():
    cli = CLI()
    cli.home(start=True)