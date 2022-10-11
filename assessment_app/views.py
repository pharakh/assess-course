from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q

import sys, json

from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import *

def index(request):

    return render(request, "assessment_app/index.html")

def student(request):
    if not request.user.is_authenticated: return redirect(reverse('login_s'))
    try: student = Student.objects.get(user=request.user)
    except Student.DoesNotExist: return render(request, "assessment_app/errors.html", {
        "message": "کاربر غیرمجاز",
        "detail": "فقط دانشجویان می‌توانند از این صفحه بازدید کنند.",
        "nav": "برای بازگشت به صفحه اصلی از این <a href='/'>لینک</a> استفاده کنید."
    })

    active_term = Term.objects.get(active=True)
    active_courses = Course.objects.filter(student=student, term=active_term, student_not_answered=student)
    prizes = PrizeName.objects.filter(student=student, active=True).all()


    return render(request, "assessment_app/student.html", {
        "subjects": active_courses,
        "student": student,
        "prizes": prizes
    })

def teacher(request):
    if not request.user.is_authenticated: return redirect(reverse('login_t'))
    try: teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist: 
        return render(request, "assessment_app/errors.html", {
        "message": "کاربر غیرمجاز",
        "detail": "فقط مدرسین و کمک‌مدرسین می‌توانند از این صفحه بازدید کنند.",
        "nav": "برای بازگشت به صفحه اصلی از این <a href='/'>لینک</a> استفاده کنید."
    })

    active_term = Term.objects.get(active=True)
    active_courses = Course.objects.filter(Q(term=active_term), Q(teacher=teacher) | Q(current_supervisor=teacher))

    all_terms = Term.objects.all()

    supersvisors = teacher.supervisor.all()

    return render(request, "assessment_app/teacher.html", {
        "subjects": active_courses,
        "terms": all_terms,
        "supervisors": supersvisors
    })

# def university(request):

#     return render(request, "assessment_app/university.html")
















def getanswers(request, term_id):
    if not request.user.is_authenticated: 
        return JsonResponse({
            "error": "You should be logged in."
        }, status=401)

    try: teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist: 
        return JsonResponse({
            "error": "You should be a teacher."
        }, status=401)
    
    if request.method != "GET":
        return JsonResponse({
            "error": "Only GET required."
        }, status=400)

    term = Term.objects.get(pk=term_id)
    active_courses = Course.objects.filter(Q(term=term), Q(teacher=teacher) | Q(current_supervisor=teacher))
    results = []

    if teacher.supervisor.all().count() == 0: is_TA = False
    else: is_TA = True

    for course in active_courses:
        allanswers = []

        # Get all questions of this form
        allques = course.form_sample.question.all()
        # Get all answers of this form
        all_answers = FormAnswerS.objects.filter(form=course)

        for que in allques:

            # If the question type is open, get answers and add them to dictionary of allanswers
            if que.q_type.q_type == "OPEN":
                # Get this questions' answers negating empty answers
                cur_que_ans = all_answers.filter(Q(question=que.id), ~Q(answer_open=""))
                answers = []
                for ans in cur_que_ans:
                    ans = ans.answer_open
                    answers.append(ans)

                allanswers.append({"text": que.q_text, "type": "OPEN", "ans": answers.copy(), "id": que.id})

            # If the question type is closed, get ansers as dictionary of values and add it to dictionary of allanswers
            elif que.q_type.q_type == "CLOSE":
                # Get this questions' answers negating empty answers
                cur_que_ans = all_answers.filter(Q(question=que.id), ~Q(answer_closed=None))
                ans = {}
                for val in que.answer_closed_vals.values.all(): ans[val.value] = 0
                for val in cur_que_ans:
                    try: ans[val.answer_closed] += 1
                    except KeyError: pass

                allanswers.append({"text": que.q_text, "type": "CLOSE", "ans": ans.copy(), "id": que.id})

        results.append({
            "name": str(course.name),
            "isTA": course.is_teacher_assisstant,
            "nameTA": str(course.teacher),
            "id": course.id,
            "answered": course.student.all().count() - course.student_not_answered.all().count(),
            "q_a" : allanswers.copy()
            })


    return JsonResponse({
        "result": results,
        "isTA": is_TA
    }, status=200)


