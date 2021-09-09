
from django.urls import path
from .views import get_custom_user_list, get_by_id

urlpatterns = [
    path('accounts/',get_custom_user_list , name = 'account_list' ),
    path('accounts/<int:id>/', get_by_id )
]