from django.test import TestCase
from django.urls import reverse
from .models import User, Question, Answer


class UserAuthTests(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
            'email': 'testuser@gmail.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='StrongPass123', email= 'testuser@gmail.com',)
        # print("Login status:", user.is_active)
        login = self.client.login(username='testuser', password='StrongPass123')
        # print("Login status:", login)
        self.assertTrue(login)


class QuestionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='poster', password='pass1234', email= 'testuser@gmail.com',)
        self.client.login(username='poster', password='pass1234')

    def test_post_question(self):
        response = self.client.post(reverse('post_question'), {
            'title': 'What is Django?',
            'body': 'Explain it like I am five.'

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)

    def test_view_questions(self):
        Question.objects.create(user=self.user, title='Sample Q', body='test')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Q')


class AnswerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='responder', password='pass123', email= 'testuser@gmail.com')
        self.client.login(username='responder', password='pass123')
        self.question = Question.objects.create(user=self.user, title='Q1', body='desc')

    def test_post_answer(self):
        response = self.client.post(reverse('question_detail', args=[self.question.id]), {
            'content': 'Here is an answer.',
            'body': 'test body'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 1)

    def test_like_answer(self):
        answer = Answer.objects.create(user=self.user, question=self.question, body='Nice one!')
        response = self.client.post(reverse('like_answer', args=[answer.id]))
        answer.refresh_from_db()
        self.assertEqual(answer.likes.count(), 1)
        self.assertIn(self.user, answer.likes.all())




