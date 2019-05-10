import ctypes


class PyObject(ctypes.Structure):
    pass


PyObject._fields_ = [("ob_refcnt", ctypes.c_int), ("ob_type", ctypes.POINTER(PyObject))]


class Members(PyObject):
    _fields_ = [("dict", ctypes.POINTER(PyObject))]


def get_members(typ: type) -> dict:
    attrs = getattr(typ, "__dict__", typ.__name__)
    pointer = Members.from_address(id(attrs))

    _dummy = {}
    ctypes.pythonapi.PyDict_SetItem(
        ctypes.py_object(_dummy), ctypes.py_object(typ.__name__), pointer.dict
    )

    return _dummy[typ.__name__]
