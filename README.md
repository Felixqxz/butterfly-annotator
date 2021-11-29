# Butterfly Annotator
## Welcome!
Welcome to Butterfly Annotator. Below, in this file, you will find instructions to be able to run application on your own machine. If you want more information on how to use the program, open `USE.md` (located at the same level as this file). *This file does not explain how to setup the software for you data either*---if you are looking for that, go to `USE.md` as well.

## Stack
- Python 3 with [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [SQLAlchemy](https://www.sqlalchemy.org/) (running on a local SQLite database);
- [Vue](https://vuejs.org/) with [Bootstrap-Vue](https://bootstrap-vue.org/).

## Running the app
To run the app:
```bash
cd butterfly-annotator
python3.8 -m venv venv
source venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt
flask create_all # Create database and tables inside it, you should see a test.db in current folder
flask populate   # Populate tables with some initial data //haven't been deployed yet
flask run        # Spin the server
```
You can now browse to <http://localhost:8080> and see the app live.
