import itertools
import sys
import threading
import time
import requests
import keyboard
import toml


def timer():
    seconds = 0
    minutes = 0
    hours = 12
    days = 0
    while seconds >= 0:
        time.sleep(0.5)
        seconds += 0.5
        if seconds == 60:
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
                str(days) + ' days, ' + str(hours) + ' hours, ' + str(
                    minutes) + ' minutes, and ' + str(int(seconds)) + ' seconds')
        global time_awake
        global days_awake
        time_awake = time_active
        days_awake = days


counter = "plants"
line_count = 0
with open(counter, "r") as files:
    for _ in files:
        line_count += 1

with open("config.toml") as f:
    config = toml.load(f)
    token = config["token"]
    channel = config["ChannelID"]


def countdown(start):
    return list(reversed(range(start + 1)))


def main():
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
                    time.sleep(0.5)
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
                    for plant in plants.readlines():
                        if keyboard.is_pressed('E'):
                            print("Ok, the farmer was killed")
                            time.sleep(2)
                            exit()
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
                        time.sleep(0.5)
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
                                    loop_counter) + ' time')
                                if loop_counter_message == "Y":
                                    payload = {
                                        'content': "So far, the farmer has watered your plants " + str(loop_counter) +
                                                   ' time and has been awake for ' + str(days_awake) + ' days'

                                    }
                                    header = {
                                        'authorization': token
                                    }
                                    _ = requests.post(channel, data=payload, headers=header)
                            else:
                                print("So far, the farmer has watered your plants " + str(
                                    loop_counter) + ' times')
                                if loop_counter_message == "Y":
                                    payload = {
                                        'content': "So far, the farmer has watered your plants " + str(
                                            loop_counter) + ' times and has been awake for ' + str(days_awake) + ' days'
                                    }
                                    header = {
                                        'authorization': token
                                    }
                                    _ = requests.post(channel, data=payload, headers=header)
                            done = False

                            def animate():
                                tl = 905
                                for c in itertools.cycle(['|', '/', '-', '\\']):
                                    if done:
                                        break
                                    sys.stdout.write('\rThe farmer has been awake for ' + time_awake + '. Waiting for '
                                                     + str(int(tl)) + ' seconds until next watering  cycle.' + c)
                                    sys.stdout.flush()
                                    time.sleep(0.5)
                                    tl -= 0.5
                                sys.stdout.write('\rDone!     ')

                            t = threading.Thread(target=animate)
                            t.start()
                            time.sleep(905)
                            done = True
                            if keyboard.is_pressed('E'):
                                print("   Ok, the farmer was killed")
                                time.sleep(2)
                                exit()

        elif start == "N":
            print("Ok, the farmer will stay asleep for now")
            time.sleep(2)
            exit()
        else:
            print("Invalid command")


if __name__ == '__main__':
    main()
