from __future__ import annotations

from enum import Enum

import addonHandler


addonHandler.initTranslation()


class StationStatusType(Enum):
    All = _('all')

    NotVerified = _('not verified')
    NotWork = _('not work')
    Works = _('works')

    @classmethod
    def get_list_values(cls) -> list[str]:
        return [item.value for item in cls]

    @classmethod
    def get_type_by_value(cls, value: str) -> StationStatusType:
        for item in cls:
            if item.value == value:
                return item
