from django.shortcuts import redirect


class LoginRedirectMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            return redirect("accounts:profile")
        else:
            return super().dispatch(request, *args, **kwargs)
