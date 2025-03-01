from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerUser,name='register'),
    path('logout/',views.logoutUser,name='logout'),
    path('',views.home,name="home"),
    path('room/<str:pk>',views.room,name="room"),
    path('profile/<str:pk>',views.userProfile,name='profile'),
    path('createroom/',views.createRoom,name='create-room'),
    path('updateroom/<str:pk>',views.updateRoom,name='update-room'),
    path('deleteroom/<str:pk>',views.deleteRoom,name='delete-room'),
    path('deleteMessage/<str:pk>',views.deleteMessage,name='delete-message'),

]