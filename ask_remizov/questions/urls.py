from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from ask_remizov import settings

urlpatterns = [
    url(r'^$', views.new_questions_view, name='base'),
    url(r'^q/(?P<question_id>[0-9]+)$', views.answers_view, name='answers'),
    url(r'^tag/(?P<tag_id>[0-9]+)$', views.tag_view, name='questions_by_tag'),
    url(r'^signup$', views.signup_view, name='signup'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^ask$', views.ask_view, name='ask'),
    url(r'^profile/edit$', views.settings_view, name='settings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
