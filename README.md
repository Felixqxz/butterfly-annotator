## Butterfly annotator

#### Quick Start

Firstly, make sure you created a virtual environment and installed all required dependences

```bash
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, you need to setup client by executing in the root path

```bash
cd templates
npm run local
```

Finally you can run server by executing in the root path

```bash
flask create_all # Create database and tables inside it, you should see a test.db in current folder
flask run        # Spin the server
```

By default, a web page will be served at http://127.0.0.1:5000/.

After first creating *test.db* file, you can run server by executing `flask run`

#### Dependences

You can install all required dependences by `requirements.txt`

#### Server

You can run the server by the following commands:

```bash
flask create_all # Create database and tables inside it, you should see a test.db in current folder
flask run        # Spin the server
flask drop_all	 # Delete database and tables inside it, you should see the test.db removed in current folder
```

#### Client

Client is automatically setted up by executing

```bash
npm run local
```

#### Environment Parameters

By default, both client and server will be configured based on `.flaskenv` file in the root path.

You can change to a production environment by deleting `FLASK_ENV = development` in the file.

```
# /.flaskenv
FLASK_APP = website/app.py
FLASK_ENV = development
```

