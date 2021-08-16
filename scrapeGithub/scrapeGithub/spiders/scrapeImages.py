import scrapy
from scrapy import Selector
import numpy as np
import pdb
from images import getDimensions
from lxml import etree

from database import getAllUrlsToBeScraped, addUrlsToBeScraped, updateUrlAsScraped

class ScrapeImages(scrapy.Spider):
    name = 'images'
    start_urls = open('githubUrls.txt','r').read().split()

    # pdb.set_trace()

    def completeUrl(self,url): #Function for completion of url if relative url is provided
        if url[0] == '/':
            return 'https://github.com'+url
        return url

    def parse(self, response):
        try:
            readme = response.xpath('//div[@id="readme"]') #Get Readme element of github repo homepage
            if readme == []:
                return
            readme = readme.getall()[0]
            imageUrls = etree.HTML(readme).xpath('//img/@src')
            if imageUrls == []:
                return
            # imageUrls = readme.xpath('//img/@src').getall()
            imageUrls = list(filter(None,imageUrls))
            imageUrls = list(map(self.completeUrl,imageUrls))
            imageDimensions = np.array(list(map(getDimensions,imageUrls)))

            properImages = imageDimensions > 45 #check whether the dimension of image is above 45px
            properImages = properImages[:,0]*properImages[:,1]
            properImageUrls = list(imageUrls[properImages]) #Select the image urls which are proper
            # pdb.set_trace()
            if properImageUrls != []:
                yield( {
                    'repoUrl' : response.url,
                    'imageUrls' : properImageUrls,
                })
        except:
            pdb.set_trace()
