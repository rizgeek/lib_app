from django.urls import path
from books.api.views.books import Library, PublicLib

urlpatterns = [
    path('library/<str:action>', Library.as_view(), name='library books'),
    path('public/<str:action>', PublicLib.as_view(), name='public books'),
]
