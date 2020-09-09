"""

    Assigns days employees can come into the office.

    ***TO IMPROVE
        move location capacities and points parameters to a config file

"""

import numpy as np
import pandas as pd
from create_dummy_data import create_dummy_data as cdd

# Specify capacity at each location
loc_caps = {'PS1': 10, 'PS2': 10, 'PS3': 10, 'PS4': 10, 'PS5': 5}

# Specify weights given to values in each field
weights_gcb = {2: 80, 3: 60, 4: 40, 5: 0, 6: 0}
weights_cat = {'L': 0, 'R': -10}
weights_pr = {0: 0, 1: 10, 2: 50, 3: 90}


def assign_days(n=100, export_to_csv=False):
    data = pd.read_csv('dummy_data.csv')

    # Assign points for each individual depending on values in fields
    # If preference or priority rating is zero, make points equal zero
    list_points = []
    for i, j in data.iterrows():
        if j['PR'] == 0 or j['Pref'] == 0:
            list_points.append(0)
        else:
            list_points.append(
                weights_gcb[j['GCB']] +
                weights_cat[j['Cat']] +
                weights_pr[j['PR']])
    data['Points'] = list_points

    # Get list of all locations
    list_locs = data['Loc'].unique()

    # Create output dataframe
    assigned_days = pd.DataFrame(index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])

    for loc in list_locs:
        data_loc = data.loc[data['Loc'] == loc]
        data_loc.sort_values(by=['Points', 'Pref'],
                             inplace=True,
                             ascending=False)
        data_loc = data_loc.reset_index()

        # Allocate individuals to days of the week
        # Depending on points and location capacities
        list_mon, list_tue, list_wed, list_thu, list_fri = ([] for i in range(5))

        for i, j in data_loc.iterrows():
            add_mon = add_tue = add_wed = add_thu = add_fri = True
            for n in np.arange(j['Pref']):

                if len(list_mon) < loc_caps[loc] and add_mon:
                    list_mon.append(j['ID'])
                    add_mon = False
                elif len(list_tue) < loc_caps[loc] and add_tue:
                    list_tue.append(j['ID'])
                    add_tue = False
                elif len(list_wed) < loc_caps[loc] and add_wed:
                    list_wed.append(j['ID'])
                    add_wed = False
                elif len(list_thu) < loc_caps[loc] and add_thu:
                    list_thu.append(j['ID'])
                    add_thu = False
                elif len(list_fri) < loc_caps[loc] and add_fri:
                    list_fri.append(j['ID'])
                    add_fri = False
                else:
                    break

            if len(list_fri) == loc_caps[loc]:
                break

        assigned_days[loc] = [list_mon, list_tue, list_wed, list_thu, list_fri]

    if export_to_csv:
        assigned_days.to_csv('assigned_days.csv')

    return assigned_days


if __name__ == '__main__':
    assign_days()
