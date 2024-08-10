from abc import ABC
import requests

from logHandler import log


class BaseParser(ABC):

    @property
    def headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0; Windows 8.1; rv:55.0; Firefox/55.0"
        }

    def get_request(self, url: str):
        content = ""

        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                content = response.content.decode("utf-8")

        except Exception as error:
            log.error(error, exc_info=True)

        return content
