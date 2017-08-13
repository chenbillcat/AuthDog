import time

import jwt

from authdog.common.encrypt import validate_password, make_password
from authdog.common.encrypt import validate_token, make_token
from authdog.tests import FunctionalTest


class TestEncryptPassword(FunctionalTest):

    def test_validate_password(self):
        input_password = "qazwsx"
        diff_password = "7ujm6yhn"
        stored_mix_password = make_password("qazwsx")

        result = validate_password(input_password, stored_mix_password)
        self.assertEqual(result, True)
        result = validate_password(diff_password, stored_mix_password)
        self.assertEqual(result, False)

    def test_make_password(self):
        password = "qazwsx"
        mix_str = make_password(password)
        assert len(mix_str.strip().split(":")) == 2


class TestEncryptToken(FunctionalTest):

    def test_make_token(self):
        context = {}
        context["user"] = "demo"
        context["role"] = "demo"
        context["is_admin"] = "False"
        context["group"] = "demo"
        token = make_token(context, expire=5)
        assert token

    def test_validate_token(self):
        context = {}
        context["user"] = "demo"
        context["role"] = "demo"
        context["is_admin"] = "False"
        context["group"] = "demo"
        token = make_token(context, expire=5)
        res = validate_token(token)
        assert res
        time.sleep(5)
        try:
            res = validate_token(token)
        except Exception as e:
            assert isinstance(e, jwt.exceptions.ExpiredSignatureError)





