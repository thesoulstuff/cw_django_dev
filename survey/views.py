from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from survey.models import Question, Answer


class QuestionListView(ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_anonymous:
            return context
        object_list = []
        for question in context.get('object_list'):
            question.user_value = self.user_value(
                user,
                question
            )
            question.user_likes = self.user_likes(
                user,
                question
            )
            question.user_dislikes = self.user_dislikes(
                user,
                question
            )
            object_list.append(question)
        context["object_list"] = object_list
        return context


    def user_value(self, user, question):
        if Answer.objects.filter(question=question, author=user).exists():
            answer = Answer.objects.get(question=question, author=user)
            return answer.value
        return 0

    def user_likes(self, user, question):
        if Answer.objects.filter(question=question, author=user).exists():
            answer = Answer.objects.get(question=question, author=user)
            return answer.liked
        return 0

    def user_dislikes(self, user, question):
        if Answer.objects.filter(question=question, author=user).exists():
            answer = Answer.objects.get(question=question, author=user)
            return not answer.liked if answer.liked != None else None
        return False


class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'description']
    redirect_url = ''

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'


def answer_question(request):
    question_pk = request.POST.get('question_pk')
    if not request.POST.get('question_pk'):
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    answer, created = Answer.objects.get_or_create(question=question, author=request.user)
    answer.value = request.POST.get('value')
    answer.save()
    return JsonResponse({'ok': True})

def like_dislike_question(request):
    question_pk = request.POST.get('question_pk')
    if not request.POST.get('question_pk'):
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    answer, created = Answer.objects.get_or_create(question=question, author=request.user)
    if request.POST["liked"] == 'liked':
        answer.liked = True
    else:
        answer.liked = False
    # TODO: Dar Like
    answer.save()
    return JsonResponse({'ok': True})

