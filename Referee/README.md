### Pingpong Referee Get Started

## Run Application Referee
Install dependencies for `pingpong Referee` using pip:

    $ cd Referee
    $ pip install -r requirements.txt

The app uses gunicorn WSGI. To run `pingpong Referee`:

    $ gunicorn -b 0.0.0.0:8000 "pingpong.app:create_app()"


## Settings

Setting can be edited in the file `config/settings.py`

* The following settings are used by the application:
    - `PLAYERS` is a dict of players with their id as keys. 
    - `MAX_SCORE` is the maximum score a player has to reach to win.


## REST API Routes

* The following API routes used by the application:
    - `/` used by the dashboard ui
    - `/api/authentication` used by the players for authentication
    - `/api/logout` used by the players to end session and logout
    - `/api/keepalive` used by the players to poll tournament state
    - `/api/attack/:gid` used by the offensive player to send attack
    - `/api/defend/:gid` used by the defensive player to send defense
    - `/api/checkgame` used by the players to poll game state
    - `/api/gamestatus` used by the dashboard ui to update view