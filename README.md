# IP-Tracker-Script
#### Consolidates all Source IP from different environment files to a single file

## How to use:
This script is ran using the command
```sh
python ip_tracker.py -e "Environment Name"
```
This script gets all files that start with "Environment Name" (e.g. "Environment Name 1.csv", "Environment Name 2.csv") and consolidates all "Source IP" column into one Combined.csv file.

## Limitations
All files needed to be processed (The csv files including the combined.csv file and the unit test script) should be on the same directory with the ip_tracker.py.

## Running the Unittest:
This script is ran using the command
```sh
python test_ip_tracker.py
```

## Optional Parameters:
You can use any of these parameters to customize your experience
| Command | Description | Default Value |
| ------ | ------ | ------ |
| --combined_file | Specify the file name of the combined file. | Combined.csv |
| --environment_column | Specify the name of the environment column in the combined file | Environment |
| --encoding | Specify the encoding of the csv files | utf-8-sig
| --columns_to_record | Specify which columns should be checked and recorded. Should be a string spearated by comma | 'Source IP'
| --allow_duplicates | Flag to check if duplciates should be recorded or disregarded | False
| --debug | Flag if info and warning messages should be shown | False

Example of a customized command

```sh
python ip_tracker.py -e "Environment Name" --combined_file Consolidated.csv --environment_column "Asia Prod" --columns_to_record "Source IP, Count" --allow_duplicates True --debug True
```
