import itertools
import sys
import threading
import time
import requests
import keyboard
import toml
from urllib.request import urlopen


def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=5)
        return True
    except:
        return False


def internet_on1():
    try:
        urlopen('http://216.58.192.142', timeout=5)
        return True
    except:
        return False


def timer():
    seconds = 0
    minutes = 0
    hours = 0
    days = 0
    while seconds >= 0:
        time.sleep(0.5)
        seconds += 0.5
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
        time_active = (
                str(days) + ' days, ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, and ' + str(int(seconds))
                + ' seconds')
        global time_awake
        global days_awake
        time_awake = time_active
        days_awake = days


def file_finder():
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
                if plant_name == 0:
                    print('Your plants list has been updated. The farmer will now kill itself, please restart the '
                          'farmer for your changes to take effect.')
                    pf.close()
                    time.sleep(4)
                    exit()

                else:
                    add_plants()
            add_plants()

        elif new_p_file == 'N':
            print('Ok, if you wish to use the farmer please create a plants file called plants.txt and save it in the '
                  'same folder as the program. Write one plant name per line and nothing else.')
            time.sleep(5)
            exit()
        else:
            print('Invalid command, estupida idiota... ')


'''with open("config.toml") as f:
    config = toml.load(f)
    token = config["token"]
    channel = config["ChannelID"]'''


def config_finder():
    try:
        with open("config.toml", 'r') as f:
            config = toml.load(f)
            global token
            global channel
            token = config["token"]
            channel = config["ChannelID"]
    except:
        print('No setup file found. Please insert your discord token and channel ID')
        with open("config.toml", 'a') as f:
            new_token = input('Please insert your Discord token. ')
            new_channel = input('Please insert the ID of the channel where you want the farmer to be active: ')
            f.write('token = "' + new_token + '"')
            f.write('\n')
            f.write('ChannelID = "' + new_channel + '"')
            print('Your setup is now complete. The farmer will kill itself one last time before you can start using it.'
                  'have a nice day :)')
            time.sleep(4)
            exit()

def countdown(start):
    return list(reversed(range(start + 1)))


def main():
    file_finder()
    config_finder()
    while True:
        start = input("Would you like to wake up the farmer?(Y/N) ").upper()
        if start == "Y":
            threading.Thread(target=timer).start()

            loop_counter_message = input(
                "Would you like the farmer to send messages to your channel telling you how many "
                "times he has watered your plants? (Y/N) ").upper()
            done = False

            def animate():
                for c in itertools.cycle(['.', '..', '...', '....', '.....']):
                    if done:
                        break
                    sys.stdout.write('\rWaking up the farmer ' + c)
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write('\rDone! The farmer is awake and will now start watering your plants!     ')
                time.sleep(0.5)

            t = threading.Thread(target=animate)
            t.start()
            time.sleep(5)
            done = True

            loop_counter = 0
            while loop_counter >= 0:
                payload_counter = 0
                while payload_counter < line_count:
                    plants = open("plants", "r")
                    time.sleep(2)
                    print("")
                    internet_on1()
                    if internet_on1():
                        for plant in plants.readlines():
                            internet_on()
                            if internet_on():
                                if plant != '':
                                    payload = {
                                        'content': "p.water " + plant
                                    }
                                    print("Watering " + plant + "...")
                                    if keyboard.is_pressed('E'):
                                        print("Ok, the farmer was killed")
                                        time.sleep(2)
                                        exit()

                                    header = {
                                        'authorization': token
                                    }
                                    _ = requests.post(channel, data=payload, headers=header)
                                    payload_counter += 1
                                    time.sleep(1)
                                if payload_counter == line_count:
                                    payload = {
                                        'content': "p.exp"
                                    }
                                    if keyboard.is_pressed('E'):
                                        exit()
                                    header = {
                                        'authorization': token
                                    }
                                    _ = requests.post(channel, data=payload, headers=header)
                                    loop_counter += 1
                                    print("")
                                    print("All your plants have been watered!")
                                    print("")
                                    print("If at any time you wish to stop the farmer, press [E] for 1 second")
                                    if keyboard.is_pressed('E'):
                                        print("   Ok, the farmer was killed")
                                        time.sleep(2)
                                        exit()
                                    if loop_counter == 1:
                                        print("So far, the farmer has watered your plants " + str(
                                            loop_counter) + " time.")
                                        if loop_counter_message == "Y":
                                            payload = {
                                                'content': "So far, the farmer has watered your plants " + str(
                                                    loop_counter) + " time, and has been awake for   " + str(
                                                    days_awake) + ' days.'
                                            }
                                            header = {
                                                'authorization': token
                                            }
                                            _ = requests.post(channel, data=payload, headers=header)
                                    else:
                                        print("So far, the farmer has watered your plants " + str(
                                            loop_counter) + " times.")
                                        if loop_counter_message == "Y":
                                            payload = {
                                                'content': "So far, the farmer has watered your plants " + str(
                                                    loop_counter) + " times, and has been awake for  " + str(
                                                    days_awake) + ' days.'

                                            }
                                            header = {
                                                'authorization': token
                                            }
                                            _ = requests.post(channel, data=payload, headers=header)
                                    done = False

                                    def animate():
                                        tl = 895
                                        for c in itertools.cycle(['|', '/', '-', '\\']):
                                            if done:
                                                break
                                            sys.stdout.write(
                                                '\rThe farmer has been awake for ' + time_awake + '. Waiting for '
                                                + str(int(tl)) + ' seconds until next watering  cycle.' + c)
                                            sys.stdout.flush()
                                            time.sleep(0.5)
                                            tl -= 0.5
                                        sys.stdout.write('\rDone!')

                                    t = threading.Thread(target=animate)
                                    t.start()
                                    time.sleep(895)
                                    done = True
                                    if keyboard.is_pressed('E'):
                                        print("   Ok, the farmer was killed")
                                        time.sleep(2)
                                        exit()
                            else:
                                print('No internet connection established, trying again soon')
                                time.sleep(1)
                                payload_counter -= 1
                                internet_on1()
                    else:
                        print('No internet connection established, trying again soon')
                        time.sleep(1)
                        payload_counter -= 1
                        internet_on1()

        elif start == "N":
            print("Ok, the farmer will stay asleep for now")
            time.sleep(2)
            exit()
        else:
            print("Invalid command")


if __name__ == '__main__':
    main()
