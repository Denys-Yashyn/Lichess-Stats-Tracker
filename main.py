import os, requests, smtplib, json, datetime
from dotenv import load_dotenv

load_dotenv()


class LichessAPIClient:
    def __init__(self):
        self.__api_token = os.getenv("LICHESS_API_TOKEN")
        self.base_url = "https://lichess.org"
        self.header = {"Authorization": f"Bearer {self.__api_token}"}

    # get player info (name, modes, rating)
    def get(self, player):
        url = f"{self.base_url}/api/user/{player}"
        response = requests.get(url, headers=self.header)

        if response.status_code == 200:
            print("Success!")
            response_data = response.json()
            return response_data["perfs"]

        elif response.status_code == 404:
            print(f'User: "{player}" not found')
            return response.status_code

        else:
            print(
                f"Something has went wrong. Code: {response.status_code}\nMore info about codes is here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status"
            )


class StatsAnalyzer:
    def __init__(self, api_client):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_dir, "config.json")
        self.api_client = api_client
        self.DEFAULT_CONFIG = {
            "usernames": ["Yashin_Denis", "Pro_100_Sasha"],
            "modes": ["rapid", "puzzle", "blitz"],
        }

        # create default config.json file
        if not os.path.exists(self.config_path):
            # This part will create a default config file
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)
            print("Created default config.json.")

        # read config file
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        self.players = self.config["usernames"]
        self.config["modes"]
        self.rank_dict = {"Date": self.date, "Users": {}}
        self.message = ""
        self.stats_path = os.path.join(self.base_dir, "stats.json")

    def generate_report(self):
        self.message = (
            f"\t\t{self.date}\n\nGood Day!\n\nHere is your requested stats:\n"
        )

        for player in self.players:
            value = self.api_client.get(player)

            if value == 404:
                continue

            elif value:

                self.modes = {
                    mode.title(): {
                        stat: value[mode][stat] for stat in ["rating", "games"]
                    }
                    for mode in self.config["modes"]
                }

                self.message += f"\n\t{player}:\n"
                self.rank_dict["Users"][player] = self.modes

                for mode, stats in self.modes.items():
                    self.message += f"\n{mode} "

                    for stat in stats:
                        self.message += f"{stat}: {stats[stat]} | "

                self.message += "\n"

            else:
                break

        if (
            self.message
            == f"\t\tDate: {self.date}\n\nGood Day!\n\nHere is your requested stats:\n"
        ):
            return None
        else:
            return self.message

    def create_stats_file(self):
        if self.generate_report() == None:
            print("Error create_stats_file: self.message is empty")
            return None

        if os.path.exists(self.stats_path):
            try:
                # read stats.json file if file exists
                with open(self.stats_path, "r", encoding="utf-8") as stats:
                    self.old_data = json.load(stats)

            except json.JSONDecodeError:
                self.old_data = {"Date": self.date, "Users": {}}

        else:
            self.old_data = {"Date": self.date, "Users": {}}

        self.new_data = self.old_data.copy()
        self.new_data.update(self.rank_dict)

        if self.new_data["Users"] == self.old_data["Users"]:
            self.message += "\nPlayers don't have changes"
            return self.message

        # update changes in stats.json file
        with open(self.stats_path, "w", encoding="utf-8") as stats:
            json.dump(self.new_data, stats, ensure_ascii=False, indent=4)

        self.message += f"\n\t\tLast Update: {self.old_data["Date"]}\n\tUPDATES:\n\n"
        self.users = self.new_data["Users"]
              

        # to learn
        old_modes = set()
        for user_data in self.old_data["Users"].values():
            old_modes.update(user_data.keys())

        new_modes = set()
        for user_data in self.users.values():
            new_modes.update(user_data.keys())

        added_modes = new_modes - old_modes
        removed_modes = old_modes - new_modes

        if added_modes or removed_modes:
            for mode in added_modes:
                self.message += f"- New mode: {mode}\n"
            self.message += "\n"
            for mode in removed_modes:
                self.message += f"- Removed mode: {mode}\n"
            self.message += "\n"

        # Check removed users 
        removed = False
        
        for old_user in self.old_data["Users"]:
            if old_user not in self.users:
                self.message += f"- Removed User: {old_user}\n"
                removed = True
        
        if removed == True:
            self.message += "\n"
        
        #  Rating comparison
        for user, gmodes in self.users.items():
            
            # New user:
            if user not in self.old_data["Users"]:
                self.message += f"- New User: {user}\n"
                continue

            # if stats changed...
            if self.users[user] != self.old_data["Users"][user]:
                user_header_printed = False
                old_user_data = self.old_data["Users"][user]

                for gmode, value in gmodes.items():
                    if gmode in added_modes:
                        continue 

                    # if mode old and has rating changes...
                    if gmode in old_user_data and old_user_data[gmode] != value:
                        if not user_header_printed:
                            self.message += f"{user}:\n"
                            user_header_printed = True

                        # compute progress
                        old_rating = old_user_data[gmode]["rating"]
                        new_rating = value["rating"] 
                        old_games = old_user_data[gmode]["games"]
                        new_games = value["games"]

                        rating_change = new_rating - old_rating
                        games_played = new_games - old_games

                        # adding "+" to positives numbers
                        sign = "+" if rating_change > 0 else ""
                        progress = f"Progress: {sign}{rating_change} for {games_played} played game(s)"

                        self.message += f"\n-  {gmode}: {old_rating} -> {new_rating} rating \n"
                        self.message += f"   {progress}\n"
                
                self.message += "\n"

        return self.message

class EmailNotifer:
    pass

analyzer = StatsAnalyzer(LichessAPIClient())
analyze = analyzer.create_stats_file()

print(analyze)
