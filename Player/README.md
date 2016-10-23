### Pingpong Player Get Started

## Run Application Player
Install dependencies for `pingpong Player` using pip:

    $ cd Player
    $ pip install -r requirements.txt

The app is standalone and can be simply run using:

    $ python PlayPingPong --username `username`


## Settings

Settings can be edited in the file `config/players.ini`

* The following settings are used by the application:
    - `username` the name of the player, used as login and case sensitive
    - `password` the password for player login, currently same as user name on the server
    - `defense` an integer representing length of defense array
    - `url` to which this application will register for tournament.() 
