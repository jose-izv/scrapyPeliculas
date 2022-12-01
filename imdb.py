import scrapy

# https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=CJJCC2GS7BA7JWY038D0&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1
class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    # 1. visitar imdb por género, género comedia
    start_urls = ['https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=CJJCC2GS7BA7JWY038D0&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1']
    count = 0

    def parse(self, response):
        movies = response.css('div.lister-list > div > div.lister-item-content')
        next_page=response.css("div.desc > a::attr(href)").get()
        link_next_page = "https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=CJJCC2GS7BA7JWY038D0&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1"+next_page
                
        for movie in movies:
            """ 1. Obtener el link de las películas de género comedia """
            genero = movie.css('p.text-muted > span.genre::text').get()
            href = movie.css('a::attr(href)').get()
            link_comedia = "https://www.imdb.com"+href

            """ 3. durante esa visita, visitar cada una de las películas para obtener la siguiente información """
            # a) puesto
            puesto = movie.css('h3.lister-item-header > span::text').get()
            # b) titulo
            titulo = movie.css('h3.lister-item-header > a::text').get()
            
            yield response.follow(url = link_comedia, callback=self.parse_reviews, meta = {'puesto': puesto, 'titulo':titulo})
           
        #yield response.follow(url = link_next_page, callback = self.parse)
        

        """ 2. visitar las 6 primeras páginas y obtener las 50 películas de cada página """
        if self.count < 5:
            self.count += 1
            yield response.follow(url = response.css(".nav a.next-page::attr(href)").get(), callback = self.parse)

    def parse_reviews(self, response):
        # c) director
        directores = response.css("ul.sc-bfec09a1-8 li:nth-child(1) li a::text").getall()
        # d) director
        escritores = response.css("ul.sc-bfec09a1-8 li:nth-child(2) li a::text").getall()
        # e) actores
        actores = response.css(".sc-bfec09a1-7 > a::text").getall()
        # f) el numero de reseñas de usuarios y critico
        resenas = response.css("ul.sc-3ff39621-0 .score::text").getall()
        
        print('PELICULA:', response.meta.get('puesto'), response.meta.get('titulo'),"\n", "NUMERO RESEÑAS DE USUARIOS Y CRÍTICOS:", resenas, "\n", "DIRECTOR(ES):", directores, "\n", "ESCRITOR(ES):", escritores, "\n", "ACTORES:", actores)

            







        # for movie in movies:
            # title = movie.css('a::text').get()
            # 1º conseguir el enlace (opcion1)
            # href = movie.css('a::attr(href)').extract()
            # link = 'https://www.imdb.com' + href[0]
            # 1º conseguir el enlace (opcion2)
            # href2 = movie.css('a::attr(href)').get()
            # link2 = 'https://www.imdb.com' + href2
            # # 2º español
            # print('MOVIE', title, link2)
            # break
        
        
            # yield {
            #     'GENERO': genero,
            #     'PUESTO': puesto,
            #     'TITULO': titulo
            # }
