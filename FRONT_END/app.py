import psycopg2
from flask import Flask, render_template, session, url_for, request, redirect, g 

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
    session['success'] = None
    session['error'] = None
    #TODO: set flash messages here


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/routes')
def searchRoutes():
    return render_template('search/index.html')


#TODO: debug or not?
if __name__ == "__main__":
    app.run(debug=True, port=5039)


# @app.route('/')
# def hello():
#     # conn = get_db_connection()
#     # cur = conn.cursor()

#     # now execute query that you want to execute
#     # cur.execute('SQL query;')
#     # data = cur.fetchall()
#     # for line in data:
#         # print(line)

#     # # TO get column name in table:
#     # cur.execute('SELECT * FROM tablename LIMIT 0;')
#     # colnames = [desc[0] for desc in cur.description]

#     # cur.close()
#     # conn.close()

#     return render_template('index.html', data=data)