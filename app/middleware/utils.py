import json

from app.settings import settings


def parse_query_params(query):
    query_params = {}
    query = query.split('&')

    for items in query:
        key, value = items.split('=')

        if key in query_params:
            query_params[key] = [query_params[key], value]
            continue

        query_params[key] = value
    return query_params


def prepare_check_string(init_data: str):
    init_data = sorted([item for item in init_data.split(settings.tg_separate_symbol)], key=lambda x: x[0])
    return settings.tg_join_symbol.join(init_data)


def extract_user_from_auth_data(auth_data: str):
    return json.loads(parse_query_params(auth_data)['user'])
