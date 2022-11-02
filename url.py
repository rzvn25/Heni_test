from urllib.parse import urlencode, parse_qs, urlsplit, urlunsplit
from collections import namedtuple


def get_url_params(url: str) -> dict:
    if None == url:
        return {}

    if '?' in url:
        url = url.split('?', 1)[1]

    params = parse_qs(url)

    for key, value in params.items():
        if 2 > len(value):
            params[key] = value[0]

    return params


def get_url_path(url: str) -> str:
    _, _, path, _, _ = urlsplit(url)

    return path


def get_url_base(url: str) -> str:

    scheme, netlock, _, _, _ = urlsplit(url)

    return '{}://{}'.format(scheme, netlock)


def override_url_params(url: str, params: dict) -> str:
    """
    Given a URL, set or replace a query parameter and return the
    modified URL.
    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    new_query_string = ""
    for param_name, param_value in params.items():
        query_params[param_name] = [param_value]
        new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))


def remove_url_params(url: str, params: list) -> str:
    """
    Given a URL, remove query parameters and return the modified URL.
    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    for param_name in params:
        query_params.pop(param_name, None)

    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))


def override_url_parts(url: str, parts_to_override: dict) -> str:
    """
    Given an URL this function overrides parts from it

    :param url: The url that parts will be overrides
    :param parts_to_override: A dictionary with parts that will be override in given url.
     Ex: {'scheme': 'https', 'netloc': 'www.google.com', 'path': 'aaa', 'query': 'a=1&b=2', 'fragment': ''}
    :return: Changed url
    """
    url_split = urlsplit(url)
    url_dict = url_split._asdict()

    for key, value in url_dict.items():
        if key in parts_to_override.keys():
            url_dict[key] = parts_to_override.get(key)

    return urlunsplit(namedtuple('GenericDict', url_dict.keys())(**url_dict))
