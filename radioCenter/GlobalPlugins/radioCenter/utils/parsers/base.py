from abc import ABC
import requests

from logHandler import log


class BaseParser(ABC):

    def get_request(self, url: str):
        content = ""

        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.content.decode("utf-8")
        except Exception as error:
            log.error(error, exc_info=True)

        return content
