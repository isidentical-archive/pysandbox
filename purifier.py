import ast


class Insecure(Exception):
    pass


def insecure(func):
    def wrapper(instance, node):
        try:
            func(instance, node)
        except Insecure:
            raise Insecure(
                f"{node.__class__.__name__} found in line {node.lineno}:{node.col_offset}"
            )

    return wrapper


class Purifier(ast.NodeVisitor):
    """Tries to dedect *basic* security falls. Of course it can
    be hacked by using dot access model, bytecode etc. The purpose
    is avoiding as much as we can"""

    @insecure
    def visit_Import(*args):
        raise Insecure

    @insecure
    def visit_ImportFrom(*args):
        raise Insecure

    @insecure
    def visit_Attribute(self, node):
        if isinstance(node.value, ast.NameConstant):
            raise Insecure
