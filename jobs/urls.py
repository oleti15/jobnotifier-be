from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import SubscriberCreateView
from .views import JobListCreateView


urlpatterns = [
    path('api/jobs/', views.job_list_api, name='job_list_api'),
    path('api/jobs/<int:job_id>/', views.job_detail_api, name='job_detail_api'),
    path('subscribe/', SubscriberCreateView.as_view(), name='subscribe'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('api/jobs/', JobListCreateView.as_view(), name='job-list-create'),
]
