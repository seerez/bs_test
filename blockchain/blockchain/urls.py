from django.contrib import admin
from django.urls import path

from transactions.views import index, tx, update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('update/', update, name='update'),
    path('tx/<str:txid>/', tx, name='tx_desc'),
]
