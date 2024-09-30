from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from exam.models import *
from django.contrib.auth.models import User
from students.models import *
from django.utils import timezone


def index(request):
    student = request.user

    studentGroup = Special_Students.objects.filter(students=student)
    examsList = []
    if studentGroup.exists():
        for student_ in studentGroup:
            stud_exams = Exam_Model.objects.filter(student_group=student_)
            if stud_exams.exists():
                if stud_exams.count() > 1:
                    for stud_exam in stud_exams:
                        examsList.append(stud_exam)
                else:
                    examsList.append(Exam_Model.objects.get(
                        student_group=student_))

    if examsList:
        for exam in examsList:
            currentExamList = StuExam_DB.objects.filter(
                examname=exam.name, student=student)

            if not currentExamList.exists():  # If no exam are there in then add exams
                tempExam = StuExam_DB(student=student, examname=exam.name,
                                        qpaper=exam.question_paper, score=0, completed=0)
                tempExam.save()
                exam_question_paper = exam.question_paper
                questions_in_paper = exam_question_paper.questions.all()
                
                for ques in questions_in_paper:
                    # add all the questions from the prof to student database
                    studentQuestion = Stu_Question(question=ques.question, optionA=ques.optionA, optionB=ques.optionB,
                                                    optionC=ques.optionC, optionD=ques.optionD,
                                                    answer=ques.answer, student=student)
                    studentQuestion.save()
                    tempExam.questions.add(studentQuestion)

    return render(request, 'students/index.html', {
        'stud': student
    })

def exams(request):
    student = request.user

    studentGroup = Special_Students.objects.filter(students=student)
    studentExamsList = StuExam_DB.objects.filter(student=student)

    if request.method == 'POST' and not request.POST.get('papertitle', False):
        paper = request.POST['paper']
        stuExam = StuExam_DB.objects.get(examname=paper, student=student)
        qPaper = stuExam.qpaper
        examMain = Exam_Model.objects.get(name=paper)

        # TIME COMPARISON
        exam_start_time = examMain.start_time
        curr_time = timezone.now()
        print("examTime_time",exam_start_time)
        print("currentTime",curr_time)
        if curr_time < exam_start_time:
            return redirect('students:exams')

        stuExam.questions.all().delete()

        qPaperQuestionsList = qPaper.questions.all()
        for ques in qPaperQuestionsList:
            student_question = Stu_Question(question=ques.question, optionA=ques.optionA, optionB=ques.optionB,
                                            optionC=ques.optionC, optionD=ques.optionD,
                                            answer=ques.answer, student=student)
            student_question.save()
            stuExam.questions.add(student_question)
            stuExam.save()

        stuExam.completed = 1
        stuExam.save()
        mins = examMain.duration
        secs = 0

        return render(request, 'students/paper/viewpaper.html', {
            'qpaper': qPaper, 'question_list': stuExam.questions.all(), 'student': student, 'exam': paper, 'min': mins, 'sec': secs
        })

    elif request.method == 'POST' and request.POST.get('papertitle', False):
        paper = request.POST['paper']
        title = request.POST['papertitle']
        stuExam = StuExam_DB.objects.get(examname=paper, student=student)
        qPaper = stuExam.qpaper

        examQuestionsList = stuExam.questions.all()
        examScore = 0
        for ques in examQuestionsList:
            ans = request.POST.get(ques.question, False)
            if not ans:
                ans = "E"
            ques.choice = ans
            ques.save()
            if ans == ques.answer:
                examScore = examScore + 1

        stuExam.score = examScore
        stuExam.save()

        return render(request, 'students/result/result.html', {
            'Title': title, 'Score': examScore, 'student': student
        })

    return render(request, 'students/exam/viewexam.html', {
        'student': student, 'paper': studentExamsList
    })

def results(request):
    student = request.user

    studentGroup = Special_Students.objects.filter(students=student)
    studentExamList = StuExam_DB.objects.filter(student=student, completed=1)

    if request.method == 'POST':
        paper = request.POST['paper']
        viewExam = StuExam_DB.objects.get(examname=paper, student=student)
        return render(request, 'students/result/individualresult.html', {
            'exam': viewExam, 'student': student, 'quesn': viewExam.questions.all()
        })

    return render(request, 'students/result/results.html', {
        'student': student, 'paper': studentExamList
    })

