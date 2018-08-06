import pandas as pd
from energyWork.py.bacnet_gateway_requests import get_value_and_units
import argparse
import tkinter as tk  # for python 3
import pygubu
import datetime
from time import sleep
from multiprocessing import Process, Value
import sys


# Import the config CSV
ahs_csv = pd.read_csv('../csv/ahs_air_wing.csv', na_filter=False, comment='#')

# Import the CSV that contains all the last known data
csv_co2_data = pd.read_csv('../csv/co2.csv')
csv_temp_data = pd.read_csv('../csv/temp.csv')


# Initialize global variables
wing = 'D'
floor = 3
last_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=60)
last_time2 = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)
print(last_time)

temp_mp = Value("d", 0)
co2_mp = Value("d", 0)


class Application:
    def __init__(self, master):

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('gui.ui')

        # 3: Create the widget using a master as parent
        self.main = builder.get_object('main', master)

        builder.connect_callbacks(self)

        self.avg_co2_out = builder.get_variable('avg_co2_out')
        self.avg_temp_out = builder.get_variable('avg_temp_out')

    def get_floor(self):
        # Get the value of floor_num
        global floor
        floor = self.builder.get_variable('floor_num').get()
        print("Floor Num: ", self.builder.get_variable('floor_num').get())
        print(floor)

        # Start the update process
        start_update(last_time, wing, floor)

    def get_wing(self):
        # Get the wing
        global wing
        wing = self.builder.get_variable('wing_var').get()
        print("Wing: ", self.builder.get_variable('wing_var').get())
        print(wing)

        # Start the update process
        start_update(last_time, wing, floor)

    def update_co2(self, co2):
        print(co2)
        self.builder.get_variable('avg_co2_out').set(str(co2))
        root.update()

    def update_temp(self, temp):
        print(temp)
        self.builder.get_variable('avg_temp_out').set(str(temp))
        root.update()

    def test(self):
        self.builder.get_variable('avg_temp_out').set(str(2))


# Setup Tkinter
root = tk.Tk()
app = Application(root)


def update_data(wng, flr, co2, temp):
    # Update data
    print("Updating Data")

    # Focus data selection to be of the specific floor and wing
    try:
        print("Wing - ", wng)
        print("Floor - ", flr)
        df_focus = ahs_csv[(ahs_csv['Wing'] == wng) & (ahs_csv['Floor'] == str(flr))]
        print(df_focus)
    except:
        print('Error Occurred')
        return

    temp_return = 0
    co2_return = 0
    df_rows = df_focus.count()

    # Iterate over the rows of the focused dataframe, getting temperature and CO2 values for each location
    for index, row in df_focus.iterrows():
        # Prints the target
        print("Facility - " + str(row['Facility']) + " | Room - " + str(row['Label']))

        # Retrieves the values
        temp_val, temp_units = retrieve_data(args, row['Facility'], row['Temperature'])
        co2_val, co2_units = retrieve_data(args, row['Facility'], row['CO2'])

        print("Room " + str(row['Label']) + " --> Temp - " + str(temp_val) + ", CO2 Lvl - " + str(co2_val))

        try:
            temp_return += float(temp_val)
            co2_return += float(co2_val)
        except TypeError:
            print("Encountered TypeError, exiting process")
            return

    # Finds the average temp and CO2 levels of the wing
    temp_return /= df_rows
    co2_return /= df_rows

    # Print the found values
    print(temp_return['Temperature'])
    print(co2_return['CO2'])

    temp.value = temp_return["Temperature"]
    co2.value = co2_return['CO2']

    return


def start_update(lasttime, wng, flr):
    print(lasttime)
    print(datetime.datetime.utcnow())
    # If 60 seconds have passed since the last update data
    print("Change in time: " + str((datetime.datetime.utcnow() - lasttime).seconds))

    if (datetime.datetime.utcnow() - lasttime).seconds >= 60:
        # Set the new last time
        global last_time
        last_time = datetime.datetime.utcnow()

        try:
            process_update_data = Process(target=update_data, args=(wng, flr, co2_mp, temp_mp))
            process_update_data.start()
            # update_data(wng, flr)
            print("Update started")
            return
        except KeyboardInterrupt:
            process_update_data.join()
            process_update_data.terminate()
            sys.exit(2)
    else:
        print("Update process already running")
        return


def retrieve_data(arguments, facility, value):
    '''
    :param arguments: The arguments to be passed in
    :param facility: Which facility at AHS to access
    :param value: The value to retrieve. Either CO2 or Temp
    :return:
    '''
    # Retrieve data from API
    try:
        data, units = get_value_and_units(facility, value, arguments.hostname, arguments.port)

        # Prepare to print
        data = float(data) if data else ''
        units = units if units else ''

        # Return data and units retrieved from server
        return data, units

    except:
        print("Unable to establish a connection with the server")
        sys.exit()


# Get hostname and port of BACnet Gateway
parser = argparse.ArgumentParser(description='Test BACnet Gateway', add_help=False)
parser.add_argument('-h', dest='hostname')
parser.add_argument('-p', dest='port')
args = parser.parse_args()


try:

    # print(ahs_csv[ahs_csv['Wing'] == 'A'])

    if __name__ == '__main__':
        # Start the update process, which calls the update_data function
        print("Starting update_data process")
        start_update(last_time, wing, floor)

        # Application.test(app)

        # Start the Tkinter frontend application
        print("Staring Tkinter application")

        while True:
            # try:
            #     t1 = open('tempfile_temp.txt', 'r')
            #     t2 = open('tempfile_co2.txt', 'r')
            #
            #     Application.update_co2(app, )
            #     Application.update_temp(app, )
            # except AttributeError:
            #     print("derp")

            if (datetime.datetime.utcnow() - last_time2).seconds >= 10:
                Application.update_co2(app, round(co2_mp.value, 1))
                Application.update_temp(app, round(temp_mp.value, 1))
                last_time2 = datetime.datetime.utcnow()

            root.update_idletasks()
            root.update()
            sleep(0.1)


except KeyboardInterrupt:
    print('Terminating Program')
    sys.exit()
