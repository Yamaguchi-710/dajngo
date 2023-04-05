# from django.http import HttpResponse

# def index(request):    
#     # return HttpResponse('hello')
#     # return HttpResponse('<img src="/media/output.png" />')


from django.shortcuts import render
 
def index(request):
    return render(request, 'index.html')