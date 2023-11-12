from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('question/<int:question_id>', views.question, name="question"),
    path('hot', views.hot, name="hot"),
    path('tag/<tag_name>', views.tag, name="tag"),
    path('ask', views.ask, name="ask"),
    path('login', views.login, name="login"),
    path('singup', views.register, name="register"),
    path('settings', views.settings, name="settings")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)