# hirola-database-site
![the mascot](https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Damaliscus_hunteri_The_book_of_antelopes_%281894%29.png/440px-Damaliscus_hunteri_The_book_of_antelopes_%281894%29.png)
## Environment Setup
__What you need:__
* A Python 3 distribution
  * (Either 3.6 or 3.7.0 will work. However, 3.6.6 is on Wiebe)
* Access to that Python 3 dist via CLI

__How to build the virtual environment:__
* Make your way to your directory of the app.

* Run the command:
  ```bash
  python3 -m venv [Desired-Path]
  ```
  * An example of this command would be: 
  ```python3 -m venv ./../.envs/hirola-database-site```
  This installs a new python3 env in ../.envs/hirola-database-site

* Now we need to activate the python env:
  ```bash
  source [Path-to-Env]/bin/activate
  ```
  * An example of this command would be: 
  ```source ../.envs/hirola-database-site/bin/activate```
  This uses the python env. From this point every python3 or pip3 command will use this environment and will not be global.
* Now we need to install requirements: (Do this with activate sourced)
  ```bash
  pip3 install -r requirements.txt
  ```
* Now you can run the app! With the virtualEnv sourced, you can run:
   ```bash
   python3 run.py
   ```
* To stop using this Env, simply type: ``` deactivate ``` now you have access to your global python installation.

