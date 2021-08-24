from django.test import TestCase
from django.contrib.auth.models import User
from survey.models import Question, Answer
from datetime import datetime

class RankingTest(TestCase):
    def setUp(self):
        users_data = [
            ("user1", "test1"),
            ("user2", "test2"),
            ("user3", "test3"),
            ("user4", "test4"),
            ("user5", "test5"),
            ("user6", "test6"),
        ]
        for username, password in users_data:
            User.objects.create(username=username,password=password)
    
    def test_ranking_new_question_with_no_answers(self):
        user = User.objects.get(username="user1")
        question = Question(
            author=user,
            title="Wild Rose?",
            description="The insignia of the Kingdom of Fynn. The rebels also use it as their password."
        )
        question.save()
        self.assertEqual(question.ranking, 10)

    def test_ranking_old_question_with_no_answers(self):
        user = User.objects.get(username="user2")
        question = Question(
            author=user,
            title="How much wood?",
            description="How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
        )
        question.save()
        question.created = datetime(2000, 5, 17)
        question.save()
        self.assertEqual(question.ranking, 0)

    def test_question_ranking(self):
        user = User.objects.get(username="user3")
        question = Question(
            author=user,
            title="How much wood?",
            description="How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
        )
        question.save()
        self.assertEqual(question.ranking, 10)
        answer = Answer(
            question=question,
            author=user,
            value=1
        )
        answer.save()
        self.assertEqual(question.ranking, 20)
        answer.liked = False
        answer.save()
        self.assertEqual(question.ranking, 17)
        answer.liked = True
        answer.save()
        self.assertEqual(question.ranking, 25)
        answer.value = 0
        answer.save()
        self.assertEqual(question.ranking, 15)
        answer.liked = False
        answer.save()
        self.assertEqual(question.ranking, 7)