from django.urls import resolve, reverse_lazy as _
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from portfolio.views import HomePageView
from portfolio.forms import ProfileForm
from portfolio.models import Profile
from io import BytesIO
import base64 # for testing image upload
import tempfile # set tempdir for media

class HomeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Before TestCase is run, set some data
        """
        cls.credentials = {
            'email': 'testuser1@gmail.com',
            'username': 'testuser1',
            'password': 'secret'}
        cls.username = cls.credentials['email']
        cls.email = cls.credentials['username']
        cls.password = cls.credentials['password']
        cls.user = get_user_model().objects.create_user(username=cls.username, email=cls.email,
                                                        password=cls.password)

    def login(self):
        """
        Method for login
        """
        self.client.login(email=self.email, password=self.password)
        self.response = self.client.get(_('home'), follow=True)

    def test_home_view_status_code(self):
        """
        Test user can open home without login
        """
        url = _('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """
        Test url '/' points to HomePageView
        """
        view = resolve('/')
        self.assertEquals(view.func.__name__, HomePageView.as_view().__name__)

    def test_login(self):
        """
        Test user login
        """
        self.login()
        self.assertEqual(str(self.response.context['user']), 'testuser1')

    def test_home_view_contains_link_profile_view_after_login(self):
        """
        After login, home should display a link to profile
        """
        self.login()
        profile_view_url = _('profile')
        self.assertContains(self.response, 'href="{}"'.format(profile_view_url))

    def test_home_view_not_contains_link_profile_view_before_login(self):
        """
        Before login, home should not display a link to profile
        """
        profile_view_url = _('profile')
        self.response = self.client.get(_('home'), follow=True)
        self.assertNotContains(self.response, 'href="{}"'.format(profile_view_url))


class ProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Before TestCase is run, set some data
        """
        cls.credentials = {
            'email': 'testuser1@gmail.com',
            'username': 'testuser1',
            'password': 'secret'}
        cls.username = cls.credentials['email']
        cls.email = cls.credentials['username']
        cls.password = cls.credentials['password']
        cls.user = get_user_model().objects.create_user(username=cls.username, email=cls.email,
                                                        password=cls.password)

    def login(self):
        """
        Method for login
        """
        self.client.login(email=self.email, password=self.password)
        self.response = self.client.get(_('profile'), follow=True)

    def test_profile_view_unauthenticated_redirected(self):
        """
        ProfileView will redirect unauthenticated user to login page
        """
        response = self.client.get(_('profile'), follow=True)
        self.assertRedirects(response, _('account_login') + '?next=/profile', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=False)

    def test_profile_view_after_login_success_status_code(self):
        """
        ProfileView renders page successfully for authenticated user
        """
        self.login()
        self.assertEquals(self.response.status_code, 200)

    def test_profile_object_created_after_access_profile_view(self):
        """
        After login for the first time and open profile page, Profile will be automatically created
        """
        self.login()
        self.assertEquals(1,Profile.objects.filter(user=self.user).count())


class ProfileEditTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'email': 'testuser1@gmail.com',
            'username': 'testuser1',
            'password': 'secret'}
        cls.username = cls.credentials['email']
        cls.email = cls.credentials['username']
        cls.password = cls.credentials['password']
        cls.user = get_user_model().objects.create_user(username=cls.username, email=cls.email,
                                                        password=cls.password)
        cls.profile = Profile.objects.create(user=cls.user)
        cls.photo = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),  # use io.BytesIO
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )

        cls.data = {
            'first_name': 'Budi',
            'last_name': 'Istiadi',
            'address': 'Purworejo',
        }

        cls.invalid_data = {
            'first_name': 'Budi',
            'last_name': 'Istiadi',
            'address': 'Purworejo',
            'phone': 'ckjsbffbkw',
        }

    def login(self):
        """
        Method for login
        """
        self.client.login(email=self.email, password=self.password)
        self.response = self.client.get(_('profile_edit'), follow=True)

    def test_csrf(self):
        """
        Test if page contains CSRF token
        """
        self.login()
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_profile_view_before_login_redirected(self):
        """
        ProfileEditView will redirect unauthenticated user to login page
        """
        response = self.client.get(_('profile_edit'), follow=True)
        self.assertRedirects(response, _('account_login') + '?next=/profile/edit', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=False)

    def test_contains_form(self):
        """
        Profile edit page must contain ProfileForm
        """
        self.login()
        form = self.response.context.get('form')
        self.assertIsInstance(form, ProfileForm)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())  # override settings for media dir to avoid consuming our disk
    def test_profile_form_valid_post_data(self):
        """
        Using valid data, test if form is valid
        """
        self.form = ProfileForm(files={'photo': self.photo}, data=self.data, instance=self.profile)
        self.assertEqual(self.form.is_valid(), True)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())  # override settings for media dir to avoid consuming our disk
    def test_save_profile_valid_post_data_update(self):
        """
        Using valid data, test if Profile can be updated
        """
        self.form = ProfileForm(files={'photo': self.photo}, data=self.data, instance=self.profile)
        self.form.save()
        self.assertEquals('Budi', self.profile.first_name)
        self.assertEquals('Istiadi', self.profile.last_name)
        self.assertEquals('Purworejo', self.profile.address)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())  # override settings for media dir to avoid consuming our disk
    def test_profile_form_invalid_post_data(self):
        """
        Using valid data, test if form is valid
        """
        self.form = ProfileForm(files={'photo': self.photo}, data=self.invalid_data, instance=self.profile)
        self.assertEqual(self.form.is_valid(), False)


TEST_IMAGE = '''
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
'''.strip()