def purchase_prize(request, prize_id):
    if not request.user.is_authenticated: 
        return JsonResponse({
            "result": "You should be logged in."
        }, status=401)

    try: student = Student.objects.get(user=request.user)
    except Student.DoesNotExist: 
        return JsonResponse({
            "result": "You should be a student."
        }, status=401)
    
    if request.method != "POST":
        return JsonResponse({
            "result": "Only POST required."
        }, status=400)

    prize = PrizeName.objects.get(pk=prize_id)

    if prize.score_needed > student.score:
        return JsonResponse({
            "result": "You Don't have enough score."
        }, status=401)

    if PrizesGot.objects.filter(user=student, prize=prize).count() != 0:
        return JsonResponse({
            "result": "You have already bought this prize."
        }, status=401)

    new_log = PrizesGot(user=student, prize=prize)
    new_log.save()
    student.score -= prize.score_needed
    student.save()

    return JsonResponse({
        "result": "Successfuly saved the result."
    }, status=200)

def purchased_prizes(request, user_id):
    if not request.user.is_authenticated: 
        return JsonResponse({
            "result": "You should be logged in."
        }, status=401)

    if request.user.id != user_id: 
        return JsonResponse({
            "result": "You are not the owner if this id."
        }, status=401)
    
    if request.method != "GET":
        return JsonResponse({
            "result": "Only GET required."
        }, status=400)

    user = User.objects.get(pk=user_id)
    student = Student.objects.get(user=user)
    prizes = PrizesGot.objects.filter(user=student).all()
    
    return JsonResponse({
        "result": [{"name": prize.prize.name, "code": prize.code} for prize in prizes]
    }, status=200)














def formsbyteacher(request, subject):
    if not request.user.is_authenticated: return redirect(reverse('login_s'))

    if Student.objects.filter(user=request.user).count() == 0: 
        return render(request, "assessment_app/errors.html", {
            "message": "کاربر غیرمجاز",
            "detail": "فقط دانشجویان می‌توانند از این صفحه بازدید کنند.",
            "nav": "برای بازگشت به صفحه اصلی از این <a href='/'>لینک</a> استفاده کنید."
        })

    if request.method == "GET":
        try: form = Course.objects.get(id=subject)
        except: 
            return render(request, "assessment_app/errors.html", {
            "message": "صفحه یافت نشد",
            "detail": "احتمالا آدرس غلط وارد شده یا این فرم وجود ندارد.",
            "nav": "برای بازگشت به صفحه پروفایل از این <a href='/student'>لینک</a> استفاده کنید."
        })

        user = Student.objects.get(user=request.user)
            
        if form.student.filter(user=user.user).count() == 0: 
            return render(request, "assessment_app/errors.html", {
                "message": "کاربر غیرمجاز",
                "detail": "نام شما در لیست این درس وجود ندارد.",
                "nav": "برای بازگشت به صفحه پروفایل از این <a href='/student'>لینک</a> استفاده کنید."
            })


        if form.student_not_answered.filter(user=user.user).count() == 0: 
            return render(request, "assessment_app/errors.html", {
                "message": "کاربر غیرمجاز",
                "detail": "شما یکبار به این فرم پاسخ داده‌اید.",
                "nav": "برای بازگشت به صفحه پروفایل از این <a href='/student'>لینک</a> استفاده کنید."
            })


        return render(request, "assessment_app/form.html", {
            "form": form
        })
    else:
        data = request.POST
        form = Course.objects.get(id=data['form_id'])
        user = Student.objects.get(user=request.user)
        if form.student_not_answered.filter(user=user.user).count() == 0: 
            return render(request, "assessment_app/errors.html", {
                "message": "کاربر غیرمجاز",
                "detail": "شما یکبار به این فرم پاسخ داده‌اید.",
                "nav": "برای بازگشت به صفحه پروفایل از این <a href='/student'>لینک</a> استفاده کنید."
            })
        for value in data:
            if value in ['form_id', 'csrfmiddlewaretoken']: continue
            question = Questions.objects.get(pk=value)
            if question.q_type.q_type == "CLOSE":
                new_ans = FormAnswerS(user=user, form=form, question=question, answer_closed=data[value])
            elif question.q_type.q_type == "OPEN":
                new_ans = FormAnswerS(user=user, form=form, question=question, answer_open=data[value])
            new_ans.save()
            form.student_not_answered.remove(user)
        user.score += form.score
        user.save()

        return redirect(reverse('student'))




















