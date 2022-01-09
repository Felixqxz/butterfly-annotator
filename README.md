# Butterfly annotator

## Welcome!
Welcome to Butterfly Annotator. Below, in this file, you will find instructions to be able to run application on your own machine. If you want more information on how to use the program, open USE.md (located at the same level as this file). This file does not explain how to setup the software for you data either---if you are looking for that, go to USE.md as well.

## Running the program

Independent of your OS, make sure you have both NodeJS and Python3 installed. 

On Linux: create a virtual environment and install all required Python dependencies:
```bash
python3.8 -m venv venv
source venv/bin/activate        # enables commands such as `flask run` (see later)
pip install -r requirements.txt # installs Python dependencies
```
For the same above step on Windows:
```bash
python3.8 -m venv venv # or "py" instead of "python3.8", depending on your installation
venv\Scripts\Activate
pip install -r requirements.txt
```

Then (for both OS, from now on), create the static content that will be served by running:
```bash
cd templates
npm install
npm run local
```

Finally you can run your server by executing in the root path:
```bash
cd ..            # if you have followed all the previous steps
flask create_all # Create database and tables
flask run        # Start the server
```

By default, a web page will be served at http://127.0.0.1:5000/.
