# REFERENCE https://github.com/Illumiya/illumiya/blob/5dfbfcc4fef3b8543aacd4bf1bb40834c66efcec/illumiya/core/models.py#L59




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
