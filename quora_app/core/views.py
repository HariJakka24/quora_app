from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .custom_decorators.error_check_decorators import error_redirect_check
from .models import Question, Answer
from .forms import RegisterForm, QuestionForm, AnswerForm

@error_redirect_check
def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'questions': questions})

@error_redirect_check
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  # for debugging in terminal
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

@error_redirect_check
def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

@error_redirect_check
def logout_view(request):
    logout(request)
    return redirect('login')

@error_redirect_check
@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'core/post_question.html', {'form': form})

@error_redirect_check
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'core/question_detail.html', {'question': question, 'answers': answers, 'form': form})

@error_redirect_check
@login_required(login_url='/login')
def like_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return redirect('question_detail', pk=answer.question.pk)


def error_page(request):
    return render(request, 'core/error_page.html')

