# Паук, который будет проходить и получать данные
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader

# Импортируем класс, чтобы передавать на обработку


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']
    #start_urls = ['https://www.castorama.ru/tools/power-tools/cordless-drills-and-screwdrivers']   # Атрибут класса
    #start_urls = ['https://www.castorama.ru/catalogsearch/result/']

    # Объявляем конструктор и переопределяем его
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}']     # Свойство объекта


    def parse(self, response: HtmlResponse):
        print()
        # *********************************************************
        # Получаем новую страницу
        next_page = response.xpath("//div[@class='pages']//a[contains(@title, 'След')]/@href").get()
        if next_page:
            print(next_page)
            yield response.follow(next_page, callback=self.parse)

        # *********************************************************
        # Получаем ссылки на товары
        links = response.xpath("//div[contains(@class, 'category-products')]//a[contains(@class, '__name')]/@href").getall()
        for link in links:
            # Возвращаем
            yield response.follow(link, callback=self.product_parse)

        # *********************************************************
        # Получаем данные товара
    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)

        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//div[contains(@class, 'add-to-cart__price')]//div[contains(@class, 'current-price')]//span[@class='price']//text()")
        loader.add_xpath('photos', "//div[@class='product-media']//img[contains(@class, 'top-slide')]/@data-src")
        loader.add_value('url', response.url)

        yield loader.load_item()

        #name = response.xpath("//h1/text()").get()
        #url = response.url
        #search_price = "//div[contains(@class, 'add-to-cart__price')]" \
        #               "//div[contains(@class, 'current-price')]//span[@class='price']//text()"
        #price = response.xpath(f"{search_price}").getall()
        #photos = response.xpath("//div[@class='product-media']//img[contains(@class, 'top-slide')]/@data-src").getall()


        # делаем экземпляр класса и возвращаем(передаём) его дальше
        #yield JobparserItem(url=url)



