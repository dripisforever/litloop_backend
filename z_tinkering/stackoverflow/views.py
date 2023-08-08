# REFERENCE: https://aws.plainenglish.io/setup-celery-5-0-and-aws-sqs-with-django-125be52262fc
from .tasks import run_job

def post(self, request):
    p = request.data.get('product') #return in dict
    product = Product(title=p['title'], description=p['description'], price=p['price'])
    product.save()
    # Call celery task to update status
    run_job(product.id)
    return Response({"success":"true", "message": "Product '{}' created successfully".format(p['title'])})
