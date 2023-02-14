from .models import UserAbstinence

class TrophyNotificationMiddlware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_anonymous == False:
            ua = UserAbstinence.objects.get(user=request.user)
            if ua.unchecked_trophies:
                request.session["unchecked_trophies"] = True
            else:
                request.session["unchecked_trophies"] = False

        return response