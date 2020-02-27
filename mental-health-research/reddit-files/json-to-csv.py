import json
import csv
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--in", required=True,
   help="JSON file to convert")
ap.add_argument("-o", "--out", required=True,
   help="CSV file to create")
args = vars(ap.parse_args())

with open(args['in']) as json_file:
    json = json.load(json_file)

    with open(args['out'], 'w') as csv_file:
        csv_columns = set().union(*(d.keys() for d in json.values()))
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for row in json.values():
            writer.writerow(row)

