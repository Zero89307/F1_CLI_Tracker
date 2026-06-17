import fastf1
import os
import pandas as pd

if not os.path.exists('cache_data'):
    os.mkdir('cache_data')

fastf1.Cache.enable_cache('cache_data')

class GetData:

    def __init__(self, driver_1, driver_2):
        self.driver_1 = driver_1
        self.driver_2 = driver_2

    def process_drivers(self, argument, *drivers):
        results = {}
        for f in drivers:
            var = argument(f)
            results[f] = var
        return results

    def data(self):
        session = fastf1.get_session(year=2026, gp="Australia", identifier='Qualifying')
        session.load()

        # Gets ALL Lap times for specific drivers //Both use driver call sign
        driver_data = self.process_drivers(session.laps.pick_drivers, self.driver_1, self.driver_2)
        #print(driver_data)

        # Gets FASTEST Lap for drivers
        fastest_data = self.process_drivers(lambda x : driver_data[x].pick_fastest(), self.driver_1, self.driver_2)

GetData("ANT", "HAM").data()
