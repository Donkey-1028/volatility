from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.utils import timezone
import random

#프론트 단에 Message를 보낼 수 있는 패키지.
from django.contrib import messages


def get_client_ip(request):
    """클라이언트의 IP를 가져 오는 함수."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_ip(request, model, pk):
    """해당 IP로 조회수를 올린 적 있는지 확인, 만약 있다고 하면
    조회수 Field는 그대로, 없으면 조회수를 올림."""
    ip = get_client_ip(request)
    queryset = model.objects.get_or_create(
        ip=ip,
        post_id=pk,
        defaults={'ip': ip,
                 'post_id': pk
                 }
    )
    return queryset

def home(request):
    return render(request, 'blog/home.html')

def index(request):

    today = timezone.now()
    yesterday = today - timezone.timedelta(hours=24)
    #지금을 기준으로 24시간 안에 작성된 Post만 필터링
    post = Post.objects.filter(update_date__range=(yesterday, today))
    #공지 사항 느낌.
    admin_post = Post.objects.filter(author='admin')
    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST or None)

        if form.is_valid():
            schType = '%s' % request.POST['search_type']
            schWord = form.cleaned_data['search_word']
            #schWord = '%s' % request.POST['search_word'] 와 같은 의미이지만. form.cleaned_data가
            # 더 안전하다고 하다. python에 맞게 형식도 바꿔준다고 함.

            #검색을 하는 인덱스 기준이 무엇인지 확인하기 위한 함수, 작성자,제목,내용을 검색할것인지 체크
            def type_check(model, schType):
                if schType == 'author':
                    search_list = model.objects.filter(Q(author__icontains=schWord), update_date__range=(yesterday, today))
                elif schType == 'title':
                    search_list = model.objects.filter(Q(title__icontains=schWord), update_date__range=(yesterday, today))
                elif schType == 'content':
                    search_list = model.objects.filter(Q(content__icontains=schWord), update_date__range=(yesterday, today))
                return search_list

            context={}
            context['admin_post'] = admin_post
            context['form'] = form
            context['post'] = post
            context['search_word'] = schWord
            context['search_list'] = type_check(Post, schType)

            if not context['search_list'].exists():
                """만약 주어진 키워드로 검색된 데이터가 없다면
                message 출력 하기 위해 message를 프론트단에 보내줌."""
                messages.warning(request, schWord + ' 에 관한 검색결과가 없습니다.')
                return redirect('/')

            return render(request, 'blog/index.html', context)

    return render(request, 'blog/index.html', {'post': post, 'form': form,
                                               'admin_post': admin_post})

# Post에 관해 삭제하거나 업데이트, 댓글 달기와 삭제
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #외래키로 외래모델의 기본키를 가져올때는 '필드명_id'
    comments = Comment.objects.filter(post_id=pk)
    check_ip(request, HitCount, pk)
    hit = HitCount.objects.filter(post_id=pk)
    random_name = str(round(random.random() * 10000))
    # 글쓴이의 이름을 익명+random숫자로 지정함

    if request.method == 'POST':
        form1 = CommentForm(request.POST or None)

        if form1.is_valid():
            form1.instance.post_id = pk
            form1.save()
    else:
        form1 = CommentForm(initial={'author': '익명'+random_name})

    return render(request, 'blog/detail.html', {'post': post, 'comments': comments,
                                                'form1': form1, 'hit': hit})


def post_create(request):
    random_name = str(round(random.random() * 10000))
    # 글쓴이의 이름을 익명+random숫자로 지정함

    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = PostForm(initial={'author': '익명' + random_name})

    return render(request, 'blog/form.html', {'form': form})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)


    if request.method == 'POST':
        form = PostForm(request.POST or None)

        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        # instance로 이미 작성된 post를 보내줌
        form = PostForm(instance=post)

    return render(request, 'blog/form.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PasswordCheck(request.POST or None)

    # 비밀번호를 주고 받기때문에 정석적인 방법이다.
    if request.method == 'POST':
        form = PasswordCheck(request.POST or None)
        if form.is_valid():
            if post.password == form.cleaned_data['check_password']:
                post.delete()
                return redirect('/')
            else:
                messages.warning(request, '비밀번호가 틀립니다')


    return render(request, 'blog/delete.html', {'post': post, 'form': form})

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    #비밀번호를 주고 받는 것이기 때문에 GET통신은 보안적으로 매우 취약하다고 한다.
    #post_delete()에서 정석적인 방법을 사용하고있다.
    if request.method == 'GET':
        password = request.GET.get('password')
        if comment.password == password:
            comment.delete()
        else:
            messages.warning(request, '비밀번호가 틀립니다.')

    return redirect('blog:detail', pk=comment.post.pk)

