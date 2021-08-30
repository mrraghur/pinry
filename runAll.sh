git clone http://github.com/anooj-gandham/pinry
# run a virtual environemnt for python
pip install -r requirements.txt


cd pinry-spa
yarn install
yarn build
sudo cp -r dist/ /var/www/pinry/

#then delete db.sqlite3 and static/ and paste scraped files from local

cd ..


python manage.py migrate
python manage.py runserver
