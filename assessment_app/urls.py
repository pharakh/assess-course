from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("student", views.student, name="student"),
    path("teacher", views.teacher, name="teacher"),
    # path("university", views.university, name="university"),

    path("logout", views.logout_view, name="logout"),
    path("teacher/login", views.login_view_t, name="login_t"),
    path("teacher/register", views.register_t, name="register_t"),
    path("student/login", views.login_view_s, name="login_s"),
    path("student/register", views.register_s, name="register_s"),

    path("forms/part/<str:subject>", views.formsbyteacher, name="forms_by_teacher"),

    # API route
    path("api/assess/<int:term_id>", views.getanswers, name="results_assess"),
    path("api/prizes_got/<int:user_id>", views.purchased_prizes, name="purchased_prizes"),
    path("api/buy_prize/<int:prize_id>", views.purchase_prize, name="purchase_prize"),


    path("api/change_password", views.change_password, name="change_password")
]
