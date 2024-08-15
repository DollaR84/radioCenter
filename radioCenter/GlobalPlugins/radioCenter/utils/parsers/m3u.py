import os
from typing import Dict, List, Optional

from logHandler import log

from .base import BaseParser

from .data import ItemData


class M3UParser(BaseParser):

    def __init__(
            self,
            url: Optional[str] = None,
            name: Optional[str] = None,
            base_path: Optional[str] = None,
    ):
        self.url = url
        self.name = name
        self.base_path = base_path

        if self.url and not self.name:
            self.name = self.url.rsplit(r"/", 1)[1].replace(".m3u", "")

    def get_data(self) -> List[ItemData]:
        results = []

        if self.url:
            data = self.get_data_from_url()
        elif self.base_path:
            data = self.get_data_from_path(self.base_path)
        else:
            return results

        for name, urls in data.items():
            for url in urls:
                results.append(ItemData(name=name, url=url))

        return results

    def get_data_from_url(self) -> Dict[str, List[str]]:
        data = self.get_request(self.url)
        return {self.name: self.get_urls_from_m3u(data)}

    def get_data_from_path(self, folder: str) -> Dict[str, List[str]]:
        results = {}

        subfolders = [subfolder for subfolder in os.listdir(folder) if os.path.isdir(os.path.join(folder, subfolder))]
        files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]

        for file in files:
            try:
                file_name, file_ext = os.path.splitext(file)
                if file_ext.lower() != ".m3u":
                    continue

                with open(os.path.join(folder, file), "r", encoding="utf-8") as file_data:
                    results[file_name] = self.get_urls_from_m3u(file_data.read())
            except Exception as error:
                log.error(f"Error read file: {file} in {folder}")
                log.error(error, exc_info=True)

        for subfolder in subfolders:
            results.update(self.get_data_from_path(os.path.join(folder, subfolder)))

        return results

    def get_urls_from_m3u(self, data: str) -> List[str]:
        urls = []

        for line in data.splitlines():
            line = line.strip()
            line_start = line[:4]

            if line_start.lower().startswith("http"):
                urls.append(line)

        return urls
