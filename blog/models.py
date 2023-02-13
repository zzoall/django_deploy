from django.db import models

# Create your models here. 
# DB의 테이블을 좀더 쉽게 꺼내오기 위해 클래스 형식으로 바꿔주는 기능
class Post(models.Model):
    # 게시글에 필요한 필드: Primary Key, 제목, 내용, 작성일, 수정일, 작성자
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)  # 아예 값 자체가 지금 시간으로 입력되어 들어감(우리가 변경할 필요 없음)
    # created_at = models.DateTimeField(auto_now_add=True)  # 값을 변경할 수는 있지만 default 값으로 현재시간이 찍혀있음 
    updated_at = models.DateTimeField()
    # updated_at = models.DateTimeField(auto_now_add=True)
    # 작성자는 추후 작성 예정

    def __str__(self):
        return f'[[{self.pk}] {self.title}]'