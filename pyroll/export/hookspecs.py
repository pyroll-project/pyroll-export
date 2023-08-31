from pyroll.export.pluggy import hookspec


@hookspec(firstresult=True)
def convert(name: str, value: object, parent: object):
    """
    Hook used to convert PyRolL objects to dict trees for exporting.

    :param name: name of the variable resp. attribute the object was assigned to
    :param value: the object itself
    """
