
WITH ft as (
    SELECT trip_id, arrival_time, stop_id, stop_sequence
    FROM stop_times
    WHERE ('12:00:00'<'15:00:00' and arrival_time>'12:00:00' and arrival_time<'15:00:00') or ('12:00:00'>'15:00:00' and (arrival_time>'12:00:00' or arrival_time<'15:00:00'))
), base as (
    SELECT t1.stop_id as source, s1.stop_name as source_stop_name, s1.stop_code as source_stop_code, t2.stop_id as destination, s2.stop_name as destination_stop_name, s2.stop_code as destination_stop_code, routes.route_id, routes.route_name, t1.arrival_time as source_time, t2.arrival_time as destination_time, fares.price as cost
    FROM ft as t1
    JOIN ft as t2 ON t2.trip_id=t1.trip_id AND t2.stop_sequence>t1.stop_sequence
    JOIN stops s1 ON s1.stop_id=t1.stop_id
    JOIN stops s2 ON s2.stop_id=t2.stop_id
    JOIN trips ON trips.trip_id=t1.trip_id
    JOIN routes ON routes.route_id=trips.route_id
    JOIN fares ON fares.route_id=routes.route_id AND fares.from_stop_id=t1.stop_id AND fares.to_stop_id=t2.stop_id
)
SELECT source, source_stop_name, source_stop_code, destination, destination_stop_name, destination_stop_code, ARRAY[route_name] as busnames, ARRAY[route_id]::integer[] as path, 1 as bus, ARRAY[]::text[] as midstopsnames, ARRAY[]::text[] as midstopscodes, ARRAY[]::integer[] as midstops, source_time, destination_time, ARRAY[]::time[] as mid_stop_reach_time, ARRAY[]::time[] as mid_stop_start_time, cost
FROM base
WHERE source='4258' AND destination='2026'

UNION

SELECT b1.source, b1.source_stop_name, b1.source_stop_code, b2.destination, b2.destination_stop_name, b2.destination_stop_code, ARRAY[b1.route_name, b2.route_name] as busnames, ARRAY[b1.route_id, b2.route_id]::integer[] as path, 2 as bus, ARRAY[b1.destination_stop_name] as midstopsnames,  ARRAY[b1.destination_stop_code] as midstopscodes, ARRAY[b1.destination]::integer[] as midstops, b1.source_time, b2.destination_time, ARRAY[b1.destination_time]::time[] as mid_stop_reach_time, ARRAY[b2.source_time]::time[] as mid_stop_start_time, b1.cost+b2.cost as cost
FROM base as b1
JOIN base as b2 ON b1.destination=b2.source AND b1.route_id!=b2.route_id
WHERE b1.source='4258' AND b2.destination='2026' and b1.destination_time<b2.source_time

UNION

SELECT b1.source, b1.source_stop_name, b1.source_stop_code, b2.destination, b2.destination_stop_name, b2.destination_stop_code, ARRAY[b1.route_name, b3.route_name, b2.route_name] as busnames, ARRAY[b1.route_id, b3.route_id, b2.route_id]::integer[] as path, 3 as bus, ARRAY[b1.destination_stop_name, b3.destination_stop_name] as midstopsnames,  ARRAY[b1.destination_stop_code, b3.destination_stop_code] as midstopscodes, ARRAY[b1.destination, b3.destination]::integer[] as midstops, b1.source_time, b2.destination_time, ARRAY[b1.destination_time, b3.destination_time]::time[] as mid_stop_reach_time, ARRAY[b3.source_time, b2.source_time]::time[] as mid_stop_start_time, b1.cost+b2.cost+b3.cost as cost
FROM base as b1
JOIN base as b2 ON b1.route_id!=b2.route_id
JOIN base as b3 ON b1.route_id!=b3.route_id AND b1.destination=b3.source AND b2.source=b3.destination
WHERE b1.source='4258' AND b2.destination='2026' and b1.destination_time<b3.source_time and b3.destination_time<b2.source_time

ORDER BY bus, cost
limit 5;