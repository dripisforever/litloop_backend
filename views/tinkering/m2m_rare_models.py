# REFERENCE https://github.com/Dekatron322/onion/blob/5c3e872efcac7444af02761507d0879cbe8f8e9c/main/models.py#L77




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.ManyToManyField(View, through="PostView")
	view_count = models.IntegerField(default=0)


class View(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.BooleanField(default=True)


class PostView(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	view = models.ForeignKey(View, on_delete=models.CASCADE)
