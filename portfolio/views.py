from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'portfolio/home.html'


class AboutPageView(TemplateView):
    template_name = 'portfolio/about.html'