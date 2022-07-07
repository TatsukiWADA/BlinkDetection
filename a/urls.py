from . import views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls.static import static
from django.urls import path

# from config import settings

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.index, name='index'),
    # path('video_feed', views.video_feed_view(), name="video_feed"),
]
# urlpatterns += staticfiles_urlpatterns()