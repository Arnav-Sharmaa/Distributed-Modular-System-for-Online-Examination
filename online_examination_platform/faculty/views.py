from django.shortcuts import render, redirect
from exam.models import *
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


def index(request):
    prof = request.user
    return render(request, 'faculty/index.html', {'prof': prof })

def view_exams(request):
    prof = request.user

    new_Form = ExamForm()
    new_Form.fields["student_group"].queryset = Special_Students.objects.filter(
        professor=prof)
    new_Form.fields["question_paper"].queryset = Question_Paper.objects.filter(
        professor=prof)

    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.professor = prof
            exam.save()
            form.save_m2m()
            return redirect('faculty:view_exams')

    exams = Exam_Model.objects.filter(professor=prof)

    return render(request, 'faculty/exam/view_exams.html', {
        'exams': exams, 'examform': new_Form, 'prof': prof,
    })
    

def view_exam(request, exam_id):
    prof = request.user
    exam = Exam_Model.objects.get(professor=prof, pk=exam_id)
    return render(request, 'faculty/exam/view_exam.html', {
        'exam': exam, 'prof': prof, 'student_group': exam.student_group.all()
    })
    

def edit_exam(request, exam_id):
    prof = request.user
    exam = Exam_Model.objects.filter(professor=prof, pk=exam_id).first()
    
    new_Form = ExamForm(instance=exam)
    new_Form.fields["student_group"].queryset = Special_Students.objects.filter(professor=prof)
    new_Form.fields["question_paper"].queryset = Question_Paper.objects.filter(professor=prof)

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('faculty:view_exams')

    return render(request, 'faculty/exam/edit_exam.html', {
        'form': new_Form, 'exam': exam, 'prof': prof
    })
    

def delete_exam(request, exam_id):
    prof = request.user
    exam = Exam_Model.objects.get(professor=prof, pk=exam_id)
    exam.delete()
    return redirect('faculty:view_exams')


