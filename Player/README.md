Setup:
======

Requires python 2.7x installed.
Additionally the requests module should be installed as given here:

	http://docs.python-requests.org/en/master/user/install/#install


Database:
=========

It is recommended to first run the script to add users:

# sh scripts/generate_db_script.sh

Enter the number of users to test for. The script will automatically update the local database. 


How to run?
===========
# sh scripts/run_simulation.sh

	Answer the question about the approximate number of concurrent threads to create.

Additional tuning?
==================

UserSession.py: Change the URL variable to point to your server / port

