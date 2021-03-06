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


class TestAuthController(FunctionalTest):

    def test_get_not_found(self):
        resp = self.app.get('/auth', expect_errors=True)
        assert resp.status_int == 404


class TestTokensController(FunctionalTest):

    def test_post(self):
        resp = self.app.post('/auth/tokens', params={})
        assert resp.status_int == 200

    def test_get_not_found(self):
        resp = self.app.get('/auth/tokens', expect_errors=True)
        assert resp.status_int == 404

    def test_post_not_found(self):
        resp = self.app.post('/auth/tokens/1', expect_errors=True)
        assert resp.status_int == 404


class TestDomainsController(FunctionalTest):

    def test_get_all(self):
        resp = self.app.get('/domains')
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


class TestGroupsController(FunctionalTest):

    def test_get_all(self):
        resp = self.app.get('/groups')
        assert resp.status_int == 200

    def test_post(self):
        resp = self.app.post('/groups', params={})
        assert resp.status_int == 200

    def test_get_one(self):
        resp = self.app.get('/groups/1')
        assert resp.status_int == 200

    def test_patch(self):
        resp = self.app.patch('/groups/1')
        assert resp.status_int == 200

    def test_delete(self):
        resp = self.app.delete('/groups/1')
        assert resp.status_int == 200

    def test_get_not_found(self):
        resp = self.app.get('/groups/1/people', expect_errors=True)
        assert resp.status_int == 404

    def test_get_not_found_users(self):
        resp = self.app.get('/groups/users', expect_errors=True)
        assert resp.status_int == 404


class TestGroupsUsersController(FunctionalTest):

    def test_get(self):
        resp = self.app.get('/groups/1/users')
        assert resp.status_int == 200

    def test_put(self):
        resp = self.app.put('/groups/1/users/2')
        assert resp.status_int == 200

    def test_head(self):
        resp = self.app.head('/groups/1/users/2')
        assert resp.status_int == 200

    def test_delete(self):
        resp = self.app.delete('/groups/1/users/2')
        assert resp.status_int == 200

    def test_get_not_found(self):
        resp = self.app.get('/groups/1/users/2/hello', expect_errors=True)
        assert resp.status_int == 404


class TestProjectsController(FunctionalTest):

    def test_get_all(self):
        resp = self.app.get('/projects')
        assert resp.status_int == 200

    def test_post(self):
        resp = self.app.post('/projects')
        assert resp.status_int == 200

    def test_get_one(self):
        resp = self.app.get('/projects/1')
        assert resp.status_int == 200

    def test_patch(self):
        resp = self.app.patch('/projects/1')
        assert resp.status_int == 200

    def test_delete(self):
        resp = self.app.delete('/projects/1')
        assert resp.status_int == 200


class TestUsersController(FunctionalTest):

    def test_get_all(self):
        resp = self.app.get('/users')
        assert resp.status_int == 200

    def test_post(self):
        resp = self.app.post('/users', params={})
        assert resp.status_int == 200

    def test_get_one(self):
        resp = self.app.get('/users/1')
        assert resp.status_int == 200

    def test_patch(self):
        resp = self.app.patch('/users/1')
        assert resp.status_int == 200

    def test_delete(self):
        resp = self.app.delete('/users/1')
        assert resp.status_int == 200

    def test_get_users_projects(self):
        resp = self.app.get('/users/1/projects')
        assert resp.status_int == 200

    def test_get_users_groups(self):
        resp = self.app.get('/users/1/groups')
        assert resp.status_int == 200

    def test_get_users_projects_not_found(self):
        resp = self.app.get('/users/1/projects/1', expect_errors=True)
        assert resp.status_int == 404

    def test_get_users_groups_not_found(self):
        resp = self.app.get('/users/1/groups/1', expect_errors=True)
        assert resp.status_int == 404

    def test_get_not_found_p(self):
        resp = self.app.get('/users/projects', expect_errors=True)
        assert resp.status_int == 404

    def test_get_not_found_g(self):
        resp = self.app.get('/users/groups', expect_errors=True)
        assert resp.status_int == 404


class TestRolesController(FunctionalTest):

    def test_get_all(self):
        resp = self.app.get('/roles')
        assert resp.status_int == 200

    def test_post(self):
        resp = self.app.post('/roles', params={})
        assert resp.status_int == 200

    def test_get_one(self):
        resp = self.app.get('/roles/1')
        assert resp.status_int == 200

    def test_patch(self):
        resp = self.app.patch('/roles/1')
        assert resp.status_int == 200

    def test_delete(self):
        resp = self.app.delete('/roles/1')
        assert resp.status_int == 200

    def test_not_found(self):
        resp = self.app.get('/roles/1/what', expect_errors=True)
        assert resp.status_int == 404
