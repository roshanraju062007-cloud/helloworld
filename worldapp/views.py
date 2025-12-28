from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def Home(request):
    return HttpResponse("Hello World")

@csrf_exempt
def login(request):
    if request.method == 'GET':
        # Simple HTML login screen
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Login</title>
            <style>
                body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; }
                form { max-width: 360px; display: grid; gap: 0.75rem; }
                label { display: grid; gap: 0.25rem; }
                input { padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; }
                button { padding: 0.5rem 0.75rem; border: 0; border-radius: 6px; background: #1677ff; color: white; }
            </style>
        </head>
        <body>
            <h1>Login</h1>
            <form method="post" action="/login">
                <label>
                    Username
                    <input type="text" name="username" required />
                </label>
                <label>
                    Password
                    <input type="password" name="password" required />
                </label>
                <button type="submit">Sign In</button>
            </form>
            
        </body>
        </html>
        """
        return HttpResponse(html)

    if request.method == 'POST':
        # Accept both form-encoded and JSON
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            try:
                data = json.loads(request.body or "{}")
                username = username or data.get('username')
                password = password or data.get('password')
            except json.JSONDecodeError:
                pass

        if not username or not password:
            return JsonResponse({
                'success': False,
                'message': 'Username and password are required'
            }, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid username or password'
            }, status=401)

    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)