# dbms-bus-transit-system

SERVER DETAILS:
group members are: Mohit Sharma, Vivek Choudhary

Uername: group_39
Password: zOVDpJD8Mck9g

Portal's URL: http://10.17.50.36:5000/
(will only work when connected to IIT Delhi's network)

Use the aforementioned credentials to connect to this DB:

Host: 10.17.50.36
Port: 5432
Database Name: group_39


Setup:
1) Local python env
Imp commands when using conda:
conda create -n dbms python=3.8
conda activate dbms
conda deactivate dbms
conda install -n dbms packagename

To install flask:
pip install flask
Check by:
python -c "import flask; print(flask.__version__)"

Flask Usage:
export FLASK_APP=app
export FLASK_ENV=development
flask run  
( http://127.0.0.1:5000/ )
(by default at port 5000 or use below command to specify port)
flask run -p 5039
( http://127.0.0.1:5039/ )

Install psycopg2:
pip install psycopg2-binary