def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def login_view_t(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("teacher"))
        else:
            return render(request, "assessment_app/login_t.html", {
                "message":  {
                    "text": "نام کاربری یا رمز عبور اشتباه است.",
                    "type": "danger"
                }})
    else:
        return render(request, "assessment_app/login_t.html")


def login_view_s(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("student"))
        else:
            return render(request, "assessment_app/login_s.html", {
                "message":  {
                    "text": "نام کاربری یا رمز عبور اشتباه است.",
                    "type": "danger"
                }})
    else:
        return render(request, "assessment_app/login_s.html")


def register_s(request):
    if request.method == "POST":
        data = request.POST

        # Ensure IDnumber is not taken
        try:
            idnum = IDNumbers.objects.get(idnum=data["username"])
            if idnum.taken:
                return render(request, "assessment_app/register_s.html", {
                    "message":  {
                        "text": "این شماره دانشجویی قبلا ثبت نام کرده.",
                        "type": "info"
                    }})
        except:
            return render(request, "assessment_app/register_s.html", {
                "message":  {
                    "text": "این شماره دانشجویی وجود ندارد.",
                    "type": "info"
                }})

        # Ensure password matches confirmation
        if data["password"] != data["confirmation"]:
            return render(request, "assessment_app/register_s.html", {
                "message":  {
                    "text": "رمزهای عبور یکسان نیست.",
                    "type": "danger"
                }})

        # Attempt to create new user
        try:
            user = User.objects.create_user(data["username"], 
                                            data["email"], 
                                            data["password"], 
                                            phonenumber=data["phonenumber"],
                                            first_name=data["first_name"],
                                            last_name=data["last_name"])
            user.save(); student = Student(user=user); student.save(); idnum.taken = True; idnum.save()
        except IntegrityError:
            return render(request, "assessment_app/register_s.html", {
                "message":  {
                    "text": "نام کاربری تکراری است.",
                    "type": "danger"
                }})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "assessment_app/register_s.html")



def register_t(request):
    if request.method == "POST":
        data = request.POST

        # Ensure password matches confirmation
        if data["password"] != data["confirmation"]:
            return render(request, "assessment_app/register_t.html", {
                "message":  {
                    "text": "رمزهای عبور یکسان نیست.",
                    "type": "danger"
                }})

        # Attempt to create new user
        try:
            user = User.objects.create_user(data["username"], 
                                            data["email"], 
                                            data["password"],
                                            first_name=data["first_name"],
                                            last_name=data["last_name"])
            user.save()
            teacher = Teacher(user=user)
            teacher.save()
        except IntegrityError:
            return render(request, "assessment_app/register_t.html", {
                "message":  {
                    "text": "نام کاربری تکراری است.",
                    "type": "danger"
                }})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "assessment_app/register_t.html")


def change_password(request):
    if not request.user.is_authenticated: 
        return JsonResponse({
            "result": "You should be logged in."
        }, status=401)

    if request.method != "POST":
        return JsonResponse({
            "result": "Only POST accepted."
        }, status=400)

    data = json.loads(request.body)

    user = authenticate(request, username=request.user, password=data["this_pass"])

    if user is not None:
        if data["new_pass"] != data["confirm"]: 
            return JsonResponse({
                "result": "Passwords are different."
            }, status=400)
        user.set_password(data["new_pass"])
        user.save()
        return JsonResponse({
                "result": "Password successfuly changed."
            }, status=200)
    else:
        return JsonResponse({
            "result": "Password is incorrect."
        }, status=401)