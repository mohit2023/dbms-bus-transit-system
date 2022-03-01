import psycopg2
from flask import Flask, render_template, session, url_for, request, redirect, g, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "thisshouldbesecret"

def get_db_connection():
    conn = psycopg2.connect(
        host = "localhost",
        #TODO: ip address of postgres server or not? instead of localhost,(what about port?)
        database = "group_39",
        user = "postgres",
        #TODO: check what read only user means
        password = "pass",
    )
    return conn

@app.errorhandler(404)
def error_404(error):
    return render_template('error.html')

@app.errorhandler(500)
def error_500(error):
    return render_template('error.html')

@app.before_request
def before_request():
    if(not request.path in ['/login','/register']):
        session['returnTo'] = request.url
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search-routes', methods = ['POST', 'GET'])
def searchInput():
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
        print(s)
        d = destination.split('-')[-1:][0]
        print(d)
        error = False # check if input is wrong
        if(s!="" and d!="" and s!=d):
            print("in")
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
                # TODO: send a array of tupels cotaining [[[route_name,from_stop_name,to_stop_name,arrival time at from_stop_id,arrival time at to_stop_id],[same for second bus in this route and so on],...], total_fare]
                # return render_template('search/routes.html', data=data, size=size, source=source, destination=destination)
                #TODO: source and destination shoudld be as "stop_name-stop_code"
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
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT stop_sequence, stops.stop_id, stop_name, stop_code, arrival_time, departure_time, stop_lat, stop_lon
        FROM stop_times
        JOIN stops ON stops.stop_id=stop_times.stop_id
        WHERE trip_id=%s
        ORDER BY stop_sequence;
    """
    try:
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
    if(request.method == 'GET'):
        return render_template('auth/login.html')
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        usertype = request.form.get('usertype')
        if(userid and password and usertype):
            conn = get_db_connection()
            cur = conn.cursor()
            query = 'select * from users where user_id=%s and user_type=%s'
            cur.execute(query, (userid, usertype))
            data = cur.fetchall()
            if(data):
                if(check_password_hash(data[1], password)):
                    session['currentUser'] = {
                        'userid' : userid,
                        'usertype' : usertype
                    }
                    flash("Welcome, "+userid+". Your are successfully logged in!", "success")
                    returnTo = session['returnTo'] or '/'
                    session['returnTo']=None
                    curr.close()
                    conn.close()
                    return redirect(returnTo)
            curr.close()
            conn.close()
        flash("Invalid Data! Try Again!", "error")    
        return redirect('/login')

@app.route('/logout')
def logout():
    if(not session.currentUser):
        flash("Error: You were not logged in", "error")
        return redirect('/')
    session['currentUser'] = None
    flash("Bye!! Have a nice day!", "success")
    return redirect('/')
        

@app.route('/register', methods = ['POST', 'GET'])
def register():
    # if(request.method == 'GET'):
    #     return render_template('auth/register.html')
    # else:
    # userid = request.form.get('userid')
    # password = request.form.get('password')
    # if(userid and password):
    #     hashedpass = generate_password_hash(passowrd, "sha256")
    #     conn = get_db_connection()
    #     cur = conn.cursor()
    #     query = "Insert into users (userid, password, usertype) values (%s, %s, 'passenger');"
    #     cur.execute(query, (userid, hashedpass))
    #     cur.close()
    #     conn.close()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select user_id from users;')
    all_ids = cur.fetchall()
    #print('user_id: ')
    user_id = input()
    if ((user_id) in all_ids):
        #print('user_id already exist.')
        cur.close()
        conn.close()
        return render_template('home.html')
    #print('password: ')
    password = input()
    #print('user_tyoe: ')
    user_type = input()
    if (user_type not in ['admin','conductor','passenger']):
        #print('user_type not exist.')
        cur.close()
        conn.close()
        return render_template('home.html')
    #print('trying to insert')
    #cur.close()
    #cur = conn.cursor()
    #cur.execute('INSERT INTO users (user_id, password, user_type) VALUES ('+user_id+','+password+','+user_type+');')
    #print('inserted')
    cur.close()
    conn.close()

    return render_template('home.html')

#TODO: debug or not?
if __name__ == "__main__":
    app.run(debug=True, port=5039)
