import scrapy
import pdb, json
from lxml import etree
import requests

from database import connectToDatabase, getAllUrlsToBeScraped, addUrlsToBeScraped, markUrlAsScraped, markUrlAsInvalid
import tensorflow as tf
from images import checkIsLogo

class ScrapeImages(scrapy.Spider):
    name = 'images'
    conn = connectToDatabase("../db.sqlite3")
    # start_urls = ['https://github.com/anooj-gandham/inv_prob','https://github.com/typesense/typesense-instantsearch-adapter','https://github.com/facebook/create-react-app']
    start_urls = getAllUrlsToBeScraped(conn)

    conn.commit()
    conn.close()
    model1 = tf.keras.models.load_model('../logoclassifiermodel_MobileNet')
    print('Logo classifier model loaded')

    def completeUrl(self,url): #Function for completion of url if relative url is provided
        if len(url)> 0:
            if url[0] == '/':
                return 'https://github.com'+url
            return url
        return url
    def checkForRepoUrl(self,u): #TODO Add proper logic to check for valid github repo
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
                conn = connectToDatabase("../db.sqlite3")
                markUrlAsInvalid(conn, response.url)
                conn.commit()
                conn.close()
                return
            imageTags = []
            for tag in response.xpath('//a[@class="topic-tag topic-tag-link"]/text()').getall(): #Get tags from about me in github repo
                imageTags.append(tag.split()[0])

            description = response.xpath('//p[@class="f4 mt-3"]/text()').getall()
            if description != []:
                description = description[0]
            else: #TODO Fill with alternate content
                description = ""
            # pdb.set_trace()
            stars = response.xpath('//a[@class="social-count js-social-count"]/text()').getall()[0].split()[0]
            headers = {
                'Authorization': 'Token 8a5539fe405358243015d7ec5bcec2b644b06a41',
                'Content-Type': 'application/json',
                    }
            postApi = 'http://localhost:8000/api/v2/pins/'

            readme = readme.getall()[0]
            imageUrls = etree.HTML(readme).xpath('//img/@src') #Check for <img> tags and get src attribute from them
            if imageUrls != []:
                imageUrls = list(filter(None,imageUrls)) #Remove empty urls
                imageUrls = list(map(self.completeUrl,imageUrls)) #Complete the urls if relative urls are given
                for img in imageUrls:
                    isLogo = checkIsLogo(img,self.model1)
                    if isLogo == '':
                        return
                    data = {'url':img,'referer':None,'description':description,'tags':imageTags, 'stars':stars,'referer':response.url,'isLogo':isLogo}
                    resp = requests.post(postApi, headers=headers, data=json.dumps(data))

            # Get all <a> tags, extract href attribute from them, check whether url is complete,
            # then check whether given url is a url of Github repo
            githubRepos = list(filter(self.checkForRepoUrl,list(map(self.completeUrl,response.xpath('//a/@href').getall()))))
            githubRepos = list(set(githubRepos)) #Remove duplicates of repo urls
            #Extracted text using xpath instead of beautiful soup
            readmeText = ''.join(etree.HTML(readme).xpath('//text()')).replace('\n',' ').replace('  ','').replace('  ','').replace('"',"'")

            conn = connectToDatabase("../db.sqlite3")

            addUrlsToBeScraped(conn,githubRepos)
            markUrlAsScraped(conn,response.url,readmeText) #TODO Need to add logic to check whether repo has bee scraped successfully

            # pdb.set_trace()
            conn.commit()
            conn.close()
        except:
            pdb.set_trace()
