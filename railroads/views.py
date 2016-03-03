# coding=utf-8
from django.shortcuts import redirect


def main(request):
    """
    Переадресовывает пользователя со стартовой страницы на /schedule
    """
    return redirect('schedule/')

