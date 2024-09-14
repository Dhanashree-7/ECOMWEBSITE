from django.urls import path
from coverapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('add',views.AddCover),
    path('',views.home),
    path('registration/',views.registerUser),
    path('login/',views.userLogin),
    path('logout/',views.userLogout),
    path('addtocart/<coverid>',views.addtocart),
    path('showcart/',views.showmycart),
    path('removecover/<cartid>',views.removeCart),
    path('updatecart/<opr>/<cartid>',views.updateCart),
    path('range',views.searchByrange),
    path('sort/<dir>',views.sortByprice),
    path('confirmorder/',views.confirmOrder),
    path('makepayment/',views.makepayment),
    path('placeorder/',views.placeOrder),
    path('aboutus/',views.AboutUs),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
