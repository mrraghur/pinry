import requests
import pdb
from database import connectToDatabase, getAllUrlsToBeScraped, addUrlsToBeScraped, markUrlAsScraped

conn = connectToDatabase("../db.sqlite3")

ids = conn.execute('SELECT id FROM core_pin').fetchall()

# pdb.set_trace()

conn.commit()
conn.close()


headers = {
    'Authorization': 'Token 8a5539fe405358243015d7ec5bcec2b644b06a41',
    'Content-Type': 'application/json',
        }
deleteApi = 'http://localhost:8000/api/v2/pins/'

for id in ids:
    deletePinApi = deleteApi + str(id[0])
    print(deletePinApi)
    response = requests.delete(deletePinApi,headers=headers)
    print(response.url, response.status_code)




