from django.shortcuts import render, redirect, get_object_or_404  # Function Based View 를 사용했습니다
from .models import Post, Category, Tag
from django.views.generic import ListView # 게시판형으로 데이터를 가지고 오는 클래스 
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from .forms import CommentForm
from django.core.exceptions import PermissionDenied # 인가 - 권한이 있는 경우가 아니면 발생시키는 예외처리

class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content', 'header_img', 'file_upload', 'category']
    # tag -> #카지노 #카지노_행님_20만원만 unique=True : 여러개 달았을 때 이미 있는 해시태그는 더 등록되지 않도록 
    # author -> 로그인 하는 순간부터 author 는 남아있기 때문에
    # created_at -> 작성되는 순간 자동 등록  
    # updated_at -> 수정되는 순간 자동 등록

class BlogHome(ListView):
    model = Post
    ordering = '-pk' 
    template_name = 'blog/blog_home.html'
    context_object_name = 'posts'

    # ListView를 상속받으면서 전달받은 get_context_data라는 함수를 오버라이딩합니다
    def get_context_data(self, **kwargs): # 함수의 파라미터를 개수 안 정해서 k-v 순으로 만들어 보내겠다
        # 속성명 = 값 -> 파이썬의 namespace에서는 키:밸류 순으로 관리됩니다
        context = super(BlogHome, self).get_context_data(**kwargs)
        context['first_post'] = Post.objects.all().last() # first_post라는 이름으로 하나 더 값을 만들어서 전달할게요
        # 필요한 값들을 ORM으로 뽑아서 가져올 수 있습니다.
        return context


class PostList(ListView):  # post_list 라고 생긴 template과 model을 조합합니다. 
    model = Post
    ordering = '-pk' 
    paginate_by = 5 # n개씩 잘라서 data(record)를 전송해주는 속성. views.py에서도, urls.py도 줄 수 있습니다
    paginate_orphans = 3 # 자투리 101개 있음 -> 5개씩 값을 꺼내오면 마지막 남는 1개(orphan)가 있음...
                        # 디자인 깨지지 않게 5개씩 꺼내올 때 값이 2개 이하이면 마지막 페이지에 걍 붙여버려

    # post_list에 전달할 전체 객체명을 바꿔줍니다.
    context_object_name = 'posts'

    # ListView를 상속받으면서 전달받은 get_context_data라는 함수를 오버라이딩합니다
    def get_context_data(self, **kwargs): # 함수의 파라미터를 개수 안 정해서 k-v 순으로 만들어 보내겠다
        # 속성명 = 값 -> 파이썬의 namespace에서는 키:밸류 순으로 관리됩니다
        context = super(PostList, self).get_context_data(**kwargs)
        context['first_post'] = Post.objects.all().last() # first_post라는 이름으로 하나 더 값을 만들어서 전달할게요
        context['categories'] = Category.objects.all()
        # 그냥 post_list.html에서 미분류의 개수를 세서 숫자를 표기해주기 위한 ORM 쿼리
        context['no_category_post_count'] = Post.objects.filter(category=None).count() 
        # 필요한 값들을 ORM으로 뽑아서 가져올 수 있습니다.
        return context

    
# blog 폴더(앱)에서 post_detail.html로 가고 있는 객체를 posts라고 이름을 변경해보세요
# 해당 변수명으로 받은 객체들에 더해 subject 라는 이름으로 제목 데이터만 전달하는 추가 변수를 달아주세요

class PostDetail(DetailView):  # post_detail 라고 생긴 template과 model을 조합합니다. 
    model = Post
    # context_object_name = 'posts'

    def get_context_data(self, **kwargs): # 함수의 파라미터를 개수 안 정해서 k-v 순으로 만들어 보내겠다
        # 속성명 = 값 -> 파이썬의 namespace에서는 키:밸류 순으로 관리됩니다
        context = super(PostDetail, self).get_context_data(**kwargs)
        # print(context['object']) # 뭐가 들어있나 확인해보세요
        context['subject'] = context['object'].title 
        # 필요한 값들을 ORM으로 뽑아서 가져올 수 있습니다.
        context['comment_form'] = CommentForm
        return context

def category_posts(request, slug):
    # 조건문을 완성해주세요 
    # 카테고리가 있으면 아래와 같이 
    if slug == "no_category":
        posts = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        posts = Post.objects.filter(category=category)

    # 카테고리가 없으면 None을 가지고 있는 값을 보냅니다.
    return render(
        request,
        'blog/post_list.html',
        {
            'posts' : posts,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count()
            # 카테고리 위젯을 잘 완성시키기 위해 만들어야 되는 변수들
            # no_category 글의 개수 세기기 count()
            # Post.objects.filter(category=None)를 호출하도록 urls도 변경해야 할겁니다

        }

    )


def tag_posts(request, slug):
    # 조건문을 완성해주세요 
    if slug == "no_tag":
        posts = Post.objects.filter(tag=None)
    else:
        tag = Tag.objects.get(slug=slug) # /hiphop
        posts = Post.objects.filter(tag=tag)

    # 카테고리가 없으면 None을 가지고 있는 값을 보냅니다.
    return render(
        request,
        'blog/post_list.html',
        {
            'posts' : posts,
            'tag' : tag,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count()
        }

    )

# 글쓰기 버튼 -> 로그인 했을 때만 나오게 하는 것과 유사
# 글쓰기 버튼 -> 누구나 로그인한 회원이면 다 쓸 수 있게 

# 댓글은 누가 다는지 ->  로그인한 사람만 달 수 있게 할거에요 (인증)

# 댓글을 쓰고 작성완료 버튼을 누르면 생기는 일
# 우리는 post_detail.html에 돌아가게 됩니다
# 댓글화면에는 지금 등록한 댓글이 출력됩니다

# 로그인(인증) 
# -> 나 이 댓글/글을 수정할 수 있는 회원이야(권한, 자격) 확인하는 과정 (인가)
# 내가 단 댓글만 수정, 삭제를 할 수 있게 할 거에요 

def new_comment(request, pk):
    # 일단 로그인상태인지 확인을 합니다
    if request.user.is_authenticated:
        # 없는 글을 호출한 경우 -> 404 에러를 내거나
        post = get_object_or_404(Post, pk=pk)
        # 있으면 post를 전달하되 글번호에 맞는 post를 전달합니다. 
        # post = Post.objects.filter(pk=pk)
    # 그리고 데이터가 잘 왔는지 확인합니다 
        if request.method=='POST':
            comment_form = CommentForm(request.POST)
            # comment_form이 인가를 거친 폼이면(아무가 아니라 로그인하고 댓글 쓸 자격이 있는 사람의 코멘트이면)
            if comment_form.is_valid():
            # 그리고 데이터를 DB에 넣어줍니다
                comment = comment_form.save(commit=False) # commit
                comment.post = post
                comment.author = request.user
                comment.save()
            # blog/post_list.html, 글번호가 있는 자리 -> 이 자리를 어딘가에서 만들어주면 될 거 같아요
            # 새로 바뀐 DB(등록된 댓글)의 데이터를 가지고 화면으로 돌아갑니다 
                return redirect(comment.get_absolute_url())
            else:
                return redirect(post.get_absolute_url())
        else:
            raise PermissionDenied

def about_me(request):
    return render(
        request,
        'blog/about.html'
    )

def contact(request):
    return render(
        request,
        'blog/contact.html'
    )
# Create your views here.
# V (view) - 화면에 출력되는 부분을 책임집니다. 
# def index(request):
#     return render(
#         request, 
#         'blog/index.html'
#     )

# def index2(request):
#     return render(
#         request, 
#         'index2.html'
#     )

