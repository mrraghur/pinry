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
- `python manage.py runserver`

To run Frontend

- `cd pinry-spa && yarn serve`

To run Scraper

- Add Github Repository Urls to urls_to_be_scraped table in db.sqlite3
  `INSERT INTO urls_to_be_scraped (url) VALUES (<url1>), (<url_2>)...`
- `cd scrapeGithub`
- `scrapy crawl images`
