import scrapy


class HkibspiderSpider(scrapy.Spider):
    name = 'hkibspider'
    allowed_domains = ['www.hongkonginsurancebrokers.com']
    start_urls = ['http://www.hongkonginsurancebrokers.com/']

    def parse(self, response):
        for row in response.css('tbody tr'):
                co_name = row.css('td:nth-child(1) .pre::text').extract_first()
                contact = row.css('td:nth-child(2) div::text').extract_first()
                if contact.find("Email") != -1:
                    contact_split = contact.replace(": ", "\n").split("\n")
                    email = contact_split[contact_split.index("Email") + 1].replace(" (at) ", "@").replace(" ", "")
                    yield {
                        'co_name' : co_name,
                        'contact' : email
                    }
        
        next_page = response.css('a.next::attr(href)').extract_first()

        if (next_page):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)

    
