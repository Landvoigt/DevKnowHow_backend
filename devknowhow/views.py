import hmac
import hashlib
import subprocess
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def github_webhook(request):
    if request.method == 'POST':
        header_signature = request.headers.get('X-Hub-Signature-256')
        if not header_signature:
            logger.error('Signature missing')
            return JsonResponse({'error': 'Signature missing'}, status=400)

        sha_name, signature = header_signature.split('=')
        if sha_name != 'sha256':
            logger.error('Unsupported hash algorithm')
            return JsonResponse({'error': 'Unsupported hash algorithm'}, status=400)

        mac = hmac.new(
            settings.GITHUB_SECRET.encode(), msg=request.body, digestmod=hashlib.sha256
        )
        if not hmac.compare_digest(mac.hexdigest(), signature):
            logger.error('Invalid signature')
            return JsonResponse({'error': 'Invalid signature'}, status=403)

        payload = request.body.decode('utf-8')
        logger.info(f'Received payload: {payload}')

        try:
            django_container_name = "django_app"
            project_path = "/srv/projects/devknowhow/devknowhow_backend"
            host_project_path = "/srv/projects/devknowhow"
            
            logger.info('Running git pull...')
            subprocess.run(['git', 'pull'], cwd=project_path, check=True)
            
            logger.info('Stopping and restarting docker containers...')
            subprocess.run(['docker-compose', 'down'], cwd=host_project_path, check=True)
            subprocess.run(['docker-compose', 'up', '-d'], cwd=host_project_path, check=True)

            logger.info('Running migrations...')
            subprocess.run(['docker', 'exec', django_container_name, 'bash', '-c', 'python manage.py makemigrations'], check=True)
            subprocess.run(['docker', 'exec', django_container_name, 'bash', '-c', 'python manage.py migrate'], check=True)
            
            return JsonResponse({'status': 'success'})
        
        except subprocess.CalledProcessError as e:
            logger.error(f'Command failed: {e}')
            return JsonResponse({'error': f'Command failed: {e}'}, status=500)
        
    logger.error('Invalid HTTP method')
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
