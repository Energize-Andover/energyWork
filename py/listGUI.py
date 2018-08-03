import pandas as pd
from energyWork.py.bacnet_gateway_requests import get_value_and_units
import argparse
import tkinter as tk  # for python 3
import pygubu
from time import sleep
from multiprocessing import Process
import sys

# Import the config CSV
ahs_csv = pd.read_csv('../csv/ahs_air_wing.csv', na_filter=False, comment='#')

# Initialize global variables
wing = 'D'
floor = 3


class Application:
    def __init__(self, master):

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('gui.ui')

        # 3: Create the widget using a master as parent
        self.main = builder.get_object('main', master)

        builder.connect_callbacks(self)

    def get_floor(self):
        # Get the value of floor_num
        global floor
        floor = self.builder.get_variable('floor_num').get()
        print("Floor Num: ", self.builder.get_variable('floor_num').get())
        print (floor)

    def get_wing(self):
        # Get the wing
        global wing
        wing = self.builder.get_variable('wing_var').get()
        print("Wing: ", self.builder.get_variable('wing_var').get())
        print(wing)


def update_data():
    while True:

        print("Updating Data")

        # Focus data selection to be of the specific floor and wing
        try:
            global wing
            global floor
            print("Wing - ", wing)
            print("Floor - ", floor)
            df_focus = ahs_csv[(ahs_csv['Wing'] == wing) & (ahs_csv['Floor'] == str(floor))]
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

            temp_return += temp_val
            co2_return += co2_val

        # Finds the average temp and CO2 levels of the wing
        temp_return /= df_rows
        co2_return /= df_rows

        print(temp_return)
        print(co2_return)


        # root.update()
        sleep(3)


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
        # Setup Tkinter
        root = tk.Tk()
        app = Application(root)

        # Start the update process, which calls the update_data function
        print("Starting update_data process")
        process_update_data = Process(target=update_data)
        process_update_data.start()
        # process_update_data.join()

        # Start the Tkinter frontend application
        print("Staring Tkinter application")
        root.mainloop()


except KeyboardInterrupt:
    print('Terminating Program')
    process_update_data.terminate()
    sys.exit()
