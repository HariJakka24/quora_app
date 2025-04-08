from django.shortcuts import redirect


def error_redirect_check(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return redirect('error_page')
    return wrapper