from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

im_dict: Final[Mapping] = MappingProxyType({})
