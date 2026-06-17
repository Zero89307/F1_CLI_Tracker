import fastf1
import os

if not os.path.exists('cache_data'):
    os.mkdir('cache_data')

fastf1.Cache.enable_cache('cache_data')

class GetData:

    def __init__(self, driver_1, driver_2):
        self.driver_1 = driver_1
        self.driver_2 = driver_2

    def data(self):
        session = fastf1.get_session(year=2026, gp="Australia", identifier='Qualifying')
        session.load()

        # Gets ALL Lap times for specific driver //Both use driver call sign
        driver_1_all_laps = session.laps.pick_driver(self.driver_1)
        driver_2_all_laps = session.laps.pick_driver(self.driver_2)

        # Gets FASTEST Lap for specific driver
        driver_1_fastest_lap = driver_1_all_laps.pick_fastest(self.driver_1)
        driver_2_fastest_lap = driver_2_all_laps.pick_fastest(self.driver_2)