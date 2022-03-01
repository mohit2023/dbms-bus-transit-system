--routes--
/*NO RECURSION ONLY ROUTES OVER SAME TRIP*/

-- WITH RECURSIVE Reaches_two_hops(source_station_name,destination_station_name, day_of_arrival, day_of_departure, total_distance, hop, path) AS
--         (SELECT source_station_name, destination_station_name, day_of_arrival, day_of_departure, distance, 0, array[source_station_name, destination_station_name] as path 
--         FROM train_info
--         WHERE source_station_name = 'DADAR' AND day_of_arrival = day_of_departure
--     UNION ALL
--         SELECT R1.source_station_name, R2.destination_station_name, R1.day_of_arrival, R2.day_of_departure, R1.total_distance+R2.distance, R1.hop+1,  array_append(path, R2.destination_station_name)
--         FROM Reaches_two_hops AS R1, train_info AS R2
--         WHERE R1.destination_station_name = R2.source_station_name AND R2.day_of_arrival = R2.day_of_departure AND R2.day_of_departure = R1.day_of_arrival AND R1.hop <= 1 AND NOT R2.destination_station_name = any(path)
--         )

-- SELECT DISTINCT destination_station_name, total_distance as distance, day_of_arrival as day
-- FROM Reaches_two_hops
-- WHERE NOT destination_station_name = 'DADAR'
-- ORDER BY destination_station_name asc, distance asc, day asc;





WITH RECURSIVE reachable_station(trip_id, stop_id, hop, reached_stops, travelled_trip) AS
        (SELECT trip_id, stop_id, 0, array[stop_id] as reached_stops, array[trip_id] as travelled_trip
        FROM stop_times
        WHERE stop_times.trip_id = any(SELECT trip_id from stop_times where stop_id = 23)
    UNION ALL
        SELECT R2.trip_id, R2.stop_id, R1.hop+1, array_append(R1.reached_stops,R2.stop_id), array_append(R1.travelled_trip,R2.trip_id)
        FROM reachable_station AS R1, stop_times AS R2
        WHERE R2.trip_id <> any(travelled_trip) AND R2.stop_id <> any(reached_stops) AND R1.hop<1
        )
SELECT DISTINCT trip_id,stop_id,hop
FROM reachable_station
ORDER BY trip_id
LIMIT 10;


-- WITH RECURSIVE inter_trip(trip_id,stop_id,hop) AS
--         (SELECT from_trip_ids.trip_id,stop_id,0
--         FROM from_trip_ids, stop_times
--         WHERE from_trip_ids.trip_id = stop_times.trip_id
--     UNION
--         SELECT R2.trip_id,R2.stop_id,R1.hop+1
--         FROM inter_trip AS R1, stop_times AS R2, to_trip_ids AS R3
--         WHERE R1.stop_id = any() AND R2.trip_id = R3.trip_id AND hop<0
--         ),

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

-- SELECT inter_trip.trip_id
-- FROM inter_trip, to_trip_ids
-- WHERE inter_trip.trip_id = to_trip_ids.trip_id
-- ORDER BY trip_id
-- LIMIT 10;


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

