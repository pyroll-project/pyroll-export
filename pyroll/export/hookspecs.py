from pyroll.export.pluggy import hookspec


@hookspec(firstresult=True)
def convert(name: str, value: object):
    """"""
