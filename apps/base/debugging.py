from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_drf_filepond.models import TemporaryUpload

@csrf_exempt
def revert_upload(request):
    if request.method == 'DELETE':
        upload_id = request.body.decode('utf-8')
        try:
            temp_upload = TemporaryUpload.objects.get(upload_id=upload_id)
            temp_upload.delete()
            return JsonResponse({'status': 'success'})
        except TemporaryUpload.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'File not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
