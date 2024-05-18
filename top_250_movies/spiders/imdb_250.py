# Для следующего задания предлагаю выбрать сайт "www.imdb.com", который содержит каталог 
# фильмов. На этом сайте можно найти различные списки фильмов, их рейтинги, режиссеров, года выпуска

# Задание для парсинга 4-х полей с сайта "www.imdb.com":
# 1. Название поля: Название фильма
# 2. Название поля: Год выпуска
# 2. Название поля: Рейтинг фильма
# 3. Название поля: Режиссер




import scrapy

class Imdb250Spider(scrapy.Spider):
    name = "imdb_250"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse(self, response):
        movies = response.xpath('//div/main/div/div[3]/section/div/div[2]/div/ul/li/div[2]/div/div/div[1]/a/h3')
        years = response.xpath('//div/main/div/div[3]/section/div/div[2]/div/ul/li/div[2]/div/div/div[2]/span[1]')
        ratings= response.xpath('//div/main/div/div[3]/section/div/div[2]/div/ul/li/div[2]/div/div/span/div/span')
        link = response.xpath('//div/main/div/div[3]/section/div/div[2]/div/ul/li/div[2]/div/div/div[1]/a')
        for item in zip(movies, ratings, years, link):
            name = item[0].xpath(".//text()").get()
            rating = float(item[1].xpath(".//text()").get())
            year = item[2].xpath(".//text()").get()
            link = item[3].xpath(".//@href").get()
            yield response.follow(url=link, callback = self.parse_movie, meta={'name': name, 'rating': rating, 'year': year})
            # print(name, rating, year, link)

    def parse_movie(self, response):

        rows = response.xpath("//main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a")
        for item in rows:
            director = item.xpath(".//text()").get()
            name = response.request.meta['name']
            rating = response.request.meta['rating']
            year = response.request.meta['year']
            yield{
                'name' : name,
                'year' : year,
                'rating' : rating,
                'director': director
            }
