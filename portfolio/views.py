from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django.forms.models import model_to_dict
from portfolio.models import Profile
from portfolio.forms import ProfileForm
from django.urls import reverse_lazy

class HomePageView(ListView):
    """
    Views for Home and User List, which shows other user's profile in full map.
    """
    template_name = 'portfolio/profile_list.html'
    model = Profile
    queryset = Profile.objects.all().prefetch_related('expertise','user')
    extra_context = dict()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_page'] = 'home' # variable to indicate which page the user is in

        return context


class ProfileView(DetailView):
    """
    Views for User Profile.
    """
    template_name = 'portfolio/profile.html'
    model = Profile
    extra_context = dict()

    def get_object(self, queryset=None):
        # get profile if profile exists, create profile if profile does not exist
        obj, created = self.model.objects.get_or_create(user=self.request.user, first_name=self.request.user.first_name,
                                                        last_name=self.request.user.last_name)
        return obj

    def get_context_data(self, **kwargs):
        # field that will be rendered using loop, so we don't have to render it manually
        self.extra_context['loop_fields'] = model_to_dict(self.get_object(),
                                                          exclude=('id', 'user', 'first_name', 'last_name'))

        # other field that will be rendered without using loop
        self.extra_context['profile'] = model_to_dict(self.get_object(), fields=('first_name', 'last_name',
                                                                                 'expertise', 'location', 'photo'))

        self.extra_context['menu_page'] = 'profile' # variable to indicate which page the user is in

        return super().get_context_data(**kwargs)

class ProfileEditView(UpdateView):
    """
    Views for User Profile Edit
    """
    template_name = 'portfolio/profile_edit.html'
    extra_context = dict()
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        obj = self.form_class.Meta.model.objects.get(user=self.request.user)
        return obj
