from django.conf.urls import url
from django.urls import path
from fasteat import views

# from fasteat.views import MenuView

urlpatterns = [
    url(r'^venuesgrid/$',views.venuesGrid,name='venuesgrid'),
    url(r'^venueslist/$',views.venuesList,name='venueslist'),

    url(r'^checkout/$',views.checkout,name='checkout'),
    url(r'^menu/$',views.menuView, name="menu"),
    # url(r'^menu/$',MenuView, name="menu"),
    url(r'^update_item/$',views.updateItem,name='update_item'),

    url(r'^entervenue/$',views.enterVenue,name='entervenue'),
    url(r'^confirm/$',views.orderConfirm,name='confirm'),

    url(r'^processOrder/$',views.processOrder,name='processOrder'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.loginPage,name='login'),
    url(r'^logout/$',views.logoutUser,name='logout'),

    url(r'^sbmVenue/$',views.sbmVenue,name='sbmVenue'),
    url(r'^home/$',views.index,name='home'),


    url(r'^resManagement/$',views.resMng,name='resMng'),
    url(r'^updataOrderStatus/$',views.updataOrderStatus,name='updataOrderStatus'),
    url(r'^historyOrder/$',views.historyOrder,name='historyOrder'),

]

app_name = 'fasteat'

