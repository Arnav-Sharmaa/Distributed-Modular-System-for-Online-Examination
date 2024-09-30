from django.urls import path
from . import views

app_name = 'faculty'
urlpatterns = [
    path('', views.index, name='index'),
    path('exams', views.view_exams, name='view_exams'),
    path('exams/<int:exam_id>', views.view_exam, name='view_exam'),
    path('exams/<int:exam_id>/edit', views.edit_exam, name='edit_exam'),
    path('exams/<int:exam_id>/delete', views.delete_exam, name='delete_exam'),
    path('viewgroups', views.create_student_group, name='view_groups'),
    path('viewgroups/<int:group_id>', views.view_specific_group, name='view_specific_group'),
    path('viewgroups/<int:group_id>/students', views.view_student_in_group, name='view_students_in_group'),
    path('viewgroups/<int:group_id>/edit', views.edit_group, name='edit_group'),
    path('viewgroups/<int:group_id>/edit/delete', views.delete_group, name='delete_group'),
    path('questionpaper', views.make_paper ,name='make_paper') ,
    path('questionpaper/addquestion',views.add_question_in_paper, name="add_question_in_paper"),
    path('questionpaper/viewpaper',views.view_paper,name='view_paper'),
    path('questionpaper/editpaper',views.edit_paper,name='edit_paper'),
    path('questionpaper/viewpaper/<int:paper_id>', views.view_specific_paper, name='view_specific_paper'),
    path('question/view_all_ques/edit_question/<int:ques_qno>',views.edit_question,name="edit_question"),
    path('question', views.add_question, name='add_question'),
    path('question/view_all_ques', views.view_all_ques, name='view_all_ques'),
    path('students', views.view_students, name='view_students'),
]