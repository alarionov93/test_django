import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.


def index(request, reg_success=None):
  # _id = request.GET.get('param1', None) # 'val1'
  if reg_success is not None: 
	# return HttpResponse(json.dumps({'a': 'b'}), content_type='application/json')
    ctx = { 
      "reg_success": reg_success,
      "test_list": [
        {
          "aaa": "asdfh",
        },
        {
          "aaa": "agfgsdf",
        },
        {
          "aaa": "asfgrbhjhmfj",
        }
      ]
    }
    return render(request, template_name='index.html', context=ctx)
  

  return redirect(to=reverse('r_site_index', args=(1,)))