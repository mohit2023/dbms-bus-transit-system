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
    CONSTRAINT stop_times_key PRIMARY KEY (trip_id),
    CONSTRAINT trips_ref FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
    CONSTRAINT stops_ref FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS public.fares
(
    fare_id text,
    route_id text,
    from_stop_id text,
    to_stop_id text,
    price float,
    CONSTRAINT fares_key PRIMARY KEY (fare_id),
    CONSTRAINT trips_ref FOREIGN KEY (route_id) REFERENCES trips(trip_id),
    CONSTRAINT stops_ref_4 FOREIGN KEY (from_stop_id) REFERENCES stops(stop_id),
    CONSTRAINT stops_ref_5 FOREIGN KEY (to_stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS public.users
(
    user_id text,
    password text,
    user_type text,
    CONSTRAINT user_key PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS public.passengers
(
    user_id text,
    balance integer,
    currently_onboarded text,
    trip_id text,
    from_stop_id integer,
    onboarded_time time,
    CONSTRAINT passengers_key PRIMARY KEY (user_id),
    CONSTRAINT trips_ref_1 FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
    CONSTRAINT stops_ref_3 FOREIGN KEY (from_stop_id) REFERENCES stops(stop_id)
);


CREATE TABLE IF NOT EXISTS public.conductors
(
    user_id text,
    trip_id text,
    CONSTRAINT constructors_key PRIMARY KEY (user_id),
    CONSTRAINT trips_ref_2 FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
);



\copy agency from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/agency.csv' DELIMITER ',' CSV HEADER;
\copy routes from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/routes.csv' DELIMITER ',' CSV HEADER;
\copy stops from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/stops.csv' DELIMITER ',' CSV HEADER;
\copy trips from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/trips.csv' DELIMITER ',' CSV HEADER;
\copy stop_times from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/stop_times.csv' DELIMITER ',' CSV HEADER;
\copy fares from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/fares.csv' DELIMITER ',' CSV HEADER;
\copy users from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/users.csv' DELIMITER ',' CSV HEADER;
\copy passengers from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/passengers.csv' DELIMITER ',' CSV HEADER;
\copy conductors from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/conductors.csv' DELIMITER ',' CSV HEADER;
