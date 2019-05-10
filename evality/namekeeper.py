import builtins
import faulthandler
import types
from collections import defaultdict
from contextlib import contextmanager

from sww import get_members

FORBID_ACCESS = ["open", "exec", "eval", "compile", "input"]
FORBID_BY_TYPE_ACCESS = {
    types.FunctionType: ["__code__", "__globals__", "__closure__"],
    types.FrameType: ["f_locals", "f_globals", "f_builtins", "f_code"],
    types.GeneratorType: ["gi_frame", "gi_code"],
    type: ["__subclasses__", "__bases__"],
}

faulthandler.enable()


class NameKeeper:
    @contextmanager
    def secure_scope(self):
        _fa = {}
        _fbta = defaultdict(dict)
        _imp = None
        try:
            for forbidden in FORBID_ACCESS:
                _fa[forbidden] = builtins.__dict__.pop(forbidden)

            for typ, forbids in FORBID_BY_TYPE_ACCESS.items():
                members = get_members(typ)
                for forbidden in forbids:
                    _fbta[typ][forbidden] = members.pop(forbidden)

            _imp = builtins.__import__
            builtins.__import__ = self._dummy
            yield
        finally:
            for unforbidden, val in _fa.items():
                builtins.__dict__[unforbidden] = val

            for typ, unforbids in _fbta.items():
                members = get_members(typ)
                for unforbidden, val in unforbids.items():
                    members[unforbidden] = val

            builtins.__import__ = _imp

    @staticmethod
    def _dummy(*args, **kwargs):
        return None
