from django.urls import path
from .views import home, logout_view, show_image, evaluate_submissions, submission_details

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('image/', show_image, name='show_image'),
    path('avaliar/', evaluate_submissions, name='evaluate_submissions'),
    path('avaliar/submission_details/<int:lesson_file_id>/', submission_details, name='submission_details')
]
