"""Logger"""

import logging


class LoggerAdapter(logging.LoggerAdapter):
    """Logger adapter"""
    def get_extra(self):
        """Get extra from adapter"""
        return self.extra

    def process(self, msg, kwargs):
        """Process message"""
        if self.extra is None:
            return msg, kwargs

        if kwargs.get('extra', None) is None:
            kwargs['extra'] = self.extra
        else:
            kwargs['extra'].update(self.extra)

        return msg, kwargs


def get_logger(name: str | None, extra: dict | None = None):
    """Make logger"""
    logger = logging.getLogger(name)
    return LoggerAdapter(logger, extra)
