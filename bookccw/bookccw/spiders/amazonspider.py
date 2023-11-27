import scrapy
import json


class AmazonspiderSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["www.americanas.com.br"]
    start_urls = [
        "https://www.americanas.com.br/busca/livro-harry-potter?chave=pc_cat_ct1_1_literatura_e_ficcao",
        "https://www.americanas.com.br/categoria/livros/literatura-e-ficcao/romance?chave=pc_cat_ct1_acom_livros-romance",
        "https://www.americanas.com.br/categoria/livros/hqs-mangas-e-graphic-novel?chave=pc_cat_ct1_acom_livros-mangas",
        "https://www.americanas.com.br/categoria/livros/religiao-e-esoterismo?chave=pc_cat_ct1_acom_livros-religiao",
        "https://www.americanas.com.br/categoria/livros/infantil-e-juvenil/juvenil?chave=pc_cat_ct1_acom_livros-juvenil",
        "https://www.americanas.com.br/categoria/livros/biografias-e-memorias?chave=pc_cat_ct1_acom_livros-biografias",
        "https://www.americanas.com.br/categoria/livros/jogos-e-passatempos?chave=pc_cat_ct1_acom_livros-jogos",
        "https://www.americanas.com.br/categoria/livros/literatura-e-ficcao/suspense-e-terror?chave=pc_cat_ct1_acom_livros-suspense"
    ]

    def parse(self, response):
        yield json.loads(response.css("main script::text").get())

        links = response.css("div *::attr(href)").getall()

        for link in links:
            if "produto" in link:
                print(link)
                yield response.follow(link, callback=self.parse)
