from django.urls import path


from library import views

app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<slug:slug>', views.author, name="author"),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
]