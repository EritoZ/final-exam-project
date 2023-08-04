from django.urls import path, include

from apps.accounts import views

urlpatterns = [
    path('create', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('<slug:slug>/', include([
        path('', views.ProfileDetailsView.as_view(), name='profile details'),
        path('edit', views.ProfileEditView.as_view(), name='profile edit'),
        path('change_password', views.ProfileChangePasswordView.as_view(), name='change password'),
        path('success', views.PasswordChangeSuccessView.as_view(), name='password change success'),
    ])),

]