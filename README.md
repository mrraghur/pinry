# ![Pinry](https://raw.github.com/pinry/pinry/master/docs/src/imgs/logo-dark.png)

The open-source core of Pinry, a tiling image board system for people
who want to save, tag, and share images, videos and webpages in an easy
to skim through format.

For more information ( screenshots and document ) visit [getpinry.com](https://getpinry.com).

## Features

- Image fetch and online preview
- Tagging system for Pins
- Browser Extensions
- Multi-user support
- Works well with docker
- Both public and private boards (add @2020.02.11)
- Search by tags / Search boards with name (add @2020.02.14)

## To Run the service

- `git clone http://github.com/anooj-gandham/pinry`

To run the backend

- `pip install -r requirements.txt`
- `python manage.py migrate`
- `pipenv run python manage.py createsuperuser`
- `python manage.py runserver`
- In separate terminal `http POST http://localhost:8000/api-token-auth/ username="<superuser name>" password="<superuser password>"`
This will generate auth token for accessing backend, paste this token in /scrapeGithub/scrapeImages.py

To run Frontend

- `cd pinry-spa && yarn serve`

To run Scraper

- `cd scrapeGithub`
- Add Github Repository Urls to urls_to_be_scraped table in db.sqlite3
  `INSERT INTO urls_to_be_scraped (url) VALUES (<url1>), (<url_2>)...`
- Or if there urls stored in file(Each line a new url), then insertUrls.py can be used to insert them to database.
  `python insertUrls.py <filename.txt>`
- `scrapy crawl images`

To view the urls in database
`SELECT url,isScraped FROM urls_to_be_scraped`

To run Nginx

- copy pinry.conf from the project directory to /etc/nginx/conf.d/
- remove dist if it exists from pinry-spa and run `yarn build`
- copy dist to /var/www/pinry and change the appropriate user permissions to nginx (`sudo chown -R nginx:nginx dist`)
- `chmod 710 /var/www/pinry/dist/`
- `sudo setenforce 0`
https://stackoverflow.com/questions/16808813/nginx-serve-static-file-and-got-403-forbidden



#BUGS
- Unable to push gifs through the scraper pipeline
- Clean exit to code if unable to download image(scrapeGithub/image.py)
- Scraper is stuck after some time of scraping (may be memory issues in my machine)
- When a pin is deleted, the tags of pin are not deleted
