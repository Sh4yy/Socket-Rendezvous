import functools
from flask import g, request, abort
from Controllers.Controller import Controller


def authorized(func):
    """
    decorator is used for authorized routes
    :param func: inner fun
    :return: decorated function
    """

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            return abort(400)

        try:
            method, token = auth.split(' ', 1)
        except:
            return abort(400)

        if method != 'Bearer' or not token:
            return abort(400)

        client_id = Controller.get_private_to_id(token)
        if not client_id:
            return abort(400)

        g.client_id = client_id
        g.private_id = token

        return func(*args, **kwargs)

    return inner_func
