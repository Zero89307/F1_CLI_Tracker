import fastf1
import os

if not os.path.exists('cache_data'):
    os.mkdir('cache_data')
fastf1.Cache.enable_cache('cache_data')

def next_race_data():
    gp_info = fastf1.get_events_remaining().iloc[0]
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
        }



    }
    #print(gp_info)
    #print(weekend_details)
next_race_data()

x = fastf1.get_events_remaining().iloc[0]
print(x)