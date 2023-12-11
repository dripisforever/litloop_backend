from rest_framework import serializers
from movies.models import Movie

class MovieSerializer(serializers.ModelSerializer):

    # id = serializers.IntegerField(read_only=True)

    # class Meta:
    #     model = Movie
    #     fields = [
    #         'id',
    #         'title',
    #         'description',
    #         # 'created_at',
    #         # 'updated_at',
    #     ]

    class Meta:
           fields = '__all__'
           model = Movie
