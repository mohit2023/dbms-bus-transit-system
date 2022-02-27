import csv
from werkzeug.security import generate_password_hash, check_password_hash

cf = open('GTFS_SQL/conductors.csv', 'a')
csv_out = csv.writer(cf, delimiter=',')
file = open("GTFS_SQL/trips.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
id=1
for row in csvreader:
    csv_out.writerow(['conductor_'+str(id) ,row[0]])
    id = id+1
file.close()
cf.close()

cf = open('GTFS_SQL/passengers.csv', 'a')
csv_out = csv.writer(cf, delimiter=',')
for x in range(1,10001):
    csv_out.writerow(['user_'+str(x) , str(((x%208)-7)*5), 'false', '', '', ''])
cf.close()

cf = open('GTFS_SQL/users.csv', 'a')
csv_out = csv.writer(cf, delimiter=',')
password_hash = generate_password_hash("adminpass", "sha256")
csv_out.writerow(['DIMTS', password_hash, 'admin'])
file = open("GTFS_SQL/conductors.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
id=1
for row in csvreader:
    password_hash = generate_password_hash(row[0]+"pass", "sha256")
    csv_out.writerow([row[0], password_hash, 'conductor'])
    id = id+1
file.close()
file = open("GTFS_SQL/passengers.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
id=1
for row in csvreader:
    password_hash = generate_password_hash(row[0]+"pass", "sha256")
    csv_out.writerow([row[0], password_hash, 'passenger'])
    id = id+1
file.close()
cf.close()