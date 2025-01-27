import hmac
import hashlib
import subprocess
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def github_webhook(request):
    if request.method == 'POST':
        header_signature = request.headers.get('X-Hub-Signature-256')
        if not header_signature:
            return JsonResponse({'error': 'Signature missing'}, status=400)

        sha_name, signature = header_signature.split('=')
        if sha_name != 'sha256':
            return JsonResponse({'error': 'Unsupported hash algorithm'}, status=400)

        mac = hmac.new(
            settings.GITHUB_SECRET.encode(), msg=request.body, digestmod=hashlib.sha256
        )
        if not hmac.compare_digest(mac.hexdigest(), signature):
            return JsonResponse({'error': 'Invalid signature'}, status=403)

        try:
            subprocess.run(['/usr/bin/git', 'pull'], cwd="/app", check=True)
            subprocess.Popen("/srv/projects/devknowhow/restart.sh")
            
            return JsonResponse({'status': 'success'})
        
        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': f'Command failed: {e}'}, status=500)
        
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
