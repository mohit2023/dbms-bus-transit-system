import psycopg2
import datetime
import time
from flask import Flask, render_template, session, url_for, request, redirect, g, flash, abort
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "thisshouldbesecret"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=300)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host = "localhost",
            #TODO: ip address of postgres server or not? instead of localhost,(what about port?)
            database = "group_39",
            user = "postgres",
            #TODO: check what read only user means
            password = "pass",
        )
    except psycopg2.Error as e:
        abort(500)
    return conn

@app.errorhandler(404)
def error_404(error):
    return render_template('error.html')

@app.errorhandler(500)
def error_500(error):
    return render_template('error.html')

@app.before_request
def before_request():
    if(not request.path in ['/login','/register'] and 'static' not in request.path):
        session['returnTo'] = request.path
        print(request.path)
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search-routes', methods = ['POST', 'GET'])
def searchRoutes():
    if(request.method == 'GET'):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = """
                SELECT stop_id,stop_name,stop_code
                FROM stops
                ORDER BY stop_name ASC;
            """
            cur.execute(query)
        except psycopg2.Error as e:
            cur.close()
            conn.close()
            abort(500)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('search/index.html', data=data)
    else:
        source = request.form.get('source')
        destination = request.form.get('destination')
        s = source.split('-')[-1:][0]
        d = destination.split('-')[-1:][0]
        if(s!="" and d!="" and s!=d):
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                query = """
                    SELECT stop_id 
                    FROM stops 
                    WHERE stop_id=%s OR stop_id=%s;
                """
                cur.execute(query, (s, d))
            except psycopg2.Error as e:
                cur.close()
                conn.close()
                abort(500)
            if(cur.rowcount==2):
                query = """
                    WITh base as (
                        SELECT t1.stop_id as source, s1.stop_name as source_stop_name, s1.stop_code as source_stop_code, t2.stop_id as destination, s2.stop_name as destination_stop_name, s2.stop_code as destination_stop_code, t1.route_id, routes.route_name
                        FROM routes_stops as t1
                        JOIN routes_stops as t2 ON t2.route_id=t1.route_id AND t2.stop_sequence>t1.stop_sequence
                        JOIN stops s1 ON s1.stop_id=t1.stop_id
                        JOIN stops s2 ON s2.stop_id=t2.stop_id
                        JOIN routes ON routes.route_id=t1.route_id
                    )
                    SELECT source, source_stop_name, source_stop_code, destination, destination_stop_name, destination_stop_code, busnames, bus, midstopsnames, midstopscodes, midstops 
                    FROM (
                    SELECT source, source_stop_name, source_stop_code, destination, destination_stop_name, destination_stop_code, ARRAY[route_name] as busnames, ARRAY[route_id]::integer[] as path, 1 as bus, ARRAY[]::text[] as midstopsnames, ARRAY[]::text[] as midstopscodes, ARRAY[]::integer[] as midstops
                    FROM base
                    WHERE source=%s AND destination=%s

                    UNION

                    SELECT b1.source, b1.source_stop_name, b1.source_stop_code, b2.destination, b2.destination_stop_name, b2.destination_stop_code, ARRAY[b1.route_name, b2.route_name] as busnames, ARRAY[b1.route_id, b2.route_id]::integer[] as path, 2 as bus, ARRAY[b1.destination_stop_name] as midstopsnames,  ARRAY[b1.destination_stop_code] as midstopscodes, ARRAY[b1.destination]::integer[] as midstops
                    FROM base as b1
                    JOIN base as b2 ON b1.destination=b2.source AND b1.route_id!=b2.route_id
                    WHERE b1.source=%s AND b2.destination=%s

                    UNION

                    SELECT b1.source, b1.source_stop_name, b1.source_stop_code, b2.destination, b2.destination_stop_name, b2.destination_stop_code, ARRAY[b1.route_name, b3.route_name, b2.route_name] as busnames, ARRAY[b1.route_id, b3.route_id, b2.route_id]::integer[] as path, 3 as bus, ARRAY[b1.destination_stop_name, b3.destination_stop_name] as midstopsnames,  ARRAY[b1.destination_stop_code, b3.destination_stop_code] as midstopscodes, ARRAY[b1.destination, b3.destination]::integer[] as midstops
                    FROM base as b1
                    JOIN base as b2 ON b1.route_id!=b2.route_id
                    JOIN base as b3 ON b1.route_id!=b3.route_id AND b1.destination=b3.source AND b2.source=b3.destination
                    WHERE b1.source=%s AND b2.destination=%s
                    ) as data
                    ORDER BY bus
                    limit 10;
                """
                try:
                    cur.execute(query, (s,d,s,d,s,d))
                except psycopg2.Error as e:
                    cur.close()
                    conn.close()
                    abort(500)
                size = cur.rowcount
                data = cur.fetchall()
                cur.close()
                conn.close()
                return render_template('search/routes.html', data=data, size=size, source=source, destination=destination)
        flash("Given stops are not present", "error")
        return redirect('/search-routes')

