import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from americanas.items import AmericanasItem
from scrapy_playwright.page import PageMethod, PageCoroutine


class AmericanasspiderSpider(CrawlSpider):
    name = 'americanas'
    allowed_domains = ['americanas.com.br', 'www.americanas.com.br']
    # start_urls = ['https://www.americanas.com.br/categoria/tv-e-home-theater']

    rules = (
        Rule(LinkExtractor(
            allow='categoria/tv-e-home-theater',
            deny=['/g/.*', '/f/.*', '/l/.*']
        )),
        Rule(LinkExtractor(allow='produto'), callback='parse_item', follow=True),
    )


    def start_requests(self):
        # GET request
        yield scrapy.Request(
            url = "https://www.americanas.com.br/categoria/tv-e-home-theater",
            meta = dict(
                playwright = True,
                playwright_include_page = True,
                playwright_page_methods = [
                    PageMethod('wait_for_selector', 'div.card'),
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageMethod('wait_for_selector', 'div.src__Card-sc-1jbhugd-1.src__ProductWrapper-sc-1jbhugd-6.faWcR'),
                ],
                errback=self.errback,
            ),
            headers =  {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            }
        )

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    def parse_item(self, response):

        # Caso o produto seja vendido e entregue por Americanas
        if response.css('div.offers-box__Wrapper-sc-189v1x3-0.kegaFO p::text').getall() == ['Este produto é vendido e entregue por ', '.']:
            item = AmericanasItem()
            item['gtin'] = response.css('td.spec-drawer__Text-sc-jcvy3q-5.fMwSYd::text')[3].get()
            item['descricao'] = response.css('h1.product-title__Title-sc-1hlrxcw-0.jyetLr::text').get()
            item['preco'] = response.css('div.styles__PriceText-sc-x06r9i-0.dUTOlD.priceSales::text').get()
            item['url'] = response.url
            item['url_photo'] = response.css('img.src__LazyImage-sc-xr9q25-0.eoRxRL::attr(src)').get()

            yield item
