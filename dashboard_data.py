import fastf1
import os
import datetime
import feedparser

if not os.path.exists('cache_data'):
    os.mkdir('cache_data')
fastf1.Cache.enable_cache('cache_data')

def next_race_data():
    gp_info = fastf1.get_events_remaining().iloc[0]
    current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
    race_time = gp_info['Session5Date'].to_pydatetime().astimezone()
    weekend_details = {
        "country" : gp_info["Country"],
        "location" : gp_info["Location"],
        "weekend_duration" : gp_info["Session1Date"].strftime("%m-%d") + " - " + gp_info["Session5Date"].strftime("%d"),
        "fp": {
            "fp_dates": {
                f"fp{i+1}_date" : gp_info[f"Session{i+1}Date"].strftime("%m-%d") for i in range(3)
            },
            "fp_times": {
                f"fp{i+1}_time" : gp_info[f"Session{i+1}Date"].strftime("%H-%M") for i in range(3)
            }
        },
        "quali": {
            "quali_date": gp_info["Session4Date"].strftime("%m-%d"),
            "quali_time": gp_info["Session4Date"].strftime("%H-%M"),
        },
        "race": {
            "race_date": gp_info["Session5Date"].strftime("%m-%d"),
            "race_time": gp_info["Session5Date"].strftime("%H-%M"),
            "time_left" : {
                "days" : (race_time - current_time).days,
                "hours" :  str((race_time - current_time).seconds // 3600),
                "minutes" :str(((race_time - current_time).seconds % 3600) // 60),
            }
        }
    }
    return weekend_details

def get_f1_news():
    feed_url = "https://www.motorsport.com/rss/f1/news/"
    news_feed = feedparser.parse(feed_url)

    news_list = []
    for entry in news_feed.entries[:4]:
        news_list.append(entry.title)

    return news_list

def current_standings():
    drivers  = fastf1.ergast.Ergast().get_driver_standings(2026)
    constructors = fastf1.ergast.Ergast().get_constructor_standings(2026)

    driver_df = drivers.content[0]
    constructors_df = constructors.content[0]

    standings = {
        f"drivers" : [
            {
                "name" : driver_df["givenName"].iloc[i],
                "constructor": driver_df["constructorNames"].iloc[i][0],
                "points": int(driver_df["points"].iloc[i].item()),
                "wins": driver_df["wins"].iloc[i].item()
            } for i in range(3)
        ],
        "constructors" : [
            {
                "name" : constructors_df["constructorName"].iloc[j],
                "points" : int(constructors_df["points"].iloc[j].item()),
                "wins" : constructors_df["wins"].iloc[j].item()
            } for j in range(3)
        ]

    }
    return standings
current_standings()