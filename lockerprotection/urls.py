from django.contrib import admin
from django.urls import path
from authentication import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboardPage,name="dashboard"),
    path('viewData/',views.viewDataPage, name="viewdata"),
    path('register/',views.registerPage, name="register"),
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutPage, name="logout"),
    path('deleteData/<int:dataId>/',views.deleteDataPage, name="deleteData"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)