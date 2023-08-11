import scrapy

class RedfinScraper(scrapy.Spider):
    name = 'redfin_sale'
    print('')
    print('')
    zipcode = input('Enter your zipcode: ')
    print('')
    print('')
    start_urls = ['https://www.redfin.com/zipcode/' + zipcode]

    def parse(self, response):
        for listings in response.css('div.bottomV2'):
            if(listings.css('span.collapsedAddress::text').get() != 'Beds'):
                yield {
                    'name': listings.css('span.collapsedAddress::text').get(),
                    'price': listings.css('span.homecardV2Price::text').get(),
                    'beds': listings.css('div.HomeStatsV2').css('div.stats::text').get(),
                    'link': 'https://www.redfin.com' + listings.css('a').attrib['href']
                }

            else:
                yield {
                    'name': listings.css('span.collapsedAddress::text').get(),
                    'price': listings.css('span.homecardV2Price::text').get(),
                    'beds': 'No information',
                    'link': 'https://www.redfin.com/' + listings.css('a').attrib['href']
                } 
    
        next =  response.css('a.clickable.goToPage').attrib['href']

        if next is not None:
            yield response.follow(next, callback = self.parse)