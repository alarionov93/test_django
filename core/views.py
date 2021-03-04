import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.


def index(request):
  _id = request.GET.get('reg_success', None)
  if _id is not None: 
	# return HttpResponse(json.dumps({'a': 'b'}), content_type='application/json')
    
    return render(request, template_name='index.html', context={ "reg_success":_id, "test_list": [1,2,3,54] })
  

  return redirect(to=reverse('r_site_index') + '?reg_success=1')