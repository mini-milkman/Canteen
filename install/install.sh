sudo apt install -y python3 python3-pip python3-django python3-pandas python3-mysqldb
for req in $(cat requirements.txt); do 
    pip3 install -U $req; 
done

cd ..
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput --no-post-process --clear --link
python3 manage.py import_initial_settings
python3 manage.py createsuperuser
