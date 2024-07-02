from typing import (
    TypeVar as _TypeVar,
    Protocol as _Protocol
)

_T_contra = _TypeVar("_T_contra", contravariant=True)

class SupportsRead(_Protocol[_T_contra]):
    def read(self, stream: _T_contra, /): ...
