import os, requests, smtplib, json
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv("LICHESS_API_TOKEN")
email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_APP_PASSWORD")
target_email = os.getenv("TARGET_EMAIL")
base_url = "https://lichess.org"
user_rating_dict = {}
user_names = ["Yashin_Denis", "Pro_100_Sasha"]


def get_user_info(user_name):
    header = {"Authorization": f"Bearer {api_token}"}
    url = f"{base_url}/api/user/{user_name}"
    response = requests.get(url, headers=header)

    if response.status_code == 200:
        print("Success!")
        response_data = response.json()
        return response_data

    elif response.status_code == 404:
        print(f'User: "{user_name}" not found')
        return response.status_code

    else:
        print(
            f"Something has went wrong. Code: {response.status_code}\nMore info about codes is here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status"
        )


for name in user_names:
    user_info = get_user_info(name)

    if user_info == 404:
        continue

    elif user_info:
        modes = {
            mode.title(): {
                stat: user_info["perfs"][mode][stat] for stat in ["rating", "games"]
            }
            for mode in ["rapid", "puzzle", "blitz"]
        }
        user_rating_dict[name] = modes

        print(f"Hey {name}, here is your stats:", end="")

        for mode, stats in modes.items():
            print(f"\nYour {mode}", end=" ")

            for stat in stats:
                print(f"{stat}: {stats[stat]} | ", end="")

        print("\n")

    else:
        break

else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stats_path = os.path.join(base_dir, "stats.json")

    if os.path.exists(stats_path):
        try:
            with open(stats_path, "r", encoding="utf-8") as stats:
                old_data = json.load(stats)
        except json.JSONDecodeError:
            old_data = {}
    else:
        old_data = {}

    new_data = old_data.copy()
    new_data.update(user_rating_dict)

    if new_data != old_data:
        # print("Before:", old_data, "\n")
        # print("After:", new_data)
        print("Changes:")

        for user_change in new_data:

            if user_change not in old_data:
                print("New user:", user_change)

            elif (
                new_data[user_change] != old_data[user_change]
            ):  # if user have changes, we are going to next point
                print(user_change, ":\n\nOld: \t\t\t\t\t >\t New:")

                for mod_change in new_data[user_change]:

                    if mod_change not in old_data[user_change]:
                        print("New mode", mod_change, new_data[user_change][mod_change])

                    elif (  # if mode have changes, we are printng these changes
                        new_data[user_change][mod_change]
                        != old_data[user_change][mod_change]
                    ):
                        old_rating = old_data[user_change][mod_change]["rating"]
                        new_rating = new_data[user_change][mod_change]["rating"]
                        old_games = old_data[user_change][mod_change]["games"]
                        new_games = new_data[user_change][mod_change]["games"]

                        rating_change = new_rating - old_rating
                        games_played = new_games - old_games

                        if rating_change > 0:
                            rating_change = f"+{rating_change}"

                        progress = f"Progress : {rating_change} for {games_played} played game(s)"

                        print(
                            f"{mod_change} : {old_rating} rating for {old_games} games \t > \t {mod_change} : {new_rating} rating for {new_games} games \n \t \t {progress} \n\n"
                        )

                print()
    else:
        print("Users don't have changes")

    with open(stats_path, "w", encoding="utf-8") as stats:
        json.dump(new_data, stats, ensure_ascii=False, indent=4)
