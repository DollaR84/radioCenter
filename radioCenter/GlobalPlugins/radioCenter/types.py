from enum import Enum

import addonHandler


addonHandler.initTranslation()


class SortType(Enum):
    Nothing = _('nothing')
    NameDirect = _('name direct')
    NameReverse = _('name reverse')
    PriorityDirect = _('priority direct')
    PriorityReverse = _('priority reverse')
    Manual = _('manual')


class PriorityType(Enum):
    High = _('high')
    Middle = _('middle')
    Low = _('low')


class SoundType(Enum):
    Failure = 0
    Move = 1
