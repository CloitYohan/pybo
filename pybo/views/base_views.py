from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from ..models import Question
from . import question_views

def index(request):
    3 / 0  # 강제로 오류발생
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    elif so == 'mostviewed':
        question_list = Question.objects.order_by('-view_number', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)
    #return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


#question url
def detail(request, question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk = question_id)

    #question.view_number += 1
    #question.save()

    answer_list = question.answer_set.order_by('-create_date')
    page = request.GET.get('page', '1')  # 페이지
    paginator = Paginator(answer_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    if request.session.get("question_id") == question_id:
        return render(request, 'pybo/question_detail.html', {'question': question, 'answer_list':page_obj, 'page': page })

    question_views.increase_views(request, question_id)
    request.session['question_id'] = question_id
    context = {'question': question, 'answer_list':page_obj, 'page': page }
    return render(request, 'pybo/question_detail.html', context)