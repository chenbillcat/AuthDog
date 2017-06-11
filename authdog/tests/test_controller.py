from unittest import TestCase
from webtest import TestApp
from authdog.tests import FunctionalTest


class TestRootController(FunctionalTest):
    
    def test_index(self):
        resp = self.app.get('/')
        assert resp.status_int == 200

    def test_get_not_found(self):
        resp = self.app.get('/books/2', expect_errors=True)
        assert resp.status_int == 404


class TestDomainsController(FunctionalTest):
    def test_get_all(self):
        resp = self.app.get('/domains/')
        assert resp.status_int == 200

    def test_get_one(self):
        resp = self.app.get('/domains/1')
        assert resp.status_int == 200

    def test_post(self):
        resp = self.app.post('/domains', params={})
        assert resp.status_int == 200

    def test_patch(self):
        resp = self.app.patch('/domains/1')
        assert resp.status_int == 200

    def test_delete(self):
        resp = self.app.delete('/domains/1')
        assert resp.status_int == 200

    def test_get_notfound(self):
        resp = self.app.get('/domains/1/books', expect_errors=True)
        assert resp.status_int == 404

