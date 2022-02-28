--routes--
SELECT stop_id,stop_name FROM stops ORDER BY stop_name ASC;

--register--
INSERT INTO users (user_id, password, user_type) VALUES ('xxx','xxx','xxx');

--search route--

--onboarding--
/*after logging in page reaches for user_id*/
SELECT * from passengers where user_id = 'xxx';
/*using python code check for balanace, make currently_onboarded = 'True' and trip_id, from_stop_id, onbo.. as per requested.*/
UPDATE passengers SET balanace = 'xxx', currently_onboarded = 'true', trip_id = 'xxx', from_stop_id = 'xxx', onboarded_time = 'xxx' where user_id = 'xxx';

--deboarding--
SELECT * from passengers where user_id = 'xxx';
/*upon deboarding at a bus stop, calculate bus rate*/
SELECT price from fares,trips,passengers where from_stop_id = 'xxx' AND to_stop_id = 'xxx' AND passengers.trip_id = trips.trip_id AND fares.route_id = trips.route_id;
/*calculate balance*/
UPDATE passengers SET balanace = 'xxx', currently_onboarded = 'false', trip_id = '', from_stop_id = '', onboarded_time = '' where user_id = 'xxx';
