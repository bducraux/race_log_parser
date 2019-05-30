from prettytable import PrettyTable
import datetime


class RaceResult:
    def __init__(self, _logfile):
        self._race_data = self._extract_log_data(_logfile)
        self._grouped_result = {}

    # Extract logfile into: [0] Hour | [1] Pilot Code | [2] Pilot Name | [3] Lap | [4] Lap Time | [5] Avg Speed
    @staticmethod
    def _extract_log_data(_logfile):
        race_data = []
        try:
            with open(_logfile, "r") as f:
                # Loop over each log line jumping the first line
                lines = f.readlines()[1:]
                for line in lines:
                    cleaned_line = tuple(line.replace(" -", "").split())
                    race_data.append(cleaned_line)
        except IOError as e:
            print("Couldn't open the file (%s)." % e)

        return race_data

    def _group_result_by_code(self):
        pilot_results = {}
        for pilot_result in self._race_data:
            if pilot_result[1] not in pilot_results:
                pilot_results[pilot_result[1]] = {'name': pilot_result[2], 'lap': pilot_result[3], 'time': [pilot_result[4]], 'speed': [pilot_result[5]]}
            else:
                pilot_results[pilot_result[1]]['lap'] = pilot_result[3]
                pilot_results[pilot_result[1]]['time'].append(pilot_result[4])
                pilot_results[pilot_result[1]]['speed'].append(pilot_result[5])

        self._grouped_result = pilot_results

    def _consolidate_results(self):
        for pilot in self._grouped_result.values():
            # get race time and best lap
            for time in pilot['time']:
                if 'race_time' not in pilot:
                    pilot['race_time'] = self.transform_str_to_timedelta(time)
                    pilot['best_lap'] = pilot['race_time']
                else:
                    new_race_time = self.transform_str_to_timedelta(time)

                    pilot['race_time'] += new_race_time

                    if pilot['best_lap'] > new_race_time:
                        pilot['best_lap'] = new_race_time

            # get avg speed
            sum_speed = 0
            for speed in pilot['speed']:
                sum_speed += float(speed.replace(",", "."))

            pilot['avg_speed'] = sum_speed / int(pilot['lap'])

    @staticmethod
    def transform_str_to_timedelta(str_time):
        tmp_time = datetime.datetime.strptime(str_time, '%M:%S.%f')
        transformed_time = datetime.timedelta(minutes=tmp_time.minute, seconds=tmp_time.second,
                                              microseconds=tmp_time.microsecond)
        return transformed_time

    def get_results(self):
        self._group_result_by_code()
        self._consolidate_results()

        results = []
        pos = 0
        for code, pilot_result in sorted(self._grouped_result.items(), key=lambda e: e[1]['race_time']):
            pos += 1
            name = pilot_result['name']
            lap = pilot_result['lap']
            race_time = str(pilot_result['race_time'])[2:-3]
            best_lap = str(pilot_result['best_lap'])[2:-3]
            avg_speed = str(pilot_result['avg_speed'])[:6]

            results.append([pos, code, name, lap, race_time, best_lap, avg_speed])

        return results

    @staticmethod
    def add_position_to_result(results):
        pos = 0
        for result in results:
            pos += 1
            [pos] + result

        return results

    def show_results(self):
        race_results = self.get_results()

        x = PrettyTable()
        x.field_names = ["Pos", "Code", "Pilot", "Lap Completed", "Race Time", "Best Lap", "Avg Speed"]
        x.align["Pilot"] = "l"

        for pilot_result in race_results:
            x.add_row(pilot_result)

        print(x.get_string(title="Race Result"))
