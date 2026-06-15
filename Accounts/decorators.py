from django.shortcuts import redirect
from django.contrib import messages


def role_required(roles):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if request.user.role in roles:
                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            messages.error(
                request,
                "You are not authorized."
            )

            return redirect("dashboard")

        return wrapper

    return decorator