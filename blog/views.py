from django.shortcuts import render

# Create your views here.
# V (view) - 화면에 출력되는 부분을 책임집니다. 
def index(request):
    return render(
        request, 
        'blog/index.html'
    )

def index2(request):
    return render(
        request, 
        'index2.html'
    )