import csv
import datetime
import os
import sys
import requests
import schedule
import time
import json
from pathlib import Path

MYSPORTS_URL = 'https://www.mysports.com'
MYSPORTS_ENTRIES = []


class MySportsEntry:
    def __init__(self, name: str, studio_id: int, studio_path: str, api_key: str):
        self.name = name
        self.studio_id = studio_id
        self.studio_path = studio_path
        self.api_key = api_key

    def __str__(self):
        return self.name.replace(' ', '_').lower()

    def __path(self, identifier: str):
        if identifier == 'active-checkin':
            return f'/nox/public/v1/studios/{self.studio_id}/utilization/v2/active-checkin'
        elif identifier == 'today':
            return f'/nox/public/v1/studios/{self.studio_id}/utilization/v2/today'
        else:
            return ''

    def __retrieve_data(self, identifier: str):
        """ Send an HTTP GET request to a "mysports.com" API-URL and return the response. """

        # URL to obtain data from
        url = f'{MYSPORTS_URL}{self.__path(identifier)}'

        # headers to send with the request
        headers = {
            "Content-Type": "application/json",
            "x-tenant": self.api_key,
            "DNT": "1",
        }

        # send GET request to the URL with headers
        response = requests.get(url, headers=headers)

        # return the response
        return response

    def is_open(self) -> bool:
        """ Check whether the gym is open. """

        # get HTTP response
        response = self.__retrieve_data('today')

        # convert response to JSON format and return the first value of the "current" key
        for x in range(len(response.json())):
            # if the "current" key exists return true
            if response.json()[x - 1]['current'] is True:
                return True

        # if the "current" key does not exist return false
        return False

    def visitor_count(self) -> int:
        """ Return the current visitor count. """

        # get HTTP response
        response = self.__retrieve_data('active-checkin')

        # convert response to JSON format and return the value of the "value" key
        return response.json()['value']

    def occupancy_percentage(self) -> int:
        """ Retrieve the current capacity utilization in percent. """

        # get HTTP response
        response = self.__retrieve_data('today')

        # convert response to JSON format and return the value of the "percentage" key
        for x in range(len(response.json())):
            # if the "current" key exists return percentage value
            if response.json()[x - 1]['current'] is True:
                return response.json()[x - 1]['percentage']

        # if the "current" key does not exist return 0
        return 0


def save_to_csv() -> str:
    """ Save the current visitor information to a csv file. """

    # dt_now stores current time
    dt_now = datetime.datetime.now()

    # convert datetime to string
    dt_now_str = dt_now.strftime("%m/%d/%Y, %H:%M:%S")

    feedback = f'{dt_now_str}:'

    for mysports_entry in MYSPORTS_ENTRIES:
        feedback += f'\n- {mysports_entry.name}: '

        # if the gym is open, retrieve visitor data
        if mysports_entry.is_open():
            # retrieve current gym occupation
            visitor_count = mysports_entry.visitor_count()
            occupancy_percentage = mysports_entry.occupancy_percentage()

            # if the retrieved data does not fulfill our requirements return error message
            if not isinstance(visitor_count, int) or visitor_count < 0:
                visitor_count = None
                feedback += f'[An error occurred while querying the data] '
            if not isinstance(occupancy_percentage, int) or not 0 <= occupancy_percentage <= 100:
                occupancy_percentage = None
                feedback += f'[An error occurred while querying the data] '

            # append datetime string and gym occupation to csvfile
            with open(f'{Path.home()}/gymstalker_data/{mysports_entry}.csv', 'a', newline='') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=',')
                datawriter.writerow([dt_now_str] + [visitor_count] + [occupancy_percentage])

            # return the visitor count and occupancy percentage
            feedback += f'{visitor_count} Visitors ({occupancy_percentage}%)'

        # if the gym is closed, return error message
        else:
            feedback += f'The studio is closed, no data available'

    # return feedback string
    return feedback


def job():
    """ Job to be executed in the specified time intervals. """

    # exit script if csv files do not exist
    for mysports_entry in MYSPORTS_ENTRIES:
        if not os.path.exists(f'{Path.home()}/gymstalker_data/{mysports_entry}.csv'):
            sys.exit()

    # call save_to_csv()
    feedback = save_to_csv()

    # print feedback to the console
    print(feedback)

    # print feedback to log file
    with open(f'../log.txt', 'w', newline='') as log:
        log.write(f'{feedback}')


def main():
    # read configuration file
    with open('../config.json') as config:
        for mysports_entry in json.load(config)['mysports_entries']:
            MYSPORTS_ENTRIES.append(MySportsEntry(name=mysports_entry['name'],
                                                  studio_id=mysports_entry['studio_id'],
                                                  studio_path=mysports_entry['studio_path'],
                                                  api_key=mysports_entry['api_key']))

    # create a new csv, if the file does not exist
    if not os.path.exists(f'{Path.home()}/gymstalker_data'):
        os.makedirs(f'{Path.home()}/gymstalker_data')
    for mysports_entry in MYSPORTS_ENTRIES:
        if not os.path.exists(f'{Path.home()}/gymstalker_data/{mysports_entry}.csv'):
            with open(f'{Path.home()}/gymstalker_data/{mysports_entry}.csv', 'w', newline='') as csvfile:
                csvfile.write('Time,Visitors,Percentage\n')

    # every 15 minutes job() is called through task scheduling
    schedule.every().hour.at(":00").do(job)
    schedule.every().hour.at(":15").do(job)
    schedule.every().hour.at(":30").do(job)
    schedule.every().hour.at(":45").do(job)

    # print feedback to the console
    print(f'Beginning to collect visitor information from...')
    for mysports_entry in MYSPORTS_ENTRIES:
        print(f'- {mysports_entry.name}: {MYSPORTS_URL}/studio/{mysports_entry.studio_path}')

    # loop so that the scheduling tasks keep on running all time
    while True:
        # checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
