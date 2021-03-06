from .test_setup import TestSetUp


class TestAuthentication(TestSetUp):
    def test_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_register(self):
        res = self.client.post(
            self.register_url, self.register_data, format='json')

        self.assertEqual(res.data['email'], self.register_data['email'])
        self.assertEqual(res.data['username'], self.register_data['username'])
        self.assertEqual(res.status_code, 201)

    def test_login_with_not_data(self):
        self.client.post(
            self.register_url, self.register_data, format='json')
        res = self.client.post(self.login_url)

        self.assertEqual(res.status_code, 400)

    def test_login(self):
        self.client.post(
            self.register_url, self.register_data, format='json')
        res = self.client.post(self.login_url, self.login_data, format='json')

        self.assertEqual(res.status_code, 200)

    def test_refresh_token(self):
        self.client.post(
            self.register_url, self.register_data, format='json')
        refresh_token = self.client.post(
            self.login_url, self.login_data, format='json').data.get('refresh')

        data = {
            'refresh': refresh_token,
        }

        res = self.client.post(self.refresh_token_url, data, format='json')

        self.assertEqual(res.status_code, 200)


class TestAccounts(TestSetUp):
    def test_get_current_account(self):
        self.client.post(
            self.register_url, self.register_data, format='json')
        res = self.client.get(self.account_url)

        self.assertEqual(res.status_code, 200)

    def test_get_account(self):
        self.client.post(
            self.register_url, self.register_data, format='json')
        access_token = self.client.post(
            self.login_url, self.login_data, format='json').data.get('access')

        res = self.client.get(self.account_url, data={
        }, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.assertEqual(res.status_code, 200)

    def test_get_account_quizzes(self):
        self.client.post(
            self.register_url, self.register_data, format='json')
        access_token = self.client.post(
            self.login_url, self.login_data, format='json').data.get('access')

        res = self.client.get(self.account_quizzes_url, data={
        }, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.assertEqual(res.status_code, 200)

    def test_get_current_account_quizzes_no_authorization(self):
        self.client.post(
            self.register_url, self.register_data, format='json')
        access_token = self.client.post(
            self.login_url, self.login_data, format='json').data.get('access')

        res = self.client.get(self.current_account_quizzes_url)

        self.assertEqual(res.status_code, 401)

    def test_get_current_account_quizzes(self):
        self.client.post(
            self.register_url, self.register_data, format='json')
        access_token = self.client.post(
            self.login_url, self.login_data, format='json').data.get('access')

        res = self.client.get(self.current_account_quizzes_url, data={
        }, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.assertEqual(res.status_code, 200)

    def test_patch_account(self):
        self.client.post(
            self.register_url, self.register_data, format='json')
        access_token = self.client.post(
            self.login_url, self.login_data, format='json').data.get('access')

        res = self.client.patch(self.current_account_url, self.patch_data,
                                format='json', HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('username'), self.patch_data['username'])
        self.assertEqual(res.data.get('bio'), self.patch_data['bio'])