@app.route('/buses')
def getbuses():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT route_id, route_name, agency_name
            FROM routes
            JOIN agency ON agency.agency_id=routes.agency_id
            ORDER BY route_name;
        """
        cur.execute(query)
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        abort(500)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('search/buses.html', data=data)

@app.route('/buses/<int:id>')
def getTrips(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query1 = """
            SELECT route_name, trip_id 
            FROM routes
            JOIN trips ON routes.route_id=trips.route_id
            WHERE routes.route_id=%s
            ORDER BY trip_id;
        """
        cur.execute(query1, (id,))
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        abort(500)
    if(cur.rowcount>0):
        data = cur.fetchall()
        query2 = """
            SELECT stops.stop_id, stop_name, stop_code, stop_sequence
            FROM routes_stops
            JOIN stops ON stops.stop_id=routes_stops.stop_id
            WHERE route_id=%s AND (stop_sequence = (
                SELECT MAX(stop_sequence) 
                FROM routes_stops
                WHERE route_id=%s
                GROUP BY route_id
                ) OR stop_sequence = (
                    SELECT MIN(stop_sequence) 
                    FROM routes_stops
                    WHERE route_id=%s
                    GROUP BY route_id
                ) 
            )
            ORDER BY stop_sequence;
        """
        try:
            cur.execute(query2, (id, id, id))
        except psycopg2.Error as e:
            cur.close()
            conn.close()
            abort(500)
        busdetails= cur.fetchall()
        cur.close()
        conn.close()
        return render_template('search/trip-list.html', data=data, busdetails=busdetails)
    flash("Bus not found", "error")
    cur.close()
    conn.close()
    abort(404)

@app.route('/trip/<id>')
def getPaths(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT stop_sequence, stops.stop_id, stop_name, stop_code, arrival_time, departure_time, stop_lat, stop_lon
            FROM stop_times
            JOIN stops ON stops.stop_id=stop_times.stop_id
            WHERE trip_id=%s
            ORDER BY stop_sequence;
        """
        cur.execute(query, (id, ))
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        abort(500)
    if(cur.rowcount>0):
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('search/trip.html', data=data, trip_id=id)
    cur.close()
    conn.close()
    abort(404)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(session.get('currentUser')):
        flash("Already logged In! Logout If you want to switch account", "error")
        return redirect('/')
    if(request.method == 'GET'):
        return render_template('auth/login.html')
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        usertype = request.form.get('usertype')
        if(userid and password and (usertype=='passenger' or usertype=='conductor')):
            conn = get_db_connection()
            cur = conn.cursor()
            if(usertype=='passenger'):
                print("pass\n")
                query = """
                    SELECT password
                    FROM passengers
                    WHERE user_id=%s;
                """
                try:
                    cur.execute(query, (userid,))
                except psycopg2.Error as e:
                    cur.close()
                    conn.close()
                    abort(500)
                if(cur.rowcount>0):
                    data = cur.fetchall()
                    if(check_password_hash(data[0][0], password)):
                        session.permanent = True
                        session['currentUser'] = {
                            'userid' : userid,
                            'usertype' : usertype
                        }
                        flash("Welcome Passenger, "+userid+". Your are successfully logged in!", "success")
                        returnTo = session.get('returnTo') or '/passenger'
                        session.pop('returnTo', None)
                        cur.close()
                        conn.close()
                        return redirect(returnTo)
            else:
                query = """
                    SELECT password
                    FROM trips
                    WHERE trip_id=%s;
                """
                try:
                    cur.execute(query, (userid,))
                except psycopg2.Error as e:
                    cur.close()
                    conn.close()
                    abort(500)
                if(cur.rowcount>0):
                    data = cur.fetchall()
                    if(check_password_hash(data[0], password)):
                        session.permanent = True
                        session['currentUser'] = {
                            'userid' : userid,
                            'usertype' : usertype
                        }
                        flash("Welcome Conductor, "+userid+". Your are successfully logged in!", "success")
                        returnTo = session.get('returnTo') or '/conductor'
                        session.pop('returnTo', None)
                        curr.close()
                        conn.close()
                        return redirect(returnTo)
            cur.close()
            conn.close()
        flash("Invalid Data! Try Again!", "error")    
        return redirect('/login')

