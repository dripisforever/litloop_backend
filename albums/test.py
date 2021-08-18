from django.db import models

[
    {
        "_id": "76070ba8-e9f8-11ea-a1ac-42010a800002",
        "courses": [
            {
                "_id": "-machine-learning-solutions",
                "title": " Machine Learning Solutions",
                "tags": [
                  "MAChine learning",
                ]
            },
            {
                "_id": "natural-language-processing",
                "title": "Natural Language Processing ",
                "tags": [
                  "Natural Language"
                ]
            }
        ],
        "description": "MAchine Learning"
        "popularity": "This Program is not rated yet"
    },
    {
        similar structure
    }
]

class Bundle(models.Model):
    name = models.charField(max_length=100)
    items = models.ManytoManyField(Item)
    popularity = models.CharField(max_length=100)

    def map_and_save(data=None):
        if data is None:
            return
        if isinstance(data, list):
            mapper = {
                "courses": ["items"],
                "description": "name",
                "popularity": "popularity"
            }

            for datum in data:
                bundle_data = {}
                item_instances = []
                for key, value in datum.items():
                    field_name = mapper.get(key, None)
                    if field_name is None:
                        continue
                    elif isinstance(field_name, list):
                        for _value in value:
                            item = Item.objects.create(name=_value.get("title"))
                            item_instances.append(item)
                        continue
                    bundle_data[field_name] = value
                bundle = Bundle.objects.create(**bundle_data)
                bundle.items.add(*item_instances)

    def create_new_movie(movie_data: dict) -> Optional[Movie]:
        """Create movie and associated ratings
        """
        if not movie_data:
            return None

        movie_data, rating_data = _parse_movie_data(movie_data)
        movie = Movie(**movie_data)
        movie.save()

        for rating in rating_data:
            movie.ratings.create(**rating)

        return movie


class Item(models.Model):
    name = models.charField(max_length=100)
    provider = models.ForeignKey(provider,null=True, blank=False,on_delete=models.CASCADE, related_name="+")
