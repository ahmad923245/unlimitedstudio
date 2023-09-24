echo " BUILD START"
python3.8 -m pip install -r requirement.txt
python3.8 manage.py collectstatic --noinput --clear
python3.8 manage.py runserver --noinput --clear
echo " BUILD END"