def create_student_group(request):
    prof = request.user

    if request.method == "POST":
        form = Group_Form(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.professor = prof
            group.save()
            form.save_m2m()
            
            return redirect('faculty:view_groups')

    return render(request, 'faculty/group/addview_groups.html', {
        'special_students_db': Special_Students.objects.filter(professor=prof), 'prof': prof, 'groupForm': Group_Form()
    })
    

def view_specific_group(request, group_id):
    prof = request.user
    group = Special_Students.objects.get(professor=prof, pk=group_id)

    return render(request, 'faculty/group/view_specific_group.html', {
        'group': group, 'prof': prof, 'group_students': group.students.all()
    })
    

def view_student_in_group(request, group_id):
    prof = request.user
    group = Special_Students.objects.get(professor=prof, pk=group_id)

    if request.method == 'POST':
        student_username = request.POST['username']
        student = User.objects.get(username=student_username)
        group.students.add(student)

    return render(request, 'faculty/group/view_special_stud.html', {
        'students': group.students.all(), 'group': group, 'prof': prof
    })
    

def edit_group(request, group_id):
    prof = request.user 
    group = Special_Students.objects.get(professor=prof, pk=group_id)
    group_form = Group_Form(instance=group)
    
    if request.method == "POST":
        form = Group_Form(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('faculty:view_groups')

    return render(request, 'faculty/group/edit_group.html', {
        'prof':prof, 'group':group, 'group_form': group_form
    })
    

def delete_group(request, group_id):
    prof = request.user
    Special_Students.objects.filter(professor=prof, pk=group_id).delete()
    return redirect('faculty:view_groups')



def make_paper(request):
    prof = request.user

    if request.method == 'POST' and not request.POST.get('presence', False):
        add_question_in_paper(request)

    elif request.method == 'POST' and request.POST.get('presence', False):
        title = request.POST['title']
        Question_Paper.objects.filter(professor=prof, qPaperTitle=title).first().delete()

    return render(request, 'faculty/question_paper/qpaper.html', {
        'qpaper_db': Question_Paper.objects.filter(professor=prof), 'prof': prof
    })



def add_question_in_paper(request):
    prof = request.user

    if request.method == 'POST' and request.POST.get('qpaper', False):
        paper_title = request.POST['qpaper']
        question_paper = Question_Paper(professor=prof, qPaperTitle=paper_title)
        question_paper.save()

        left_ques = []
        curr_paper_questions = question_paper.questions.all()
        for ques in Question_DB.objects.filter(professor=prof):
            if ques not in curr_paper_questions:
                left_ques.append(ques)

        return render(request, 'faculty/question_paper/addquestopaper.html', {
            'qpaper': question_paper,
            'question_list': left_ques, 'prof': prof
        })

    elif request.method == 'POST' and request.POST.get('title', False):
        addques = request.POST['title']
        ques_ = Question_DB.objects.filter(professor=prof, qno=addques).first()
        title = request.POST['papertitle']
        ques_paper = Question_Paper.objects.filter(professor=prof, qPaperTitle=title).first()
        ques_paper.questions.add(ques_)
        ques_paper.save()

        left_ques = []
        curr_paper_questions = ques_paper.questions.all()
        for ques in Question_DB.objects.filter(professor=prof):
            if ques not in curr_paper_questions:
                left_ques.append(ques)

        return render(request, 'faculty/question_paper/addquestopaper.html', {
            'qpaper': ques_paper, 'question_list': left_ques, 'prof': prof
        })

    return render(request, 'faculty/question_paper/addquestopaper.html')



def view_paper(request):
    prof = request.user

    if request.method == 'POST':
        papertitle = request.POST['title']
        ques_paper = Question_Paper.objects.get(professor=prof, qPaperTitle=papertitle)

        return render(request, 'faculty/question_paper/viewpaper.html', {
            'qpaper': ques_paper, 'question_list': ques_paper.questions.all(), 'prof': prof
        })



def edit_paper(request):
    prof = request.user

    if request.method == 'POST' and request.POST.get('title', False):
        papertitle = request.POST['title']
        ques_paper = Question_Paper.objects.filter(professor=prof, qPaperTitle=papertitle).first()

        left_ques = []
        curr_paper_questions = ques_paper.questions.all()
        for ques in Question_DB.objects.filter(professor=prof):
            if ques not in curr_paper_questions:
                left_ques.append(ques)

        return render(request, 'faculty/question_paper/editpaper.html', {
            'ques_left': left_ques, 'qpaper': ques_paper, 'question_list': ques_paper.questions.all(), 'prof': prof
        })

    elif request.method == 'POST' and request.POST.get('remove', False):
        papertitle = request.POST['paper']
        no = request.POST['question']
        ques_paper = Question_Paper.objects.filter(professor=prof, qPaperTitle=papertitle).first()
        ques = Question_DB.objects.filter(professor=prof, qno=no).first()
        ques_paper.questions.remove(ques)
        ques_paper.save()

        left_ques = []
        curr_paper_questions = ques_paper.questions.all()
        for ques in Question_DB.objects.filter(professor=prof):
            if ques not in curr_paper_questions:
                left_ques.append(ques)

        return render(request, 'faculty/question_paper/editpaper.html', {
            'ques_left': left_ques, 'qpaper': ques_paper, 'question_list': ques_paper.questions.all(), 'prof': prof
        })

    elif request.method == 'POST' and request.POST.get('qnumber', False) != False:
        qno = request.POST['qnumber']
        ptitle = request.POST['titlepaper']
        ques_paper = Question_Paper.objects.filter(
            professor=prof, qPaperTitle=ptitle).first()
        a = Question_DB.objects.filter(professor=prof, qno=qno).first()
        ques_paper.questions.add(a)
        ques_paper.save()

        left_ques = []
        curr_paper_questions = ques_paper.questions.all()
        for ques in Question_DB.objects.filter(professor=prof):
            if ques not in curr_paper_questions:
                left_ques.append(ques)

        return render(request, 'faculty/question_paper/editpaper.html', {
            'ques_left': left_ques, 'qpaper': ques_paper, 'question_list': ques_paper.questions.all(), 'prof': prof
        })
            


def view_specific_paper(request, paper_id):
    prof = request.user

    paper = Question_Paper.objects.get(professor=prof, pk=paper_id)
    return render(request, 'faculty/question_paper/viewpaper.html', {
        'qpaper': paper, 'question_list': paper.questions.all(), 'prof': prof
    })

def add_question(request):
    prof = request.user

    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.professor = prof
            form.save()
            return redirect('faculty:view_all_ques')

    return render(request, 'faculty/question/question.html', {
        'question_db': Question_DB.objects.filter(professor=prof), 'form': QForm(), 'prof': prof
    })

   
def view_all_ques(request):
    prof = request.user

    if request.method == 'POST':
        Q_No = int(request.POST['qno'])
        sum_ = 1 + Question_DB.objects.filter(professor=prof).count()

        for i in range(Q_No+1, sum_):
            ques = Question_DB.objects.filter(
                professor=prof, qno=int(i)).first()
            ques.qno -= 1
            ques.save()

        sum_ -= 1

        Question_DB.objects.filter(professor=prof, qno=Q_No).delete()

    return render(request, 'faculty/question/view_all_questions.html', {
        'question_db': Question_DB.objects.filter(professor=prof), 'prof': prof
    })

    
def edit_question(request, ques_qno):
    prof = request.user
    ques = Question_DB.objects.get(professor=prof, qno=ques_qno)
    form = QForm(instance=ques)

    if request.method == "POST":
        form = QForm(request.POST, instance=ques)
        if form.is_valid():
            form.save()
            return redirect('faculty:view_all_ques')

    return render(request, 'faculty/question/edit_question.html', {
        'i': Question_DB.objects.filter(professor=prof, qno=ques_qno).first(), 'form': form, 'prof': prof
    })

def view_students(request):
    prof = request.user
    return render(request, 'faculty/student/view_students.html', {
        'students': User.objects.filter(groups__name='Student'), 'prof': prof
    })






