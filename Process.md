# Creating the virtual environment

```md
python -m venv ./"Locker Protection"
cd "Locker Protection"/scripts
activate
```

# Creating the Project

```md
pip install django
django-admin startproject lockerprotection
cd lockerprotection
```

# Creating the app (for authentication)

*Installation Command*
```md
python manage.py startapp authentication
```

*INSTALLED_APPS*
```md
'authentication',
```

*working*
## Inner Project Folder (lockerprotection)

*urls.py*
```md
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
```

*settings.py*
```md
LOGIN_URL = 'login'
```

## Authentication (app)

*views.py*
```md
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .forms import FileUploadForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@login_required
@csrf_protect
def dashboardPage(request):
    user = request.user
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fileName = form.cleaned_data.get('fileName')
            description = form.cleaned_data.get('description')
            fileUpload = form.cleaned_data.get('fileUpload')
            if fileUpload:
                models.Data.objects.create(user=user, fileName=fileName, description=description, fileUpload=fileUpload)
            else:
                models.Data.objects.create(user=user, fileName=fileName, description=description)
            return redirect('dashboard')
    else:
        form = FileUploadForm()
    return render(request, 'dashboard.html', {'form': form, 'user': user})

@login_required
@csrf_protect
def viewDataPage(request):
    user = request.user
    user_data = models.Data.objects.filter(user=request.user)
    return render(request, 'viewData.html', {'username': user, 'user_data': user_data})

@login_required
@csrf_protect    
def deleteDataPage(request, dataId):
    data = get_object_or_404(models.Data, id=dataId, user=request.user)
    data.delete()
    return redirect('viewdata')

@csrf_protect
def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if password != repassword:
            return redirect('register')
        if User.objects.filter(username=username).exists():
            return redirect('register')
        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
        except Exception as e:
            return redirect('register')
    return render(request, 'register.html')

@csrf_protect
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
@csrf_protect
def logoutPage(request):
    logout(request)
    return redirect('login')
```

*forms.py*
```md
from django import forms
from .models import Data
import os

class FileUploadForm(forms.Form):
    fileName = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    fileUpload = forms.FileField(required=False)

    def clean_fileUpload(self):
        file = self.cleaned_data.get('fileUpload', False)
        if file:
            ext = os.path.splitext(file.name)[1]
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt']
            if not ext.lower() in valid_extensions:
                raise forms.ValidationError('Unsupported file extension.')
            if file.size > 1024*1024:
                raise forms.ValidationError('File size too large. The maximum file size allowed is 1MB.')
        return file
```

*models.py*
```md
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Data(models.Model):
    # id = models.AutoField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    fileName = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    fileUpload = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.fileName
```

*admin.py*
```md
from django.contrib import admin
from .models import Data

class AdminData(admin.ModelAdmin):
    list_display = ('user', 'fileName', 'description', 'fileUpload')
    search_fields = ('user', 'fileName', 'description')
    list_filter = ('user', 'fileName', 'description')

admin.site.register(Data, AdminData)
```


# Templates

*Folder*
```md
mkdir templates
```

*TEMPLATES*
```md
'DIRS': [os.path.join(BASE_DIR,'templates')],
```

# Static 

*Folder*
```md
mkdir static
```

*Additional*
```md
import os
```

*Additional*
```md
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
```

## For Production
*urls.py*
```md
from django.conf import settings
from django.conf.urls.static import static
```

## For Production
*urls.py*
```md
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

# Whitenoise (for static files)

## For Production
*Installation Command*
```md
pip install whitenoise
```

*Additional*
```md
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

*Middlewares*
```md
'whitenoise.middleware.WhiteNoiseMiddleware',
```

# Media

*Folder*
```md
mkdir media
```

*Additional*
```md
import os
```

*Additional*
```md
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## For Production
*urls.py*
```md
from django.conf import settings
from django.conf.urls.static import static
```

## For Production
*urls.py*
```md
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

# DOTENV

*Installation command*
```md
pip install python-dotenv
```

*Additional*
```md
import os
from dotenv import load_dotenv
load_dotenv()
```

*Usage*
```md
os.environ.get("Name")
```

# DEPLOYMENT

*render*

*Production Installation*
```md
pip install gunicorn
```

*Production Modules*
```md
pip freeze > requirements.txt
```

*Production Command*
```md
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

*Postgresql Database*
**Installation**
```md
pip install dj-database-url psycopg2-binary
```

```md
import dj_database_url
```

```md
DATABASES = {
        'default': dj_database_url.parse('POSTGRESQLDBURL')
}
```