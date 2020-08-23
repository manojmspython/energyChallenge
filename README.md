# EnergyChallenge
The application should be a Django project that runs on Python 3.6 or 3.7.
It should have a management command that can be called with the path to a
NEM13 file (or files). The specification for these files is included below.
The data for each reading in the file should be extracted and stored in a local
database. The information available for each reading should include, as a
minimum:

● NMI
● Meter serial number
● The reading value
● When the reading happened
● The filename of the flow file

It should provide a version of the Django admin site that allows a user to search
for the reading values and dates associated with either:
● A NMI
● A meter serial number

There should be a test suite and instructions on how to run the tests.

# Environtment Setup (Works in Mac)
Run the following steps to get th application running:
  1. Open a command shell where this README.md is present
  2. run "python3 -m venv env"
  3. run "source env/bin/activate"
  4. run "cd energy"
  5. run "pip install -r requirements.txt"
  6. run "python3 manage.py migrate"
  7. run "python3 manage.py load_nem_file <filepath>" where filepath refers to the nem13 filepath

# Test Usage.
run "python3 manage.py test"

# Usage
1) run "python3 manage.py runserver" in the command shell
2) Navigate to "http://127.0.0.1:8000/admin/backend/nemdata/" in browser.
3) Enter the UserName: admin and Password: Password@12345
4) Now you can search for your serialNumber


That's it. Hope you enjoy this!



