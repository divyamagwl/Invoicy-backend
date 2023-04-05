from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register': reverse('user-list', request=request, format=format),
        'login': reverse('user-login', request=request, format=format),
        'add-client': reverse('add-client', request=request, format=format),
        'fetch-clients': reverse('fetch-clients', request=request, format=format),
    })