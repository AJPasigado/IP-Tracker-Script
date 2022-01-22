"""
IP Tracker Script

Created by: AJ Pasigado
Created on January 23, 2022
"""

import csv
import os
import sys
import glob
import ast


def csv_reader(file_name, columns_to_record, encoding,
               environment_column, env_name, debug, add_env=False):
    """
    Open the file and extract each value of each column from each row.

    Parameters
    ----------
    file_path : str
        File path to the combined file.
    columns_to_record : list
        List of columns to be recorded.
    encoding : str
        Specify another encoding for the input and
        output file.
    environment_column : str
        The column name of the environment to be recorded.
    env_name : str
        The name of the current environemnt being checked.
    debug : bool
        Turn on warning messages when running the code.
    add_env : bool
        Optional Parameter. Flag if environment column is also
        needed to be added on each returned row.

    Returns
    ------
    values_to_return : list
        List of dictionaries of each columns to be recorded of
        each row. Environment is also appended on each entry
        depending on add_env parameter

    """

    values_to_return = []

    try:
        with open(file_name, "r", encoding=encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                row_values = {}

                for column in columns_to_record:
                    row_values[column] = row.get(column)

                    if row_values[column] and add_env:
                        # Add environemt column if specified
                        row_values[environment_column] = env_name
                    elif not row_values[column] and debug:
                        # If no value is found
                        print(f'WARNING: Value for {column} in row {row} of \
                                {file_name} not found.')

                values_to_return.append(row_values)
    except PermissionError as exception:
        print(exception)

    return values_to_return


def csv_writer(file_path, extracted_values, recorded_values,
               columns_to_record, allow_duplicates, encoding):
    """
    Go through all of the extracted values and write them to
    the combined csv file. (Duplicates in the results will then be
    handled unless otherwise specified).

    Parameters
    ----------
    file_path : str
        File path to the combined file.
    extracted_values : list
        List of Dictionaries all extracted values.
    recorded_values : list
        List of Dictionaries all previously recorded values from combined file.
    columns_to_record : list
        List of headers/columns to be recorded
    allow_duplicates : bool
        Allow duplciates to be recorded or not.
    encoding : str
        Specify another encoding for the input and
        output file.

    Returns
    ------
    None

    """

    file_exists = os.path.exists(file_path)

    try:
        with open(file_path, mode='a',  encoding=encoding, newline='') as file:
            writer = csv.DictWriter(file, delimiter=',',
                                    fieldnames=columns_to_record)

            if not file_exists:
                writer.writeheader()

            for values in extracted_values:
                if allow_duplicates or (values not in recorded_values
                                        and not allow_duplicates):
                    recorded_values.append(values)
                    writer.writerow(values)
    except PermissionError as exception:
        print(exception)


def ip_tracker(env_name, columns_to_record=['Source IP'],
               combined_file='Combined.csv', environment_column='Environment',
               allow_duplicates=False, encoding='utf-8-sig',
               debug=False):

    """
    Loops through all of the possible files with the environment name and
    consolidates the results. It consists of the values specified in
    the columns to be recorded. The reuslts will then be written in a CSV file
    (Duplicates in the results will then be handled unless
    otherwise specified).

    Parameters
    ----------
    env_name : str
        Name of the environment to be checked. This will also serve as
        the prefix of the file names to be checked.
    columns_to_record : list
        Optional parameter. You can specify which columns should be recorded.
        Default value is to check only "Source IP" column.
    combined_file : str
        Optional Parameter. File name of the output file.
        Default value is "Combined.csv".
    environment_column : str
        Optional Parameter. You can specify another name for the Environement
        column that will be recorded.
        Default value is "Environment".
    allow_duplicates : bool
        Optional Parameter. Allow duplciates to be recorded or not.
        Default value is False.
    encoding : str
        Optional Parameter. Specify another encoding for the input and
        output file.
        Default value is "utf-8-sig".
    debug : bool
        Optional Parameter. Turn on warning messages when running the code.
        Default value is False.

    Returns
    ------
    None

    """

    # Get the list of files starting in env_name*.csv
    files = glob.glob(os.path.join(sys.path[0], env_name + '*.csv'))
    # Use sum to consoidate all list of dictionaries into a single list
    extracted_values = sum([csv_reader(file, columns_to_record, encoding,
                            environment_column, env_name, debug, True)
                            for file in files], [])

    if not files and debug:
        print('WARNING: No files detected')

    # Get the output file
    combined_file_name = glob.glob(os.path.join(sys.path[0], combined_file))
    combine_file_values = [csv_reader(file,
                           columns_to_record + [environment_column], encoding,
                           environment_column, env_name, debug)
                           for file in combined_file_name]
    recorded_values = sum(combine_file_values, [])

    if not combined_file_name and debug:
        print('INFO: No combined file detected')

    if not combined_file_name:
        # If output file is not found, create a new file
        combined_file_name = [os.path.join(sys.path[0], combined_file)]

    if len(extracted_values) > 0:
        csv_writer(combined_file_name[0], extracted_values, recorded_values,
                   columns_to_record + [environment_column],
                   allow_duplicates, encoding)
    elif debug:
        print('INFO: No lines to be written')


var = input().split(',')

params = {}
for index, value in enumerate(var):
    if index == 0 and type(value) == str:
        params['env_name'] = value
    elif index == 2 and type(value) == str:
        params['combined_file'] = value
    elif index == 3 and type(value) == str:
        params['environment_column'] = value
    elif index == 5 and type(value) == str:
        params['encoding'] = value
    else:
        try:
            value = ast.literal_eval(value)
            if index == 1 and type(value) == list:
                params['columns_to_record'] = value
            elif index == 4 and type(value) == bool:
                params['allow_duplicates'] = value
            elif index == 6 and type(value) == bool:
                params['debug'] = value
        except ValueError:
            print(f'Value error for parameter {index}')

ip_tracker(**params)
