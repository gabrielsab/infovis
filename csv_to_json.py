import csv
import json
import glob

jc_filename_template = '/home/gabriel/dev/infovis/data/extracted/JC-{}-citibike-tripdata.csv'

def process_file(filename, station_data):
	with open(filename, 'r') as f:
		csv_reader = csv.reader(f)
		first = True
		for row in csv_reader:
			if first:
				first = False
				continue

			orig = row[3]
			dest = row[7]

			if orig == 'NULL' or dest == 'NULL':
				continue

			if orig not in station_data:
				station_data[orig] = {}
				station_data[orig]['name'] = row[4]
				station_data[orig]['lat']  = row[5]
				station_data[orig]['long'] = row[6]
				station_data[orig]['trips_outbound_count'] = 1
				station_data[orig]['trips_outbound'] = { dest: 1 }
				station_data[orig]['trips_inbound_count'] = 0
				station_data[orig]['trips_inbound'] = {}
			else:
				station_data[orig]['trips_outbound_count'] += 1
				if dest in station_data[orig]['trips_outbound']:
					station_data[orig]['trips_outbound'][dest] += 1
				else:
					station_data[orig]['trips_outbound'][dest] = 1

			if dest not in station_data:
				station_data[dest] = {}
				station_data[dest]['name'] = row[8]
				station_data[dest]['lat']  = row[9]
				station_data[dest]['long'] = row[10]
				station_data[dest]['trips_outbound_count'] = 0
				station_data[dest]['trips_outbound'] = { }
				station_data[dest]['trips_inbound_count'] = 1
				station_data[dest]['trips_inbound'] = { orig: 1}
			else:
				station_data[dest]['trips_inbound_count'] += 1
				if orig in station_data[dest]['trips_inbound']:
					station_data[dest]['trips_inbound'][orig] += 1
				else:
					station_data[dest]['trips_inbound'][orig] = 1

filenames = glob.glob('/home/gabriel/dev/infovis/data/extracted/*.csv')
filenames.sort()

for filename in filenames:
	if '/JC-' in filename:
		continue

	year_month = filename.split('-')[0].split('/')[-1]

	print(year_month)

	station_data = {}

	process_file(filename, station_data)

	jc_filename = jc_filename_template.format(year_month)
	if jc_filename in filenames:
		process_file(jc_filename, station_data)

	with open('/home/gabriel/dev/infovis/data/processed/citibike_trips_monthly_{}.json'.format(year_month), 'w') as out:
		out.write(json.dumps(station_data, indent=4))