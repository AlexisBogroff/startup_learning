# How to run the virtual website

- Open a terminal
- Go to a location where you want to place a new virtual environment (using the command "cd" to move along the directories, and "ls" to display what is contained in the folder)
- Create a virtualenv (using Python3): "virtualenv [envName] -p python3.6"
- Go inside this new folder: "cd [envName]"
- Activate this new environment: "source bin/activate" (on Mac)
- Install Django using pip: "pip install django"
- Go to the folder containing the code that I provided (you should be able to see a file named manage.py in your folder)
- Write the command: "python3 manage.py runserver"
- Click the link (or copy the adress in your ), which is http://127.0.0.1:8000/


## The terminal should display something like:

"Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 3 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth.
Run 'python manage.py migrate' to apply them.

September 30, 2019 - 20:26:40
Django version 2.2.5, using settings 'project_esilv.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C."