@app.route('/logout')
def logout():
    if(not session.get('currentUser')):
        flash("Error: You were not logged in", "error")
        return redirect('/')
    session.pop('currentUser', None)
    flash("Bye!! Have a nice day!", "success")
    return redirect('/')

@app.route('/passenger')
def passenger_profile():
    if(not session.get('currentUser')):
        return redirect('/login')
    if(session.get('currentUser').get('usertype')!='passenger'):
        flash("You need to login as passenger", "error")
        return redirect(session.get('returnTo'))
    conn=get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT user_id, balance, currently_onboarded, trip_id, from_stop_id, onboarded_time
        FROM passengers
        WHERE user_id=%s;
    """
    try:
        cur.execute(query, (session.get('currentUser').get('userid'), ))
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        abort(500)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('passenger/passenger.html', data=data[0])

@app.route('/live-search', methods = ['POST', 'GET'])
def live_search():
    if(not session.get('currentUser')):
        return redirect('/login')
    if(session.get('currentUser').get('usertype')!='passenger'):
        flash("You need to login as passenger", "error")
        return redirect(session.get('returnTo'))
    if(request.method == 'GET'):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = """
                SELECT stop_id,stop_name,stop_code
                FROM stops
                ORDER BY stop_name ASC;
            """
            cur.execute(query)
        except psycopg2.Error as e:
            cur.close()
            conn.close()
            abort(500)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('passenger/search.html', data=data)
    else:
        source = request.form.get('source')
        destination = request.form.get('destination')
        time = request.form.get('user-time')
        s = source.split('-')[-1:][0]
        d = destination.split('-')[-1:][0]
        print(time)
        if(s!="" and d!="" and s!=d and len(time)==5 and time[2]==':' and time>'00:00' and time<'23:59' and time[0].isdigit() and time[1].isdigit() and time[3].isdigit() and time[4].isdigit()):
            time = time+':00'
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                query = """
                    SELECT stop_id 
                    FROM stops 
                    WHERE stop_id=%s OR stop_id=%s;
                """
                cur.execute(query, (s, d))
            except psycopg2.Error as e:
                cur.close()
                conn.close()
                abort(500)
            if(cur.rowcount==2):
                st = time
                hour = (int(time[:2])+2)%24
                str_hour = str(hour)
                if (hour<10):
                    str_hour = '0'+str(hour)
                et = str_hour+time[2:]
                query = """
                    WITH ft as (
                        SELECT trip_id, arrival_time, stop_id, stop_sequence
                        FROM stop_times
                        WHERE (%s<%s and arrival_time>%s and arrival_time<%s) or (%s>%s and (arrival_time>%s or arrival_time<%s))
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
                    WHERE source=%s AND destination=%s

                    UNION

                    SELECT b1.source, b1.source_stop_name, b1.source_stop_code, b2.destination, b2.destination_stop_name, b2.destination_stop_code, ARRAY[b1.route_name, b2.route_name] as busnames, ARRAY[b1.route_id, b2.route_id]::integer[] as path, 2 as bus, ARRAY[b1.destination_stop_name] as midstopsnames,  ARRAY[b1.destination_stop_code] as midstopscodes, ARRAY[b1.destination]::integer[] as midstops, b1.source_time, b2.destination_time, ARRAY[b1.destination_time]::time[] as mid_stop_reach_time, ARRAY[b2.source_time]::time[] as mid_stop_start_time, b1.cost+b2.cost as cost
                    FROM base as b1
                    JOIN base as b2 ON b1.destination=b2.source AND b1.route_id!=b2.route_id
                    WHERE b1.source=%s AND b2.destination=%s and b1.destination_time<b2.source_time

                    UNION

                    SELECT b1.source, b1.source_stop_name, b1.source_stop_code, b2.destination, b2.destination_stop_name, b2.destination_stop_code, ARRAY[b1.route_name, b3.route_name, b2.route_name] as busnames, ARRAY[b1.route_id, b3.route_id, b2.route_id]::integer[] as path, 3 as bus, ARRAY[b1.destination_stop_name, b3.destination_stop_name] as midstopsnames,  ARRAY[b1.destination_stop_code, b3.destination_stop_code] as midstopscodes, ARRAY[b1.destination, b3.destination]::integer[] as midstops, b1.source_time, b2.destination_time, ARRAY[b1.destination_time, b3.destination_time]::time[] as mid_stop_reach_time, ARRAY[b3.source_time, b2.source_time]::time[] as mid_stop_start_time, b1.cost+b2.cost+b3.cost as cost
                    FROM base as b1
                    JOIN base as b2 ON b1.route_id!=b2.route_id
                    JOIN base as b3 ON b1.route_id!=b3.route_id AND b1.destination=b3.source AND b2.source=b3.destination
                    WHERE b1.source=%s AND b2.destination=%s and b1.destination_time<b3.source_time and b3.destination_time<b2.source_time

                    ORDER BY bus, cost
                    limit 5;
                """
                try:
                    cur.execute(query, (st,et,st,et,st,et,st,et,s,d,s,d,s,d))
                except psycopg2.Error as e:
                    cur.close()
                    conn.close()
                    abort(500)
                size = cur.rowcount
                data = cur.fetchall()
                cur.close()
                conn.close()
                return render_template('passenger/live-routes.html', data=data, size=size, source=source, destination=destination)
                # TODO: send a array of tupels cotaining [[[route_name,from_stop_name,to_stop_name,arrival time at from_stop_id,arrival time at to_stop_id],[same for second bus in this route and so on],...], total_fare]
                # return render_template('search/routes.html', data=data, size=size, source=source, destination=destination)
                #TODO: source and destination shoudld be as "stop_name-stop_code"
        flash("Given stops are not present or Invalid Time", "error")
        return redirect('/live-search')


@app.route('/passenger/buy-ticket')
def showStopsToBuyTicket():
    if(not session.get('currentUser')):
        return redirect('/login')
    if(session.get('currentUser').get('usertype')!='passenger'):
        flash("You need to login as passenger", "error")
        return redirect(session.get('returnTo'))
    conn=get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT stop_id, stop_name, stop_code
        FROM stops
        ORDER BY stop_name;
    """
    try:
        cur.execute(query)
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        abort(500)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('passenger/selectstop.html', data=data)

@app.route('/passenger/buy-ticket/<int:stopid>')
def showTripsToBuyTicket(stopid):
    if(not session.get('currentUser')):
        return redirect('/login')
    if(session.get('currentUser').get('usertype')!='passenger'):
        flash("You need to login as passenger", "error")
        return redirect(session.get('returnTo'))
    conn=get_db_connection()
    cur = conn.cursor()
    st = datetime.datetime.now().strftime("%H:%M:%S")
    sec = int(st[:2])*3600+int(st[3:5])*60+int(st[6:])
    sec = sec + 300
    sec=sec%(24*60*60)
    et = time.strftime('%H:%M:%S', time.gmtime(sec))
    st='07:30:20'
    et='07:35:20' # TODO: remove
    query = """
        SELECT trips.trip_id, route_name, stop_id, departure_time
        FROM stop_times
        JOIN trips ON trips.trip_id=stop_times.trip_id
        JOIN routes ON routes.route_id=trips.route_id
        WHERE stop_id=%s AND ((%s<%s AND arrival_time BETWEEN %s AND %s) OR (%s>%s AND (arrival_time>%s OR arrival_time<%s) ))
        ORDER BY route_name;
    """
    try:
        cur.execute(query,(stopid, st,et,st,et,st,et,st,et))
    except psycopg2.Error as e:
        print(e)
        cur.close()
        conn.close()
        abort(500)
    if(cur.rowcount>0):
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('passenger/selecttrip.html', data=data)
    cur.close()
    conn.close()
    flash("Buses not found for given stop", "error")
    return redirect('/passenger/buy-ticket')

@app.route('/passenger/buy-ticket/<int:stopid>/<tripid>', methods = ['POST', 'GET'])
def buyTicket(stopid, tripid):
    if(not session.get('currentUser')):
        return redirect('/login')
    if(session.get('currentUser').get('usertype')!='passenger'):
        flash("You need to login as passenger", "error")
        return redirect(session.get('returnTo'))
    
    if(method=='GET'):
        conn=get_db_connection()
        cur = conn.cursor()
        st = datetime.datetime.now().strftime("%H:%M:%S")
        sec = int(st[:2])*3600+int(st[3:5])*60+int(st[6:])
        sec = sec + 300
        sec=sec%(24*60*60)
        et = time.strftime('%H:%M:%S', time.gmtime(sec))
        st='07:30:20'
        et='07:35:20' # TODO : remove
        query = """
            SELECT trips.trip_id, route_name, stops.stop_id, stop_name, stop_code, departure_time 
            FROM stop_times
            JOIN trips ON trips.trip_id=stop_times.trip_id
            JOIN routes ON routes.route_id=trips.route_id
            JOIN stops ON stops.stop_id=stop_times.stop_id
            WHERE stop_times.trip_id=%s AND stops.stop_id=%s AND ((%s<%s AND arrival_time BETWEEN %s AND %s) OR (%s>%s AND (arrival_time>%s OR arrival_time<%s) ))
            ORDER BY stop_sequence;
        """
        try:
            cur.execute(query,(tripid, stopid, st,et,st,et,st,et,st,et))
        except psycopg2.Error as e:
            print(e)
            cur.close()
            conn.close()
            abort(500)
        if(cur.rowcount>0):
            data = cur.fetchone()
            cur.close()
            conn.close()
            return render_template('passenger/buyticket.html', data=data)
        cur.close()
        conn.close()
        flash("Buses not found for given stop and trip", "error")
        return redirect('/passenger/buy-ticket/'+str(stopid))
    else:
        conn=get_db_connection()
        cur = conn.cursor()
        st = datetime.datetime.now().strftime("%H:%M:%S")
        sec = int(st[:2])*3600+int(st[3:5])*60+int(st[6:])
        sec = sec + 300
        sec=sec%(24*60*60)
        et = time.strftime('%H:%M:%S', time.gmtime(sec))
        st='07:30:20'
        et='07:35:20' # TODO : remove
        # TODO: check again if this bus is actually running right now
        # TODO: check if user already onboarded
        # TODO: minimum balance check
        timestamp=datetime.datetime.now()
        query = """
            UPDATE passengers
            SET currently_onboarded='true', trip_id=%s, from_stop_id=%s,onboarded_time=%s, balance = balance - (
                SELECT cost
                FROM fares
                WHERE fares.from_stop_id=%s AND fares.route_id=(
                    SELECT routes.route_id
                    FROM trips
                    WHERE trips.trip_id=%s
                ) AND fares.to_stop_id = (
                    SELECT stop_id
                    FROM stop_times
                    WHERE trip_id=%s AND stop_sequence = (
                        SELECT MAX(stop_sequence)
                        FROM stop_times
                        WHERE trip_id=%s
                    )
                )
            )
            WHERE user_id=%s;
        """
        # TODO: update stop_times bus onboarded counts(diff_pick_drop)
        try:
            cur.execute(query,(tripid, stopid, timestamp, stopid, tripid, tripid, tripid))
        except psycopg2.Error as e:
            print(e)
            cur.close()
            conn.close()
            abort(500)
        if(cur.rowcount>0):
            data = cur.fetchone()
            cur.close()
            conn.close()
            flash("Ticket Bought! Any Extra Charges Deducted will returned when you deboard!", "success")
            return redirect('/passenger')
        cur.close()
        conn.close()
        flash("Internal Error Occurred! Sry", "error")
        return redirect('/passenger')
    

@app.route('/conductor')
def conductor_profile():
    if(not session.get('currentUser')):
        return redirect('/login')
    if(session.get('currentUser').get('usertype')!='conductor'):
        flash("You need to login as conductor", "error")
        return redirect(session.get('returnTo'))
    conn=get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT trips.trip_id, route_id, arrival_time, departure_time, stops.stop_id, stop_sequence, diff_pick_drop, stop_name, stop_code
        FROM trips
        JOIN stop_times ON trips.trip_id=stop_times.trip_id
        JOIN stops ON stops.stop_id=stop_times.stop_id
        WHERE trip_id=%s;
    """
    try:
        cur.execute(query, (session.get('currentUser').get('userid'), ))
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        abort(500)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('conductor/conductor.html', data=data[0])

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if(request.method == 'GET'):
        return render_template('auth/register.html')
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        if(userid and password):
            hashedpass = generate_password_hash(password, "sha256")
            conn = get_db_connection()
            cur = conn.cursor()
            query = """
                INSERT into passengers (userid, password, balance, currently_onboard) values (%s, %s, 1000, 'false');
            """
            cur.execute(query, (userid, hashedpass))
            if(cur.rowcount>0):
                flash("Successfully registred! Try Login", "success")
                cur.close()
                conn.close()
                return redirect('/login')
            cur.close()
            conn.close()
        flash("Invalid data! Maybe User Name already Registered", "error")
        return redirect('/register')


#TODO: debug or not?
if __name__ == "__main__":
    app.run(debug=True, port=5039)
