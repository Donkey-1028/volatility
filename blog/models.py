from django.db import models
from django.urls import reverse

class Post(models.Model):
    author = models.CharField('User', max_length=10)
    password = models.CharField('Password', max_length=10)

    title = models.CharField('Title', max_length=10)
    content = models.TextField('Content')

    create_date = models.DateTimeField('Create date', auto_now_add=True)
    update_date = models.DateTimeField('Update date', auto_now=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #get_absolute_url 호출시 detail호출, pk값에 self.id 를 넘겨줌
        return reverse('blog:detail', kwargs={'pk': self.id})





#이번 프로젝트에서는 직접 댓글다는것을 구현 하기로함.
class Comment(models.Model):
    #어떠한 포스트의 댓글인지 체크하기위해 외래키 Post모델과 연결.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    author = models.CharField('User', max_length=10)
    password = models.CharField('Password', max_length=10)
    comment = models.CharField('Comment', max_length=100)

    create_date = models.DateTimeField('Create date', auto_now_add=True)

    def __str__(self):
        return self.comment


class HitCount(models.Model):
    """조회수 model. 검색을 해보니 보통은 쿠키를 이용해서 조회수를 올리지만,
    단점으로는 인터넷 쿠키를 삭제하고 다시 조회 할 경우 조회수는 계속 올라간다.
    그래서 IP주소로 조회수를 올린다면 어떻게 될까 하고 만들어 보았다."""

    hit_count = models.PositiveIntegerField(default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(protocol='IPv4')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title
# Create your models here.
