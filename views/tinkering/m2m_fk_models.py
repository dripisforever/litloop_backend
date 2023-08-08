# REFERENCE https://stackoverflow.com/questions/74500748/increment-integer-field-in-django



class Post(models.Model):
    likes_count = models.IntegerField(default=0, blank=True) # kinda important


    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey('users.User', related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', related_name='likes', on_delete=models.CASCADE)
