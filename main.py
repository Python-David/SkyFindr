import tweepy.errors
import os
import dotenv
from air_peace import AirPeace
import time

air_peace = AirPeace()


# air_peace.get_today_flight_details("ABV", "LOS")
# air_peace.get_any_day_flight_details_one_way("21", "September", "2022", "LOS", "ABV")
# air_peace.get_any_day_flight_details_return("10", "September", "2022", "17", "September", "2022", "LOS", "ABV")

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, "r")
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, "w")
    f_write.write(str(last_seen_id))
    f_write.close()
    return


# 1559502339152781312
def process_tweet(tweet):
    if "#skyfind" in tweet:
        bare_tweet = tweet.replace("@skyfindr #skyfind ", "").split(",")
        tweet_list = [x.replace(" ", "").lower().upper() for x in bare_tweet]

        return tweet_list

    else:
        return "Keyword #skyfind not detected, try again."


dotenv.load_dotenv()
auth = tweepy.OAuthHandler(os.environ["API_Key"], os.environ["API_Secret_Key"])
auth.set_access_token(os.environ["Access_Token"], os.environ["Access_Token_Secret"])
api = tweepy.API(auth)


# Process begins

def run_app():
    mentions = api.mentions_timeline(since_id=retrieve_last_seen_id("last_seen_id.txt"))

    for mention in reversed(mentions):
        tweet_text = process_tweet(mention.text)
        state_keys = {
            "LAGOS": "LOS",
            "ABUJA": "ABV",
            "KANO": "KAN",
            "ENUGU": "ENU",
            "ACCRA": "AAC",
            "AKURE": "AKR",
            "ANAMBRA": "ANA",
            "ASABA": "ABB",
            "BANJUL": "BJL",
            "BENIN": "BNI",
            "CALABAR": "CBQ",
            "DAKAR": "DSS",
            "DOUALA": "DLA",
            "DUBAI": "DXB",
            "FREETOWN": "FNA",
            "GOMBE": "GMO",
            "IBADAN": "IBA",
            "ILORIN": "ILR",
            "JOHANNESBURG": "JNB",
            "MAKURDI": "MDI",
            "OWERRI": "QOW",
            "PORT HARCOURT": "PHC",
            "PORTHARCOURT": "PHC",
            "PORT-HARCOURT": "PHC",
            "WARRI": "QRW",
        }
        username = mention.user.screen_name
        user_id = mention.user.id
        last_seen = mention.id

        if tweet_text == "Keyword #skyfind not detected, try again.":
            api.update_status(
                f"@{username} Please try again, make sure the #skyfind hashtag is in your tweet. See pinned "
                f"tweet for more details", in_reply_to_status_id=last_seen)
        else:
            if (tweet_text[0] == "AIRPEACE" or tweet_text[0] == "AIR PEACE") and ("ONEWAY" or "ONE WAY") in tweet_text:
                print(tweet_text[1], tweet_text[2].title(), tweet_text[3], tweet_text[4],
                      tweet_text[5])
                response = air_peace.get_any_day_flight_details_one_way(tweet_text[1],
                                                                        tweet_text[2].title(),
                                                                        tweet_text[3],
                                                                        state_keys[tweet_text[4]],
                                                                        state_keys[tweet_text[5]]
                                                                        )

                num = 1
                message = ""

                if type(response) == dict:
                    try:
                        for key in response:
                            message += f"{num}. {response[key][0]}" + " | " f"{response[key][1][0]}" + \
                                       " - " f"{response[key][1][1]}\n"
                            num += 1
                        direct_message = f"Hey {username},\n\nHere are the flights we were able to #skyfind for you from " \
                                         f"{tweet_text[0].title()} on {tweet_text[2].title()} {tweet_text[1]}:\n\n{message}" \
                                         f"\n\nSky Findr."
                        api.send_direct_message(recipient_id=user_id, text=direct_message)
                        api.update_status(f"@{username} Your flight details are now available in your DM",
                                          in_reply_to_status_id=last_seen)
                    except tweepy.Forbidden:
                        reply = "Please try again but this time, follow back so I can send the info to your DM."
                        api.update_status(f"@{username} {reply}", in_reply_to_status_id=last_seen)
                else:
                    api.update_status(f"@{username} {response}", in_reply_to_status_id=last_seen)
            elif (tweet_text[0] == "AIRPEACE" or tweet_text[0] == "AIR PEACE") and ("RETURN") in tweet_text:
                print(tweet_text[1], tweet_text[2].title(), tweet_text[3], tweet_text[4],
                      tweet_text[5], tweet_text[6], tweet_text[7], tweet_text[8])
                response = air_peace.get_any_day_flight_details_return(tweet_text[1],
                                                                       tweet_text[2].title(),
                                                                       tweet_text[3],
                                                                       tweet_text[4],
                                                                       tweet_text[5].title(),
                                                                       tweet_text[6],
                                                                       state_keys[tweet_text[7]],
                                                                       state_keys[tweet_text[8]],
                                                                       )

                num = 1
                message = ""
                username = mention.user.screen_name
                user_id = mention.user.id
                last_seen = mention.id
                if type(response) == dict:
                    try:
                        for key in response:
                            message += f"{num}. {response[key][0]}" + " | " f"{response[key][1][0]}" + \
                                       " - " f"{response[key][1][1]}" + " | " f"{response[key][2]}\n"
                            num += 1
                        direct_message = f"Hey {username},\n\nHere are the flights we were able to #skyfind for you from " \
                                         f"{tweet_text[0].title()} on {tweet_text[2].title()} {tweet_text[1]} " \
                                         f"returning {tweet_text[5].title()} {tweet_text[4]}:\n\n{message}" \
                                         f"\n\nSky Findr."
                        api.send_direct_message(recipient_id=user_id, text=direct_message)
                        api.update_status(f"@{username} Your flight details are now available in your DM",
                                          in_reply_to_status_id=last_seen)
                    except tweepy.Forbidden:
                        reply = "Please try again but this time, follow back so I can send the info to your DM."
                        api.update_status(f"@{username} {reply}", in_reply_to_status_id=last_seen)
                else:
                    api.update_status(f"@{username} {response}", in_reply_to_status_id=last_seen)

        store_last_seen_id(last_seen, file_name="last_seen_id.txt")


while True:
    run_app()
    print("running")
    time.sleep(100)
