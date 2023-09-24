echo " BUILD START"
python -m pip install -r requirement.txt
python manage.py collectstatic --noinput --clear
python manage.py runserver 
echo " BUILD END"