import fastf1
import os
import pandas as pd

if not os.path.exists('cache_data'):
    os.mkdir('cache_data')

fastf1.Cache.enable_cache('cache_data')

class GetData:

    def __init__(self, *driver):
        self.drivers = list(driver)


    def process_drivers(self, argument, driver_list):
        results = {}
        for f in driver_list:
            var = argument(f)
            results[f] = var
        return results

    def data(self, year, gp, identifier):
        session = fastf1.get_session(year=2026, gp="Australia", identifier='Qualifying')
        session.load()

        # Gets ALL Lap times for specific drivers //uses driver call sign
        driver_data = self.process_drivers(session.laps.pick_drivers, self.drivers)
        print(driver_data)

        # Gets FASTEST Lap for drivers
        fastest_data = self.process_drivers(lambda x : driver_data[x].pick_fastest(), self.drivers) # returns dictionary with pd df

        # Gets individual Sector Timings
        sector_timings = {driver : {
            f"sec{j+1}" : fastest_data[driver][f"Sector{j+1}Time"].total_seconds() for j in range(3)
        } for driver in self.drivers}
        print(sector_timings)

GetData("ANT", "HAM").data(2025, "Miami",'Qualifying')
