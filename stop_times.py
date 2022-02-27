import csv

csv_out = csv.writer(open('GTFS/stop_times.csv', 'w'), delimiter=',')

f = open('GTFS/stop_times.txt')
for line in f:
  vals = line.split(',')
  vals[4] = vals[4][:-1]
  #print(vals)
  csv_out.writerow([vals[0], vals[1], vals[2], vals[4], vals[3]])
  break
for line in f:
  vals = line.split(',')
  vals[4] = vals[4][:-1]
  #print(vals)
  if (vals[1]>'23:59:59'):
    vals[1] = '0'+str(int(vals[1][0:2])%24)+vals[1][2:8]
  if (vals[2]>'23:59:59'):
    vals[2] = '0'+str(int(vals[2][0:2])%24)+vals[2][2:8]
  csv_out.writerow([vals[0], vals[1], vals[2], vals[4], vals[3]])
f.close()