from django.urls import resolve, reverse_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory
from portfolio.admin import ProfileAdmin
from portfolio.models import Profile
from users.models import LogEntry


def setup_test_data(cls):
    # user that is created from signup process
    cls.credentials = {
        'email': 'testuser1@gmail.com',
        'username': 'testuser1',
        'password': 'secret'}
    cls.email = cls.credentials['email']
    cls.username = cls.credentials['username']
    cls.password = cls.credentials['password']
    # Create user that mimics signed-up user
    cls.user = get_user_model().objects.create_user(username=cls.username, email=cls.email,
                                                    password=cls.password, is_staff=True)
    cls.profile = Profile.objects.create(user=cls.user, first_name=cls.user.first_name,
                                         last_name=cls.user.last_name)

    # user with superuser status
    cls.credentials2 = {
        'email': 'testuser2@gmail.com',
        'username': 'testuser2',
        'password': 'secret'}
    cls.email2 = cls.credentials2['email']
    cls.username2 = cls.credentials2['username']
    cls.password2 = cls.credentials2['password']
    # Create user that mimics signed-up user
    cls.user2 = get_user_model().objects.create_user(username=cls.username2, email=cls.email2,
                                                     password=cls.password2, is_superuser=True)
    cls.profile2 = Profile.objects.create(user=cls.user2, first_name=cls.user2.first_name,
                                          last_name=cls.user2.last_name)

class CustomUsertest(TestCase):
    """
    TestCase for CustomUser
    """

    @classmethod
    def setUpTestData(cls):
        """
        Before TestCase is run, set some data
        """
        setup_test_data(cls)

    def login(self):
        """
        Method for login
        """
        self.client.login(email=self.email, password=self.password)
        self.response = self.client.get('/admin', follow=True)

    def test_default_permission(self):
        """
        Signed-up User should only have `portfolio.change_profile` permission
        """
        self.assertEquals(True, self.user.has_perm('portfolio.change_profile'))
        self.assertEquals(1, self.user.user_permissions.all().count())

    def test_staff_status(self):
        """
        Signed-up User should have staff status
        """
        self.assertEquals(self.user.is_staff, True)

    def test_user_is_superuser(self):
        """
        Signed-up User should not have superuser status
        """
        self.assertEquals(self.user.is_superuser, False)

    def test_superuser_is_superuser(self):
        """
        Signed-up User should not have superuser status
        """
        self.assertEquals(self.user.is_superuser, False)

    def test_user_login_admin(self):
        """
        Signed-up User should be able to login to admin page (indicated as having change admin password)
        """
        self.login()
        self.assertContains(self.response, 'href="/admin/password_change/"')

    def test_user_open_user_model(self):
        """
        Signed-up User should not be able to open User model in admin
        """
        self.login()
        response = self.client.get('/admin/users/customuser/', follow=True)
        self.assertEquals(response.status_code, 403)

    def test_superuser_open_user_model(self):
        """
        Signed-up User should not be able to open User model in admin
        """
        self.client.login(email=self.email2, password=self.password2)
        response = self.client.get('/admin/users/customuser/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_user_can_only_access_associated_profile(self):
        """
        Signed-up User can only access his/her profile. We have 2 profiles, so that means
        the number of profile returned by admin should be 1 instead of 2 and
        the Signed-up User is associated to that profile
        """
        self.request_factory = RequestFactory()
        request = self.request_factory.get('/admin/profile')
        request.user = self.user
        profile_admin = ProfileAdmin(Profile, AdminSite())
        qs = profile_admin.get_queryset(request)
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs.first().user, self.user)

    def test_superuser_can_access_all_profile(self):
        """
        Superuser can access all profile. We have 2 profiles, so that means
        the number of profile returned by admin should be 2
        """
        self.request_factory = RequestFactory()
        request = self.request_factory.get('/admin/profile')
        request.user = self.user2
        profile_admin = ProfileAdmin(Profile, AdminSite())
        qs = profile_admin.get_queryset(request)
        self.assertEquals(qs.count(), 2)

class LogEntryTest(TestCase):
    """
    TestCase for LogEntry
    """

    @classmethod
    def setUpTestData(cls):
        setup_test_data(cls)

    def test_user_successfull_login(self):
        """
        After successfull login, LogEntry should have object with value
        action=user_logged_in, email=testuser1@gmail.com
        """
        self.client.login(email=self.email, password=self.password)
        self.response = self.client.get(_('home'), follow=True)
        # LogEntry is sorted descending by id, so last created entry will be in the first position
        log = LogEntry.objects.all().first()

        self.assertEquals(log.action, 'user_logged_in')
        self.assertEquals(log.email, self.email)

    def test_user2_successfull_login(self):
        """
        After successfull login, LogEntry should have object with value
        action=user_logged_in, email=testuser2@gmail.com
        """
        self.client.login(email=self.email2, password=self.password2)
        self.response = self.client.get(_('home'), follow=True)
        # LogEntry is sorted descending by id, so last created entry will be in the first position
        log = LogEntry.objects.all().first()

        self.assertEquals(log.action, 'user_logged_in')
        self.assertEquals(log.email, self.email2)

    def test_user_successfull_logout(self):
        """
        After successfull logout, LogEntry should have object with value
        action=user_logged_in, email=testuser1@gmail.com
        """
        self.client.login(email=self.email, password=self.password)
        self.client.logout()
        self.response = self.client.get(_('home'), follow=True)
        # LogEntry is sorted descending by id, so last created entry will be in the first position
        log = LogEntry.objects.all().first()

        self.assertEquals(log.action, 'user_logged_out')
        self.assertEquals(log.email, self.email)

    def test_user2_successfull_logout(self):
        """
        After successfull logout, LogEntry should have object with value
        action=user_logged_in, ip=user_logged_in, email=testuser1@gmail.com
        """
        self.client.login(email=self.email2, password=self.password2)
        self.client.logout()
        self.response = self.client.get(_('home'), follow=True)
        # LogEntry is sorted descending by id, so last created entry will be in the first position
        log = LogEntry.objects.all().first()

        self.assertEquals(log.action, 'user_logged_out')
        self.assertEquals(log.email, self.email2)