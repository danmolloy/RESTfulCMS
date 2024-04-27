from django.urls import path, include

from . import views

urlpatterns = [
    path('api/<str:username>/', views.restful_api),
    path("accounts/", include("django.contrib.auth.urls")),
    path('signup/', views.signup, name='signup'),
    path("create/", views.CreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.UpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.DeleteView.as_view(), name="delete"),
    path("posts/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("", views.IndexView.as_view(), name="index"),
]
