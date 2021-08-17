import scrapy
import pdb, json
from lxml import etree
import requests

from database import connectToDatabase, getAllUrlsToBeScraped, addUrlsToBeScraped, updateUrlAsScraped

class ScrapeImages(scrapy.Spider):
    name = 'images'
    conn = connectToDatabase("../db.sqlite3")
    start_urls = getAllUrlsToBeScraped(conn)
    pdb.set_trace()
    conn.commit()
    conn.close()



    def completeUrl(self,url): #Function for completion of url if relative url is provided
        if len(url)> 0:
            if url[0] == '/':
                return 'https://github.com'+url
            return url
        return url
    def checkForRepoUrl(self,u):
        splitUrl = u.split('/')
        if len(u) == 0: #If len of url is zero return False
            return False
        elif len(splitUrl) == 5 and splitUrl[3] in ['features','topics','apps']:
            return False #if url is of this form http://github.com/aaa/bbb
        elif len(splitUrl) == 5 and splitUrl[2] == 'github.com':
            return True
        elif len(splitUrl) == 9 and splitUrl[2] == 'github.com' and splitUrl[5] == 'tree':
            return True
        return False

    def parseTag(self,t):
        return t.split()[0]

    def parse(self, response):
        try:
            readme = response.xpath('//div[@id="readme"]') #Get Readme element of github repo homepage
            if readme == []:
                return
            readme = readme.getall()[0]
            imageTags = []
            for tag in response.xpath('//a[@class="topic-tag topic-tag-link"]/text()').getall(): #Get tags from about me in github repo
                imageTags.append(tag.split()[0])
            stars = response.xpath('//a[@class="social-count js-social-count"]/text()').getall()[0].split()[0]
            imageUrls = etree.HTML(readme).xpath('//img/@src') #Check for <img> tags and get src attribute from them
            headers = {
                'Authorization': 'Token fa965469e96d536925bfffa38a64d0919c511713',
                'Content-Type': 'application/json',
                    }
            postApi = 'http://localhost:8000/api/v2/pins/'

            if imageUrls != []:
                imageUrls = list(filter(None,imageUrls)) #Remove empty urls
                imageUrls = list(map(self.completeUrl,imageUrls)) #Complete the urls if relative urls are given
                for img in imageUrls:
                    data = {'url':img,'referer':None,'description':'','tags':imageTags, 'stars':stars}
                    response = requests.post(postApi, headers=headers, data=json.dumps(data))

            githubRepos = list(filter(self.checkForRepoUrl,list(map(self.completeUrl,response.xpath('//a/@href').getall()))))
            # Get all <a> tags, extract href attribute from them, check whether url is complete,
            # then check whether given url is a url of Github repo
            githubRepos = list(set(githubRepos)) #Remove duplicates of repo urls

            conn = connectToDatabase("../db.sqlite3")
             
            addUrlsToBeScraped(conn,githubRepos)
            updateUrlAsScraped(conn,response.url)
            pdb.set_trace()

            conn.commit()
            conn.close()
        except:
            pdb.set_trace()
