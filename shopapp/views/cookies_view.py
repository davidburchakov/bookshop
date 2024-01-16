from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from shopapp.models.models import UserActivity
import json


@csrf_exempt
@require_POST
def set_cookie_consent(request):
    data = json.loads(request.body)
    consent = data.get('consent')

    response = JsonResponse({'status': 'success'})

    # Set a cookie based on user's choice
    if consent == 'accepted':
        response.set_cookie('cookie_consent', 'accepted')

        ip_address = get_client_ip(request)
        browser_info = request.META.get('HTTP_USER_AGENT', '')

        # For location, you can either leave it blank or use an external service.
        # Without an external service, you can only capture the IP address.
        location = "Not available without external service"

        # Save the information
        UserActivity.objects.create(ip_address=ip_address, location=location, browser_info=browser_info)
        print("ip address:", ip_address)
        print("location:", location)
        print("browser_info:", browser_info)

    elif consent == 'rejected':
        response.set_cookie('cookie_consent', 'rejected')

    return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
