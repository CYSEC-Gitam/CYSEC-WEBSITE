from django.urls import path
from certificate.views import *


urlpatterns = [
    path('verify/<str:verify_id>/', verify ,name="verify" ),
    path('delete/<int:id>/<slug:slug>', delete_event, name='delete_event'),
    path('view_certificate_status', view_certificate_status, name="view_certificate_status"),
    
    path('', create, name='certificate-home'),
    path('<int:id>/<slug:slug>', track, name='track'),
]