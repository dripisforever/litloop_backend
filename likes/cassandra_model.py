from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
from .models import User, Post

class Like(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user = columns.UUID()
    post = columns.UUID()
    timestamp = columns.DateTime()
    # Add more fields as needed

    @classmethod
    def create(cls, user_id, post_id):
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        like = cls(user=user.id, post=post.id, timestamp=datetime.now())
        like.save()
        return like
