from django.shortcuts import render

# Create your views here.
# api/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from netmiko import ConnectHandler


def make_conncn(device,config):
    
    try:
        with ConnectHandler(**device) as ssh:
            result=ssh.send_config_set(config)
            result=result.replace('\n','<br>')
            return (result,True)
    except Exception as msg:
        return (str(msg),False)

def collector(device,command):
    
    try:
        with ConnectHandler(**device) as ssh:
            result=ssh.send_command(command[0])
            #result=result.replace('\n','<br>')
            return (result,True)
    except Exception as msg:
        return (str(msg),False)

def collect_data(payload):
    iplist=payload['ipAddresses']
    out_dic={}
    for ip in iplist:
        dev = {
            'host': ip,
            'username':payload['username'],
            'password':payload['password'],
            'device_type':payload['deviceType'],
            'secret': payload['deviceType']
            }
        result=collector(dev,payload['configCommand'])
        out_dic[ip]={
            'status':result[1],
            'output':result[0]
        }
    return out_dic





def configure_device(payload):
    iplist=payload['ipAddresses']
    out_dic={}
    for ip in iplist:
        dev = {
            'host': ip,
            'username':payload['username'],
            'password':payload['password'],
            'device_type':payload['deviceType'],
            'secret': payload['deviceType']
            }
        result=make_conncn(dev,payload['configCommand'])
        out_dic[ip]={
            'config status':result[1],
            'config_log':result[0]
        }
    return out_dic



@csrf_exempt
def configure_device_view(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            result=configure_device(payload)  # Call your function here
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)




@csrf_exempt
def data_collector_view(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            result=collect_data(payload)  # Call your function here
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
