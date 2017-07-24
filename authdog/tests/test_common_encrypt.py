from authdog.common.encrypt import compare_password, make_password
from authdog.tests import FunctionalTest


class TestEncryptPassword(FunctionalTest):

    def test_compare_password(self):
        input_password = "qazwsx"
        diff_password = "7ujm6yhn"
        stored_mix_password = make_password("qazwsx")

        result = compare_password(input_password, stored_mix_password)
        self.assertEqual(result, True)
        result = compare_password(diff_password, stored_mix_password)
        self.assertEqual(result, False)

    def test_make_password(self):
        password = "qazwsx"
        mix_str = make_password(password)
        assert len(mix_str.strip().split(":")) == 2
