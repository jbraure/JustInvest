# Steps done :

[TOC]

## Django project creation
- Create Django project in heroku/ folder : `django-admin startproject justinvest`
- Rename top folder justinvest-project/
- Create git repo in justinvest-project/ :`git init`
- Initial commit in SourceTree
- Create a 'trades' app :`python3 manage.py startapp trades`
- Run server to check... :`python3 manage.py runserver`
  - open http://127.0.0.1:8000
- Make initial migrations :`python3 manage.py migrate`
- Create class HomeView in views.py
- Create Trade model
- Declare the Trades app
- Create home.html in trades/templates/trades/
- Migrate DB :`python3 manage.py makemigrations`
  - `python3 manage.py migrate`
- Migrations must be commited too!  

## Users and authentication
- Create a superuser :`python3 manage.py createsuperuser`
  - With my usual credentials
- Check that Admin console is functional. It should be, at this point.
- Create base.html, footer.html, home.html
- Adds login and logout

## Data display as list
- Open database with "DB Bowser for SQLite" and insert some records.
- Add "trades" list url mapping in urls.py
- Add TradeListView in views.py
- Create list.html

## Add some style
- css ref in base.html
- add css file in static/trades/css/main.css

## Data insertion
- Create form in forms.py
- Add link in home.html
- Adapt urls.py
- Create create.html
- Create TradeForm in forms.py
- Create TradeFormView in views.py

## Change style, use bootstrap
- add tag in base.html

## Heroku deployment
- `cd` into the site folder
- Add DB settings in settings.py
- Add static file setting in settings.py
- Make the requirements.txt using `pip freeze > requirements.txt` to declare the package dependencies. Must be at the same level as the .git. See link (1)
- Make Procfile to declare the start command. See link (1)(3)
- Invoque `heroku create justinvest` to actually create the project on Heroku and receive the git and website urls. See link (3)(8)
https://justinvest.herokuapp.com/ | https://git.heroku.com/justinvest.git
- Run : `git init` then `heroku git:remote -a justinvest` to attach git to the new distant repo.
- Deploy using `git push heroku master` then `heroku ps:scale web=1` and open the website.
- If there's an error, run `heroku logs --tail`.
- And if needed : `heroku apps:destroy` to start over.
- /!\ locations of files matter, if at root or just below.
- Then configure the database on heroku : Put the credentials in environement / config vars. See link (2)(9)
- If needed, run `heroku run python manage.py migrate` to migrate the remote database.
- Run `heroku run python manage.py createsuperuser` to create the Django superuser on the remote database.

## Admin console customization
- edit admin.py

---------------

### Links
- (1) https://devcenter.heroku.com/articles/django-app-configuration
    - Procfile
    - gunicorn package
    - django-heroku package
    - settings.py changes
- (2) https://devcenter.heroku.com/articles/config-vars
    - Heroku (web) dashboard
- (3) http://www.marinamele.com/2013/12/how-to-set-django-app-on-heroku-part-i.html
    - set up Heroku
    - set up PostgreSQL
    - start a Django app in a Virtualenv
    - set the Procfile
    - specify the dependencies
    - separate your applications and your libraries
    - set the settings.py file
    - push your app in Heroku
    - change the name of your app
- (4) http://www.marinamele.com/2013/12/how-to-set-django-app-on-heroku-part-ii.html
    - set different settings.py files for development, production and testing
    - save all the templates of your app in the same location
    - set debug false in production
    - install HTML5 Boilerplate
- (5) http://www.marinamele.com/2014/01/how-to-set-django-app-on-heroku-part-iii.html
    - configure PostgreSQL in your local machine
    - configure PostgreSQL in Heroku
    - syncdb and Django shell in Heroku
- (6) http://www.marinamele.com/2014/02/how-to-deploy-django-app-on-heroku-part.html
    - Install South and run it both on your local machine and on Heroku
    - Prepare your app to support different languages
    - Prepare your app to support Localization
- (7) http://www.marinamele.com/2014/05/postgresql-on-heroku-and-the-pgbackup-add-on.html
    - configure and use PostgreSQL in your Heroku app.
    - perform database backups using the PG Backups add-on.
- (8) https://www.codementor.io/jamesezechukwu/how-to-deploy-django-app-on-heroku-dtsee04d4
    - virtualenv
    - create app on heroku
- (9) https://realpython.com/migrating-your-django-project-to-heroku/
    - transfer the data from the local database to the production database
    - fabric to ease deployment, commits, push etc
    - database config on heroku
    - __local_settings.py__
