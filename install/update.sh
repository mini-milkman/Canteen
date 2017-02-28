cd ..
git pull
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput --no-post-process --clear --link
python3 manage.py import_initial_settings
