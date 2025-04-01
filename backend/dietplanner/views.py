from django.http import HttpResponse, JsonResponse

def index(request):
    return JsonResponse({
        "message": "Welcome to AI Diet Planner API",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "user_api": "/api/users/"
        }
    })