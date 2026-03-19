import logging
import inspect
from . import no_instance

TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")

def as_trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kwargs)
logging.Logger.trace = as_trace

@no_instance
class LogMan:
    @staticmethod
    def _get_logger_context():
        try:
            caller_frame = inspect.stack()[2].frame
            module_name = caller_frame.f_globals.get("__name__", "UNKNOWN")
            return logging.getLogger(module_name)

        except Exception as e:
            return logging.getLogger("root")

    @staticmethod
    def log_trace(msg: str, *args, tmpl="[ TRACE ]: ") -> None:
        """Logs important information as TRACE (from tmpl).
        Args:
            msg (str): The information that needs to be logged.
            tmpl (str, optional): Prefix string to use for trace, defaults to "[ TRACE ]:".
        """
        if not msg:
            return

        LogMan._get_logger_context().trace(f"{tmpl}{msg}", *args)

    @staticmethod
    def log_error(msg: str, *args, tmpl: str = "[ ERROR ]: ") -> None:
        """Logs important information as an ERROR (from tmpl).
        Args:
            msg (str): The error that needs to be logged.
            tmpl (_type_, optional): Prefix string to use for error, defaults to "[ ERROR ]:".
        """
        if not msg:
            return

        LogMan._get_logger_context().error(f"{tmpl}{msg}", *args)

    @staticmethod
    def log_warn(msg: str, *args, tmpl: str = "[ WARN ]: ") -> None:
        """Logs important information as a WARN (from tmpl).
        Args:
            msg (str): The error that needs to be logged.
            tmpl (_type_, optional): Prefix string to use for warn, defaults to "[ WARN ]:".
        """
        if not msg:
            return
        LogMan._get_logger_context().warning(f"{tmpl}{msg}", *args)

    @staticmethod
    def log_info(msg: str, *args, tmpl: str = "[ INFO ]: ") -> None:
        """Logs important information as INFO (from tmpl).
        Args:
            msg (str): The error that needs to be logged.
            tmpl (_type_, optional): Prefix string to use for info, defaults to "[ INFO ]:".
        """
        if not msg:
            return

        LogMan._get_logger_context().info(f"{tmpl}{msg}", *args)
