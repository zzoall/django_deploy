from django.shortcuts import render  # Function Based View 를 사용했습니다
from .models import Post, Category # 추가
from django.views.generic import ListView # 게시판형으로 데이터를 가지고 오는 클래스 
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator

class BlogList(ListView): 
    model = Post
    ordering = '-pk' 
    template_name = 'blog/blog_home.html'
    context_object_name = 'post_list'

    # ListView를 상속받으면서 전달받은 get_context_data라는 함수를 오버라이딩합니다
    def get_context_data(self, **kwargs): # 함수의 파라미터를 개수 안 정해서 k-v 순으로 만들어 보내겠다
        # 속성명 = 값 -> 파이썬의 namespace에서는 키:밸류 순으로 관리됩니다
        context = super(BlogList, self).get_context_data(**kwargs)
        context['first_post'] = Post.objects.all().last() # first_post라는 이름으로 하나 더 값을 만들어서 전달할게요
        # 필요한 값들을 ORM으로 뽑아서 가져올 수 있습니다.
        return context

class PostList(ListView):  # post_list 라고 생긴 template과 model을 조합합니다. 
    model = Post
    ordering = '-pk'
    # 글을 10개씩만 가져오기로 함 
    paginate_by = 5 # 한 페이지에 제한할 Object 수
    # object가 페이지 당 10개씩 나타내면, 뒤에 일부가 남을때 자투리 object가 5개 이상일 때만 출력하겠음
    paginate_orphans = 2  # 자투리 처리
    page_kwarg = "page" # 페이징과 관련된 argument

    # 추가
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

# blog 폴더(앱)에서 post_detail.html로 가고 있는 객체를 posts라고 이름을 변경해보세요
# 해당 변수명으로 받은 객체들에 더해 subject 라는 이름으로 제목 데이터만 전달하는 추가 변수를 달아주세요

class PostDetail(DetailView):  # post_detail 라고 생긴 template과 model을 조합합니다. 
    model = Post
   

    def get_context_data(self, **kwargs): # 함수의 파라미터를 개수 안 정해서 k-v 순으로 만들어 보내겠다
        # 속성명 = 값 -> 파이썬의 namespace에서는 키:밸류 순으로 관리됩니다
        context = super(PostDetail, self).get_context_data(**kwargs)
        # print(context['object']) # 뭐가 들어있나 확인해보세요
        context['subject'] = context['object'].title 
        # 필요한 값들을 ORM으로 뽑아서 가져올 수 있습니다.
        return context

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

