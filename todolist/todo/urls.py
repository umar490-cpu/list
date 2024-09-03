from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path('delete/<pk>/', views.delete_todo, name='delete_todo'),
    path('tasks/create/', views.create_and_list_todo, name='create_and_list_todo'),
    path('tasks/<pk>/update/', views.edit_todo, name='edit_todo'),
    path("finish/<id>",views.finish,name="finish"),
    path('tasks/', views.finding, name='finding_all'),
    path('tasks/<str:status>/', views.finding, name='finding_status'),
    path('signout/', views.signout, name='signout'),
    
]
