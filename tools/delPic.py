from django.shortcuts import redirect,reverse
from django.http import JsonResponse
import os

# 删除旧服务器图片
def delPic(img_url):
    d=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tu_jpg=os.path.join(d,"media/" + img_url)
    if os.path.isfile(tu_jpg):
        os.remove(tu_jpg)