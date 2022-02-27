CREATE TABLE IF NOT EXISTS public.agency
(
    agency_id text,
    agency_name text,
    agency_url text,
    agency_timezone text,
    agency_lang text,
    agency_phone text,
    agency_fare_url text,
    CONSTRAINT agency_key PRIMARY KEY (agency_id)
);

CREATE TABLE IF NOT EXISTS public.routes
(
    route_short_name text,
    route_long_name text,
    route_type integer,
    route_id integer,
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
    zone_id integer,
    CONSTRAINT stops_key PRIMARY KEY (stop_id)
);

CREATE TABLE IF NOT EXISTS public.trips
(
    route_id integer,
    service_id integer,
    trip_id text,
    shape_id text,
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
    CONSTRAINT trips_ref FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
    CONSTRAINT stops_ref FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS public.fare_attributes
(
    fare_id text,
    price float,
    currency_type text,
    payment_method integer,
    transfers integer,
    agency_id text,
    CONSTRAINT fare_attributes_key PRIMARY KEY (fare_id)
);

CREATE TABLE IF NOT EXISTS public.fare_rules
(
    fare_id text,
    route_id integer,
    origin_id integer,
    destination_id integer,
    CONSTRAINT routes_ref_1 FOREIGN KEY (route_id) REFERENCES routes(route_id),
    CONSTRAINT stops_ref_1 FOREIGN KEY (origin_id) REFERENCES stops(stop_id),
    CONSTRAINT stops_ref_2 FOREIGN KEY (destination_id) REFERENCES stops(stop_id)
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

drop table agency cascade;
drop table routes cascade;
drop table stops cascade;
drop table trips cascade;
drop table stop_times cascade;
drop table fare_rules cascade;
drop table fare_attributes cascade;
drop table users cascade;
drop table passengers cascade;
drop table conductors cascade;


\copy agency from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/agency.csv' DELIMITER ',' CSV HEADER;
\copy routes from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/routes.csv' DELIMITER ',' CSV HEADER;
\copy stops from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/stops.csv' DELIMITER ',' CSV HEADER;
\copy trips from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/trips.csv' DELIMITER ',' CSV HEADER;
\copy stop_times from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/stop_times.csv' DELIMITER ',' CSV HEADER;
\copy fare_attributes from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/fare_attributes.csv' DELIMITER ',' CSV HEADER;
\copy fare_rules from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/fare_rules.csv' DELIMITER ',' CSV HEADER;
\copy users from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/users.csv' DELIMITER ',' CSV HEADER;
\copy passengers from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/passengers.csv' DELIMITER ',' CSV HEADER;
\copy conductors from 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/home/conductors.csv' DELIMITER ',' CSV HEADER;

\copy (select fare_rules.fare_id, route_id, origin_id as from_stop_id, destination_id as to_stop_id, price FROM fare_attributes JOIN fare_rules on fare_attributes.fare_id=fare_rules.fare_id) to 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/fares.csv'csv header; 
\copy (select stop_id,stop_code,stop_name,stop_lat,stop_lon from stops) to 'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/stops.csv'csv header;
\copy (select route_id,route_long_name,agency_id from routes) to  'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/routes.csv'csv header;
\copy (select agency_id,agency_name,agency_url,agency_phone from agency) to  'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/agency.csv'csv header;
\copy (select trip_id,route_id from trips) to  'C:/Users/vbikk/Desktop/Study_material/6th semester/COL362(DBMS)/Assignments/dbms-bus-transit-system/database/GTFS_SQL/trips.csv'csv header;















