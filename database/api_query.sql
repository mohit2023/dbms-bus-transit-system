--routes--
/*NO RECURSION ONLY ROUTES OVER SAME TRIP*/
-- WITH RECURSIVE inter_trip(trip_id,stop_id,hop) AS
--         (SELECT from_trip_ids.trip_id,stop_id,0
--         FROM from_trip_ids, stop_times
--         WHERE from_trip_ids.trip_id = stop_times.trip_id
--     UNION
--         SELECT R2.trip_id,R2.stop_id,R1.hop+1
--         FROM inter_trip AS R1, stop_times AS R2, to_trip_ids AS R3
--         WHERE R1.stop_id = any() AND R2.trip_id = R3.trip_id AND hop<0
--         ),

WITH from_trip_ids AS(
    SELECT trips.trip_id, arrival_time, route_id
    FROM trips, stop_times
    WHERE stop_times.stop_id = 23 AND stop_times.trip_id = trips.trip_id
),

to_trip_ids AS(
    SELECT trips.trip_id
    FROM trips, stop_times, from_trip_ids
    WHERE stop_times.stop_id = 100 AND stop_times.trip_id = trips.trip_id AND stop_times.departure_time >= from_trip_ids.arrival_time
)

SELECT inter_trip.trip_id
FROM inter_trip, to_trip_ids
WHERE inter_trip.trip_id = to_trip_ids.trip_id
ORDER BY trip_id
LIMIT 10;


-- WITH from_trip_ids AS(
--     SELECT trips.trip_id, arrival_time, route_id
--     FROM trips, stop_times
--     WHERE stop_times.stop_id = 23 AND stop_times.trip_id = trips.trip_id
-- ),

-- to_trip_ids AS(
--     SELECT trips.trip_id
--     FROM trips, stop_times, from_trip_ids
--     WHERE stop_times.stop_id = 100 AND stop_times.trip_id = trips.trip_id AND stop_times.departure_time >= from_trip_ids.arrival_time
-- )

-- SELECT from_trip_ids.trip_id, route_id
-- FROM from_trip_ids, to_trip_ids
-- WHERE from_trip_ids.trip_id = to_trip_ids.trip_id
-- ORDER BY trip_id
-- LIMIT 10;





-- WITH RECURSIVE Reaches_two_hops(source_station_name,destination_station_name, hop) AS
--         (SELECT source_station_name, destination_station_name, 0
--         FROM train_info
--         WHERE source_station_name = 'KURLA' AND train_no = 97131
--     UNION ALL
--         SELECT R1.source_station_name, R2.destination_station_name, R1.hop+1
--         FROM Reaches_two_hops AS R1, train_info AS R2
--         WHERE R1.destination_station_name = R2.source_station_name AND R1.hop <= 1
--         )
-- SELECT DISTINCT destination_station_name
-- FROM Reaches_two_hops
-- ORDER BY destination_station_name;






-- --register--
-- INSERT INTO users (user_id, password, user_type) VALUES ('xxx','xxx','xxx');


-- --onboarding--
-- /*after logging in page reaches for user_id*/
-- SELECT * from passengers where user_id = 'xxx';
-- /*using python code check for balanace, make currently_onboarded = 'True' and trip_id, from_stop_id, onbo.. as per requested.*/
-- UPDATE passengers SET balanace = 'xxx', currently_onboarded = 'true', trip_id = 'xxx', from_stop_id = 'xxx', onboarded_time = 'xxx' where user_id = 'xxx';

-- --deboarding--
-- SELECT * from passengers where user_id = 'xxx';
-- /*upon deboarding at a bus stop, calculate bus rate*/
-- SELECT price from fares,trips,passengers where from_stop_id = 'xxx' AND to_stop_id = 'xxx' AND passengers.trip_id = trips.trip_id AND fares.route_id = trips.route_id;
-- /*calculate balance*/
-- UPDATE passengers SET balanace = 'xxx', currently_onboarded = 'false', trip_id = '', from_stop_id = '', onboarded_time = '' where user_id = 'xxx';

