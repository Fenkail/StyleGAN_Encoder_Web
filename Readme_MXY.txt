use the local 224*224 images as a database, and only can use size 224*224
so need to use "python -m http.server 20202" under the root direction of images to start a local network, here 20202 is port and it can be changed
just need to change the config_retrieval in config.py, and mostly just need to modify the "images_root_dir" and "server"

start the http.server 
use "cd" into the images root direction
then use "python -m http.server 20202", here 20202 is port and it can be changed
and there will return a msg like "Serving HTTP on 0.0.0.0 port 20202 (http://0.0.0.0:20202/) ..."
in Linux, just copy "http://0.0.0.0:20202/" to the "server" in config_retrieval from config.py
in Windows, need to copy the IP to replace the "0.0.0.0", like "http://192.168.253.1:20202/"

then use the cmd to start the flask
in Linux:
if need venv, use follows in the project direction
	$ virtualenv venv
for python3, use
        $ virtualenv -p /usr/bin/python3.6 venv
	$ . venv/bin/activate
	$ pip install -r requirements.txt
later, just need follows to start the venv
	$ . venv/bin/activate
no need venv, just use follows
	$ export FLASK_APP=sotu.py
	$ export FLASK_ENV=development
to extract features, use following cmd, and must remember the Database is local, so it use the absolute path
	$ flask extract
then run flask
	$ flask run -h localhost -p 8080

in windows cmd:
create venv
	> virtualenv venv 
start venv
	> venv\Scripts\activate
	> set FLASK_APP=sotu.py
	> flask extract
	> flask run -h localhost -p 8080

no evaluation

