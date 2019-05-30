from race_result import RaceResult
from sys import argv


if __name__ == "__main__":
    # Get file passed as argument, if no argument is passed use the sample log file
    logFile = argv[1] if len(argv) == 2 else 'sample_race.log'

    # instantiate the RaceResult Class
    raceResult = RaceResult(logFile)

    # Show results
    raceResult.show_results()
