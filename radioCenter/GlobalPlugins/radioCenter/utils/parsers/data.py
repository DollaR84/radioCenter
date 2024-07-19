from dataclasses import dataclass, field


@dataclass(slots=True)
class ItemData:
    name: str
    url: str
    info: list[str] = field(default_factory=list)

    def add_info(self, *infos):
        for info in infos:
            self.info.append(info)
