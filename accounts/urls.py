from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'login/$', views.sign_in, name='sign_in'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'sign_out/$', views.sign_out, name='sign_out'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'profile/change_password/$', views.change_password,
        name="change_password"),
    url(r'profile/edit_avatar/$', views.edit_avatar,
        name="edit_avatar"),
    url(r'profile/edit_avatar/crop/', views.edit_avatar_crop,
        name="edit_avatar_crop"),
    url(r'profile/edit_avatar/rotate/$', views.edit_avatar_rotate,
        name="edit_avatar_rotate"),
    url(r'profile/edit_avatar/flip/$', views.edit_avatar_flip,
        name="edit_avatar_flip"),
]
