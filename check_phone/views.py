import json
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from check_phone import models

error_dict = {0: 'OK',
              1: 'no phone',
              2: 'wrong phone, must be like 79876543210',
              3: 'technical work please re-request later',
              4: 'operator not found'}


def get_phone(phone):
    code = phone[1:4]
    tel = phone[4:]
    return models.Phones.objects.filter(code=code, start__lte=tel, finish__gte=tel).first()


def check_phone(phone):
    if not phone:
        code = 1
    elif not phone.isdigit() or len(phone) != 11 or phone[0] != '7':
        code = 2
    else:
        code = 0
    return code


def check_base():
    settings = models.Settings.objects.first()
    if not settings:
        return None
    return settings.base_ready


class WebView(View):

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        phone = request.POST.get('phone')
        code = check_phone(phone)
        if not code:
            if not check_base():
                code = 3
        if not code:
            obj = get_phone(phone)
            if not obj:
                code = 4
        if code:
            return render(request, 'index.html', context={'error': error_dict.get(code, 'Unknown error')})
        return render(
            request, 'index.html', context={'phone': phone, 'obj': obj})


@method_decorator(csrf_exempt, name='dispatch')
class ApiView(View):

    def post(self, request):
        request_phone = json.loads(request.body.decode('utf8'))
        code = check_phone(request_phone)
        if not code:
            if not check_base():
                code = 3
        if not code:
            obj = get_phone(request_phone)
            if not obj:
                code = 4
        if code:
            return JsonResponse({'code': code, 'text': error_dict.get(code, 'Unknown error')})
        return JsonResponse({
            'code': code, 'text': error_dict.get(code),
            'phone': request_phone, 'operator': obj.operator.operator, 'location': obj.location.location})
