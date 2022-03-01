import csv
from werkzeug.security import generate_password_hash, check_password_hash

# cf = open('GTFS_SQL/trips2.csv', 'w')
# csv_out = csv.writer(cf, delimiter=',')
# file = open("GTFS_SQL/trips.csv")
# csvreader = csv.reader(file)
# header = next(csvreader)
# csv_out.writerow(['trip_id', 'route_id', 'password'])
# print(header)
# id=1
# for row in csvreader:
#     password_hash = generate_password_hash(row[0]+"pass", "sha256")
#     csv_out.writerow([row[0], row[1], password_hash])
#     id = id+1
# file.close()
# cf.close()

cf = open('GTFS_SQL/passengers.csv', 'w')
csv_out = csv.writer(cf, delimiter=',')
csv_out.writerow(['user_id', 'password', 'balance', 'currently_onboarded', 'trip_id', 'from_stop_id', 'onboarded_time'])
for x in range(1,10001):
    userid = 'user'+str(x)
    password_hash = generate_password_hash(userid+"pass", "sha256")
    csv_out.writerow([userid, password_hash, str(((x%208)-7)*5), 'false', '', '', ''])
cf.close()