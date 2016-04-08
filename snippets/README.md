some commands

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

rm -f tmp.db db.sqlite3
rm -r snippets/migrations
python manage.py makemigrations snippets
python manage.py migrate
python manage.py createsuperuser
heroku local
git stash pop

python manage.py shell

python manage.py startapp snippets
python manage.py shell
sqlite3 db.sqlite3
.databases
.tables
.schema auth_user
select * from auth_user;