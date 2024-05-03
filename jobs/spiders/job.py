import scrapy
from scrapy.http import Response


class JobSpider(scrapy.Spider):
    name = "job"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-it-python/?advs=1"]

    def parse(self, response: Response, **kwargs) -> Response:
        jobs_link = response.css("div.card.card-hover.card-search > div > h2 > a")
        for job_link in jobs_link:
            yield response.follow(job_link, callback=self.parse_job)

        next_page = response.css("ul.pagination > li.circle-style:last-child > a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_job(self, response: Response) -> dict:
        return {
            "title": self._get_title(response),
            "technologies": self._get_technologies(response)
        }

    def _get_title(self, response: Response) -> str:
        return response.css("#h1-name::text").get()

    def _get_technologies(self, response: Response) -> list[str]:
        technologies_tag = response.css("div.flex.toggle-block.toggle-block>span")
        return [
            technology.css(".ellipsis::text").get()
            for technology in technologies_tag
        ]
