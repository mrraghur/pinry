from database import connectToDatabase, getAllUrlsToBeScraped, addUrlsToBeScraped, markUrlAsScraped
import sys

urlsToBeAdded = open(sys.argv[1]).read().split()

conn = connectToDatabase("../db.sqlite3")
addUrlsToBeScraped(conn, urlsToBeAdded)
conn.commit()
conn.close()
