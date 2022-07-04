import scrapy
import csv

class FranchizeSpider(scrapy.Spider):
    name = "franch"
    start_urls = ['https://www.franchisedirect.com/top100globalfranchises/']
    
    def parse(self, response):
        year = 2022
        for url in response.css('ul.reportsList a.btn.navy::attr(href)'):
            yield scrapy.Request(url=url.get(), callback=self.parse_items,)
            with open(f"ranks{year}.csv", "w") as csv_file:
                writer = csv.writer(csv_file, delimiter="\n")
                writer.writerow(['Rank, Name, Country, Industry, URL,'])
            year -= 1
            
    def parse_items(self, response):
        year = response.css('h1.pageTitle::text').get().replace('Top 100 Franchises ', '')
        for row in response.css('tbody tr'):
            rank = row.css('td:nth-child(1) .tablesaw-cell-content::text').get()
            name = row.css('.tablesaw-cell-content span::text').get()
            country = row.css('td:nth-child(4) .tablesaw-cell-content::text').get()
            industry = row.css('td:nth-child(5) a::text').get()
            url = row.css('.tablesaw-cell-content a::attr(href)').get()
            with open(f"ranks{year}.csv", "a+") as csv_file:
                write = csv.writer(csv_file)
                write.writerow([rank, name, country, industry, url])
            yield{
                'Rank': rank,
                'Name': name,
                'Country': country,
                'Industry': industry,
                'URL': url,
            }
        next_page = response.xpath("//div[@class='col span2point4']/a[@class='btn select blue ']/parent::div/following-sibling::div/a[@class='btn grey']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_items)