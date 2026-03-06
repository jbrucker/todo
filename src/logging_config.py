"""Configure logging and provide an accessor for the logger."""
import structlog


def configure_logging():
    """One time configuration of logging should be done before first use."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            # Add a 'stack' key to log output, the value is the call stack (may be long).
            structlog.processors.StackInfoRenderer(),
            # automatically adds exception info to log messages when an exception is logged.
            # Can be long, since it includes the full stack trace.
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            # JSON formatting 
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(*args, **kwargs):
    """Return a logger instance."""
    return structlog.get_logger(*args, **kwargs)


# for compatibility with existing code that uses the standard logging module.
getLogger = get_logger