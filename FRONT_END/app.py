import psycopg2
from flask import Flask, render_template, session, url_for, request, redirect, g, flash 

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
        data = []
        # TODO: Send a array of tupels containing [stop_id, stop_name, stop_code]
        return render_template('search/index.html', data=data)
    else:
        source = request.form.get('source')
        destination = request.form.get('destination')
        # These are ids of source and destination stops ,find routes
        error = False # check if input is wrong
        if(error):
            flash("Given stops are not present", "error")
            return redirect('/search-routes')
        data = []
        # TODO: send a array of tupels cotaining [[[route_name,from_stop_name,to_stop_name,arrival time at from_stop_id,arrival time at to_stop_id],[same for second bus in this route and so on],...], total_fare]
        return render_template('search/routes.html', data=data, source=source, destination=destination)
        #TODO: source and destination shoudld be as "stop_name-stop_code"


@app.route('/register')
def register_user():
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
