from django.shortcuts import render,redirect
from django_ratelimit.exceptions import Ratelimited
from django.shortcuts import render


# class RatelimitMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         try:
#             response = self.get_response(request)
#         except Ratelimited:
#             return render(
#                 request,
#                 "verify_otp.html",
#                 {
#                     "rate_limited": True,
#                     "error": "Too many OTP attempts. Please wait 1 minute."
#                 },
#                 status=429
#             )
#         return response

class TwoFAMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_2fa_enabled:
                if not request.session.get("2fa_verified"):
                    if request.path not in ["/verifyotp/", "/logout/"]:
                        return redirect("verifyotp")
        return self.get_response(request)

        