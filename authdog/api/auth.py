from authdog.common.encrypt import compare_password, make_password


def identify_with_password(context=None, *args, **kwargs):
    """DATA example for context
    context = request.POST.get("auth")
        if use password for identity:
        {
            "auth": {
                "identity": {
                    "methods": "password",
                    "password": {
                        "user": {
                            "name": "admin",
                            "domain": {
                                "name": "Default"
                            },
                            "password": "devstacker"
                        }
                    }
                }
            }
        }

    :param context: context is the data from request: context = request.POST.get("auth")
    :param args:
    :param kwargs:
    :return:
    """
    identity = context.get("identity")
    method = identity.get("methods")
    password = identity.get("password")
    if method == "password":
        pass
    else:
        message = "this method can only handle identity methods: password "
        return {"code": 500, "message": message}


def identify_with_token(context=None, *args, **kwargs):
    """DATA example for context
    if use token for identity
    {
        "auth": {
            "identity": {
                "methods": "token",
                "token": {
                    "id": "'$OS_TOKEN'"
                }
            }
        }
    }
    :param context: context is the data from request: context = request.POST.get("auth")
    :param args:
    :param kwargs:
    :return:
    """
    identity = context.get("identity")
    method = identity.get("methods")
    password = identity.get("token")
    if method == "token":
        pass
    else:
        message = "this method can only handle identity methods: token"
        return {"code": 500, "message": message}
