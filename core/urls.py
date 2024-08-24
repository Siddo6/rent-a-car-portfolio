from django.urls import path
from .  import views

urlpatterns = [
    path ('', views.index, name='index'),
    path ('add-new', views.reservation_create, name='add_reservation'),
    path ('all_reservations', views.reservation_list, name='all_reservations'),
    path ('reservation_list/<int:current_month>/<int:current_year>/', views.reservation_list_current_month, name='reservation_list_current_month'),
    path ('cars', views.cars, name='cars'),
    path('reservation/<int:pk>/edit/', views.reservation_edit_view, name='reservation_edit'),
    path('reservation/<int:pk>/delete/', views.reservation_delete_view, name='reservation_delete'),
    path('reservation/<int:pk>/', views.reservation_detail_view, name='reservation_detail'),
    path('select_dates', views.available_cars, name='available_cars'),
    path('get_booked_dates/<int:car_id>', views.get_booked_dates, name='get_booked_dates'),
    path('daily_report', views.daily_report, name='daily_report'),
]
