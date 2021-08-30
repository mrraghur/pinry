import requests
import pdb
from database import connectToDatabase, getAllUrlsToBeScraped, addUrlsToBeScraped, markUrlAsScraped

conn = connectToDatabase("../db.sqlite3")

blockedList = ['https://github.com/all-contributors/app',]

toBeDeleted = []
for blockedUrl in blockedList:
    query = f'SELECT id FROM core_pin WHERE referer="{blockedUrl}"'
    toBeDeleted += conn.execute(query).fetchall()

# toBeDeleted = conn.execute('SELECT id FROM core_pin').fetchall()
# Uncomment above to delete all pins
# pdb.set_trace()

conn.commit()
conn.close()

#ENTER valid token generated in your machine or
#TODO change it to env variable
headers = {
    'Authorization': 'Token 21064be4b6a703be0b5cceac361df43dc3b50e81',
    'Content-Type': 'application/json',
        }
deleteApi = 'http://localhost:8000/api/v2/pins/'

for id in toBeDeleted:
    deletePinApi = deleteApi + str(id[0])
    print(deletePinApi)
    response = requests.delete(deletePinApi,headers=headers)
    print(response.url, response.status_code)

