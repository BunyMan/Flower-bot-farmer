import sys
from urllib.request import urlopen
import toml
import time
import threading
import itertools
import requests


def internet_on():  # checks for internet connection
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except:
        print('No internet connection established')
        return False


def timer():  # starts once the program is started
    try:
        with open('time_keeper', 'r')as f:  # opens a time_keeper file if it already exists
            tk = toml.load(f)
            seconds = tk["seconds"]
            minutes = tk["minutes"]
            hours = tk["hours"]
            days = tk["days"]
            f.close()
            while True:
                time.sleep(1)
                seconds += 1
                if seconds == 59:
                    minutes += 1
                    seconds = 0
                if minutes == 60:
                    hours += 1
                    minutes = 0
                    seconds = 0
                if hours == 24:
                    days += 1
                    hours = 0
                    minutes = 0
                    seconds = 0
                global time_active
                time_active = (
                        str(days) + ' days, ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, and ' +
                        str(int(seconds)) + ' seconds')
                with open('time_keeper',
                          'w') as tk:  # updates the time_keeper file so that is doesn't loose time once the program
                    # is closed
                    tk.write('seconds = ' + str(seconds) + '\n')
                    tk.write('minutes = ' + str(minutes) + '\n')
                    tk.write('hours = ' + str(hours) + '\n')
                    tk.write('days = ' + str(days) + '\n')
    except:  # Creates a new time_keeper file if one isn't found
        with open("time_keeper", 'w') as f:
            s = 0
            m = 0
            h = 0
            d = 0
            f.write('seconds = ' + str(int(s)) + '\n')
            f.write('minutes = ' + str(int(m)) + '\n')
            f.write('hours = ' + str(int(h)) + '\n')
            f.write('days = ' + str(int(d)) + '\n')
            f.close()


def plant_finder():
    try:
        global line_count
        line_count = 0
        with open('plants', "r") as files:
            for _ in files:
                line_count += 1
    except:
        new_p_file = input('No plants file found. Would you like to create one?(Y/N) ').upper()
        if new_p_file == 'Y':
            pf = open('plants', 'w+')
            print('Plants file successfully created. Please insert your plants name one per line.')

            def add_plants():
                plant_name = pf.write(input('Plant name: '))
                pf.write('\n')
                if plant_name == 0 or plant_name == '' or plant_name == ' ':
                    print('Your plants list has been updated!')
                    pf.close()

                else:
                    add_plants()

            add_plants()
        elif new_p_file == 'N':
            print('Ok, if you wish to use the farmer please create a plants file called plants.txt and save it in the '
                  'same folder as the program. Write one plant name per line and nothing else.')
            time.sleep(5)
            exit()
        else:
            print('Nao sabes ler?, sim ou nao?')
            plant_finder()


def config_finder():
    try:
        with open('config.toml', 'r') as f:
            config = toml.load(f)
            global token
            global channel
            token = config['token']
            channel = config['ChannelID']
    except:
        print('No setup file found. Please insert your discord token and channel ID')
        with open("config.toml", 'a') as f:
            new_token = input('Please insert your Discord token. ')
            new_channel = input('Please insert the ID of the channel where you want the farmer to be active: ')
            f.write('token = "' + new_token + '"')
            f.write('\n')
            f.write('ChannelID = "' + new_channel + '"')
            print('Your setup is now complete! The farmer will kill itself one last time before you can start using it.'
                  ' have a nice day :)')
            time.sleep(4)
            exit()


def main():
    global lcm
    plant_finder()
    config_finder()
    while True:
        start = input('Would you like to start the Farmer?(Y/N)').upper()
        if start == 'Y':
            threading.Thread(target=timer).start()
            plant_finder()
            loop_counter_message = input("Would you like the farmer to send messages to your channel telling you how"
                                         " many times he has watered your plants? (Y/N) ").upper()
            if loop_counter_message == 'Y':
                lcm = 1
            elif loop_counter_message == 'N':
                lcm = 0
            else:
                print('Nao sabes ler? Sim ou Nao?')
            done = False

            def animate():
                for c in itertools.cycle(['.', '..', '...', '....', '.....']):
                    if done:
                        break
                    sys.stdout.write('\rWaking up the farmer' + c)
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write('\rDone! The farmer is awake and will now start watering your plants!')
                time.sleep(0.5)

            t = threading.Thread(target=animate)
            t.start()
            time.sleep(5)
            done = True
            loop_counter = 0
            while True:
                payload_counter = 0
                while payload_counter < line_count:
                    with open('plants', 'r') as f:
                        time.sleep(1)
                        print('\n')
                        if internet_on():
                            try:
                                for plant in f.readlines():
                                    if plant != 0 or plant != '' or plant != ' ':
                                        payload = {
                                            'content': 'p.water ' + plant
                                        }
                                        print('Watering ' + plant + '...')
                                        header = {
                                            'authorization': token
                                        }
                                        _ = requests.post(channel, data=payload, headers=header)
                                        payload_counter += 1
                                        time.sleep(1)
                                    if payload_counter == line_count:
                                        payload = {
                                            'content': 'p.exp'
                                        }
                                        header = {
                                            'authorization': token
                                        }
                                        _ = requests.post(channel, data=payload, headers=header)
                                        loop_counter += 1
                                        print('\n')
                                        print('All your plants have been watered')
                                        print('\n')
                                        if loop_counter == 1:
                                            print('So far the farmer has watered your plants 1 time.')
                                            if lcm == 1:
                                                payload = {
                                                    'content': 'So far  the farmer has watered your plants 1 time.'
                                                }
                                                header = {
                                                    'authorization': token
                                                }
                                                _ = requests.post(channel, data=payload, headers=header)
                                        else:
                                            print('So far the farmer has watered your plants ' + str(
                                                loop_counter) + ' times, and has been awake for ' + str(time_active))
                                            if lcm == 1:
                                                payload = {
                                                    'content': 'So far the farmer has watered your plants ' + str(
                                                        loop_counter) + ' times, and has been awake for ' + str(time_active)

                                                }
                                                header = {
                                                    'authorization': token
                                                }
                                                _ = requests.post(channel, data=payload, headers=header)
                                        done = False

                                        def animate():
                                            tl = 900
                                            for c in itertools.cycle(['|', '/', '-', '\\']):
                                                if done:
                                                    break
                                                sys.stdout.write(
                                                    '\rThe farmer has been awake for ' + str(time_active) + '. Waiting for '
                                                    + str(int(tl)) + ' seconds until next watering cycle. ' + c)
                                                sys.stdout.flush()
                                                time.sleep(0.5)
                                                tl -= 0.5
                                            sys.stdout.write('\nDone')

                                        t = threading.Thread(target=animate)
                                        t.start()
                                        time.sleep(900)
                                        done = True
                            except:
                                print('An unknown error occurred, trying again soon.')
                                time.sleep(3)
                                payload_counter -= 1
                                internet_on()
                        else:
                            print('No internet connection established, trying to connect again soon')
                            time.sleep(3)
                            payload_counter -= 1
                            internet_on()
        elif start == 'N':
            print('Ok, the farmer will stay asleep for now')
            time.sleep(2)
            exit()
        else:
            print('Nao sabes ler? sim ou nao?')


if __name__ == '__main__':
    main()
