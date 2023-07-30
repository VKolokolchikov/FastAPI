import hashlib
import hmac
import traceback
from urllib.parse import unquote

from app.middleware.utils import prepare_check_string
from app.settings import settings
from commons.logger import get_logger

logger = get_logger('api-server', extra={'middleware': 'auth'})


def validate_auth_data(
        *,
        auth_data: str,
        token: str,
        constant_string: str = settings.tg_constant_string,
        separate_hash: str = settings.tg_separate_hash
):
    """
    Validates the data received from the Telegram web app, using the
    method documented here:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    auth_data - A string with raw data transferred to the Web App
    token - Telegram bot's token
    constant_string - constant string (default = "WebAppData")
    separate_hash - A symbol to separate the hash part
    """
    try:
        # Отделение проверяемых данных от валидного хеша
        auth_data, valid_hash = unquote(auth_data).split(separate_hash)
        # Обработка проверяемых данных согласно документации
        data_check_str = prepare_check_string(auth_data)

        secret_key = hmac.new(constant_string.encode(), token.encode(), hashlib.sha256).digest()
        data_check = hmac.new(secret_key, data_check_str.encode(), hashlib.sha256)
    except Exception as exc:
        logger.exception(exc, extra={
            'exception': traceback.format_exception(exc),
            'exception_handler': f'{exc.__class__.__name__}',
        })
    else:
        if data_check.hexdigest() == valid_hash:
            return auth_data

        logger.warning("Code not valid")
