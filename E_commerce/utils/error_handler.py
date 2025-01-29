from django.http import JsonResponse

def handler404(request, exception):
    response = JsonResponse({'error': 'Path not found'})
    response.status_code = 404
    return response

def handler500(request):
    response = JsonResponse({'error': 'Internal Server Error'})
    response.status_code = 500
    return response