from .logman import LogMan

class InstanceException(Exception):
    """InstanceException class for no instance classes.
    Note:
        InstanceException is raised when attempting to
        instantiate a class that should not be
        instantiated through the @no_instance
        decorator.
    """

    def __init__(self, cname, message=None):
        if not message:
            message = f"Instantiation error occurred. You are not allowed to instantiate {cname} class."
        self.cname = cname
        super().__init__(message)


def no_instance(cls):
    """Decorator to prevent instantiation of class.

    Note:
        Will RAISE an Exception when trying to create
        an instance of a '@no_instance' class.
    """

    def _prevent_new(cls_inner, *args, **kwargs):
        raise InstanceException(cls.__name__)

    cls.__new__ = staticmethod(_prevent_new)
    return cls

__version__ = "1.0.0"
__all__ = ["LogMan"]