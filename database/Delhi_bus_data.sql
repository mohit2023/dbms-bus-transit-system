CREATE TABLE IF NOT EXISTS public.agency
(
    agency_id text,
    agency_name text,
    agency_url text,
    agency_timezone text,
    agency_lang text,
    agency_phone text,
    agency_fare_url text
);
CREATE TABLE IF NOT EXISTS public.calendar
(
    start_date integer,
    end_date integer,
    monday integer,
    tuesday integer,
    wednesday integer,
    thursday integer,
    friday integer,
    saturday integer,
    sunday integer,
    service_id integer
);
CREATE TABLE IF NOT EXISTS public.fare_attributes
(
    fare_id text,
    price float,
    currency_type text,
    payment_method integer,
    transfers integer,
    agency_id text
);
CREATE TABLE IF NOT EXISTS public.fare_rules
(
    fare_id text,
    route_id integer,
    origin_id integer,
    destination_id integer
);
CREATE TABLE IF NOT EXISTS public.routes
(
    route_short_name text,
    route_long_name text,
    route_type integer,
    route_id integer,
    agency_id text
);
CREATE TABLE IF NOT EXISTS public.stop_times
(
    trip_id text,
    arrival_time time,
    departure_time time,
    stop_id integer,
    stop_sequence integer
);
CREATE TABLE IF NOT EXISTS public.stops
(
    stop_id integer,
    stop_code text,
    stop_name text,
    stop_lat float,
    stop_lon float,
    zone_id integer
);
CREATE TABLE IF NOT EXISTS public.trips
(
    route_id integer,
    service_id integer,
    trip_id text,
    shape_id text
);
