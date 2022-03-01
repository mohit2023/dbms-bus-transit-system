CREATE TABLE IF NOT EXISTS public.agency
(
    agency_id text,
    agency_name text,
    agency_url text,
    agency_phone text,
    CONSTRAINT agency_key PRIMARY KEY (agency_id)
);

CREATE TABLE IF NOT EXISTS public.routes
(
    route_id integer,
    route_name text,
    agency_id text,
    CONSTRAINT route_key PRIMARY KEY (route_id),
    CONSTRAINT agency_ref FOREIGN KEY (agency_id) REFERENCES agency(agency_id)
);

CREATE TABLE IF NOT EXISTS public.stops
(
    stop_id integer,
    stop_code text,
    stop_name text,
    stop_lat float,
    stop_lon float,
    CONSTRAINT stops_key PRIMARY KEY (stop_id)
);

CREATE TABLE IF NOT EXISTS public.trips
(
    trip_id text,
    route_id integer,
    password text,
    CONSTRAINT trips_key PRIMARY KEY (trip_id),
    CONSTRAINT routes_ref FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

CREATE TABLE IF NOT EXISTS public.stop_times
(
    trip_id text,
    arrival_time time,
    departure_time time,
    stop_id integer,
    stop_sequence integer,
    diff_pick_drop integer,
    CONSTRAINT stop_times_key PRIMARY KEY (trip_id, stop_id, stop_sequence),
    CONSTRAINT trips_ref FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
    CONSTRAINT stops_ref FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS public.fares
(
    fare_id text,
    route_id integer,
    from_stop_id integer,
    to_stop_id integer,
    price float,
    CONSTRAINT fares_key PRIMARY KEY (fare_id),
    CONSTRAINT routes_ref_from_fares FOREIGN KEY (route_id) REFERENCES routes(route_id),
    CONSTRAINT stops_ref_4 FOREIGN KEY (from_stop_id) REFERENCES stops(stop_id),
    CONSTRAINT stops_ref_5 FOREIGN KEY (to_stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS public.passengers
(
    user_id text,
    password text,
    balance integer,
    currently_onboarded text,
    trip_id text,
    from_stop_id integer,
    onboarded_time timestamp,
    CONSTRAINT passengers_key PRIMARY KEY (user_id),
    CONSTRAINT trips_ref_1 FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
    CONSTRAINT stops_ref_3 FOREIGN KEY (from_stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS public.routes_stops
(
    route_id integer,
    stop_id integer,
    stop_sequence integer,
    CONSTRAINT routes_stops_key PRIMARY KEY (route_id, stop_sequence),
    CONSTRAINT routesid_ref FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

-- \copy agency from '/mnt/d/sem6/col362/project/dbms-bus-transit-system/database/GTFS_SQL/agency.csv' DELIMITER ',' CSV HEADER;
-- \copy routes from '/mnt/d/sem6/col362/project/dbms-bus-transit-system/database/GTFS_SQL/routes.csv' DELIMITER ',' CSV HEADER;
-- \copy stops from '/mnt/d/sem6/col362/project/dbms-bus-transit-system/database/GTFS_SQL/stops.csv' DELIMITER ',' CSV HEADER;
-- \copy trips from '/mnt/d/sem6/col362/project/dbms-bus-transit-system/database/GTFS_SQL/trips.csv' DELIMITER ',' CSV HEADER;
-- \copy stop_times from '/mnt/d/sem6/col362/project/dbms-bus-transit-system/database/GTFS_SQL/stop_times.csv' DELIMITER ',' CSV HEADER;
-- \copy fares from '/mnt/d/sem6/col362/project/dbms-bus-transit-system/database/GTFS_SQL/fares.csv' DELIMITER ',' CSV HEADER;
-- \copy passengers from '/mnt/d/sem6/col362/project/dbms-bus-transit-system/database/GTFS_SQL/passengers.csv' DELIMITER ',' CSV HEADER;
-- \copy routes_stops from '/mnt/d/sem6/col362/project/dbms-bus-transit-system/database/GTFS_SQL/routes_stops.csv' DELIMITER ',' CSV HEADER;
