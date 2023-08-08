




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.ManyToManyField(User, through="View")
	view_count = models.IntegerField(default=0)


class View(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
