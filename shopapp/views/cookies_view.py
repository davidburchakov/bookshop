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
        user_agent, ip_address, browser, os, location = get_user_agent(request)

        # Save the information
        UserActivity.objects.create(ip_address=ip_address, location=location, user_agent=user_agent, browser=browser,
                                    os=os)

    elif consent == 'rejected':
        response.set_cookie('cookie_consent', 'rejected')

    return response


def get_user_agent(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ip_address = get_client_ip(request)
    browser = "Unknown"
    os = "Unknown"
    location = "Unknown"  # Without an external service, you can only capture the IP address.

    if "windows" in user_agent.lower():
        os = "Windows"
    elif "linux" in user_agent.lower():
        os = "Linux"

    if "chrome" in user_agent.lower():
        browser = "Chrome"
    elif "firefox" in user_agent.lower():
        browser = "Firefox"

    return user_agent, ip_address, browser, os, location


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
