from django.db import models


# Create your models here.

# 电脑信息表
class Computer(models.Model):
    computer_id = models.BigIntegerField(primary_key=True)
    brand = models.CharField(max_length=30, null=False)
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    img_url = models.CharField(max_length=255)
    param = models.TextField()
    if_spider = models.BooleanField(default=False)
    good_rate = models.FloatField(default=0.0)

    class Meta:
        db_table = 'computer'

#  评论标签
class Tag(models.Model):
    tags = models.CharField(max_length=255, null=False)
    count = models.CharField(max_length=200, null=False)
    computer = models.OneToOneField(Computer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'computer_tag'


#  评论内容
class Comment(models.Model):
    comment_id = models.CharField(max_length=40, unique=True)
    content = models.TextField()
    jieba_content = models.TextField()
    score = models.BigIntegerField(null=False)
    create_time = models.CharField(max_length=30)
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'computer_comment'
