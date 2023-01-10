from django.shortcuts import render,redirect
from .models import Notes,Homework,Todo
from .forms import *
import requests 
from django.views import generic
from django.contrib import messages
from youtubesearchpython import VideosSearch

def home(request):
  return render(request,'dashboard/home.html')

def notes(request):
  if request.method=="POST":
    form=NotesForm(request.POST)
    if form.is_valid():
      notes=Notes(user=request.user,title=request.POST['title'],desc=request.POST['desc'])
      notes.save()
      messages.success(request,f"Notes from {request.user.username} added successfully")
  else:
    form=NotesForm()
  notes=Notes.objects.filter(user=request.user)
  context={'notes':notes,'form':form}
  return render(request,'dashboard/notes.html',context)

def delete(request,pk=None):
  Notes.objects.get(id=pk).delete()
  return redirect("notes")
# Create your views here.


class NoteDetailView(generic.DetailView):
  model=Notes

def homework(request):
  if request.method=="POST":
    form=HomeworkForm(request.POST)
    if form.is_valid():
      try:
        finished=request.POST['is_finished']
        if finished=='on':
          finished=True
        else:
          finished=False
      except:
        finished=False
      homeworks=Homework(user=request.user,subject=request.POST['subject'],title=request.POST['title'],
      desc=request.POST['desc'],due=request.POST['due'],is_finished=finished)
      homeworks.save() 
      messages.success(request,f"Homework from {request.user.username} added successfully")       
  else:
    form=HomeworkForm()

  # form=HomeworkForm()
  homework=Homework.objects.filter(user=request.user)
  if len(homework)==0:
    homework_done=True
  else:
    homework_done=False  
  context={'homework':homework,'homework_done':homework_done,'form':form}
  return render(request,'dashboard/homework.html',context)  

def update_homework(request,pk=None):
  homework=Homework.objects.get(id=pk)
  if homework.is_finished == True:
    homework.is_finished=False
  else:
    homework.is_finished=True
  homework.save()
  return redirect('homework')    


def delete_homework(request,pk=None):
  Homework.objects.get(id=pk).delete()
  return redirect("homework")


def youtube(request):
  if request.method=="POST":
    form=DashboardForm(request.POST)
    text=request.POST['text']
    video=VideosSearch(text,limit=10)
    result_list=[]
    for i in video.result()['result']:
      result_dict={
        'input':text,
        'title':i['title'],
        'duration':i['duration'],
        'thumbnail':i['thumbnails'][0]['url'],
        'channel':i['channel']['name'],
        'link':i['link'],
        'views':i['viewCount']['short'],
        'published':i['publishedTime'],
      }
      desc=''
      if i['descriptionSnippet']:
        for j in i['descriptionSnippet']:
          desc += j['text']
      result_dict['description']=desc
      result_list.append(result_dict)
      context={'form':form,'results':result_list}  
    return render(request,'dashboard/youtube.html',context)      
  else:
    form=DashboardForm()  
  context={'form':form}
  return render(request,'dashboard/youtube.html',context)  


def todo(request):
  if request.method=='POST':
    form=TodoForm(request.POST)
    if form.is_valid():
      try:
        finished=request.POST['is_finished']
        if finished=='on':
          finished=True
        else:
          finished=False
      except:
        finished=False
      todo=Todo(user=request.user,title=request.POST['title'],is_finished=finished)
      todo.save()        
      messages.success(request,f"Todo from {request.user.username} added successfully")           
  else:
    form=TodoForm()
  todo=Todo.objects.filter(user=request.user)  
  if len(todo)==0:
    todo_done=True
  else:
    todo_done=False    
  
  context={'todo':todo,'form':form,'todo_done':todo_done}
  return render(request,'dashboard/todo.html',context)  

def update_todo(request,pk=None): 
  todo=Todo.objects.get(id=pk)
  if todo.is_finished == True:
    todo.is_finished=False
  else:
    todo.is_finished=True
  todo.save()
  return redirect('todo')   

def delete_todo(request,pk=None):
  Todo.objects.get(id=pk).delete()
  return redirect("todo")

def books(request):
  if request.method=="POST":
    form=DashboardForm(request.POST)
    text=request.POST['text']
    url="https://www.googleapis.com/books/v1/volumes?q="+text
    r=requests.get(url)
    answer=r.json()
    result_list=[]
    for i in range(10):
      result_dict={
        'title':answer['items'][i]['volumeInfo']['title'],
        'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
        'description':answer['items'][i]['volumeInfo'].get('description'),
        'count':answer['items'][i]['volumeInfo'].get('pageCount'),
        'categories':answer['items'][i]['volumeInfo'].get('categories'),
        'rating':answer['items'][i]['volumeInfo'].get('rating'),
        'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
        'preview':answer['items'][i]['volumeInfo'].get('previewLink')
      }
      result_list.append(result_dict)
      context={'form':form,'results':result_list}  
    return render(request,'dashboard/books.html',context)      
  else:
    form=DashboardForm()  
  context={'form':form}
  return render(request,'dashboard/books.html',context)  

def dictionary(request):
    if request.method=="POST":
      form=DashboardForm(request.POST)
      text=request.POST['text']
      url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
      r=requests.get(url)
      answer=r.json()
      try:
        phonetics=answer[0]['phonetics'][0]['text']
        audio=answer[0]['phonetics'][0]['audio']
        definiton=answer[0]['meanings'][0]['definitions'][0]['definition']
        example=answer[0]['meanings'][0]['definitions'][0]['example']
        synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
        context={'form':form,'input':input,'phonetic':phonetics,'audio':audio,'definiton':definiton,'example':example,'synonyms':synonyms}
      except:
        context={'form':form,'input':''}
      return render(request,"dashboard/dictionary.html",context)
    else:      
      form=DashboardForm()
      context={'form':form}
    return render(request,'dashboard/dictionary.html',context)

def conversion(request):
  if request.method=="POST":
    form=COnversionForm(request.POST)
    if request.POST['measurements']=='length':
      measurement_form=ConversionLengthForm()
      context={'form':form,'m_form':measurement_form,'input':True}
      if 'input' in request.POST:
        first=request.POST['measure1']
        second=request.POST['measure2']
        input=request.POST['input']
        answer=''
        if input and int(input)>=0:
          if first =='yard' and second=='foot':
            answer=f'{first} yard = {int(input)*3} foot'
          if first =='yard' and second=='foot':
            answer=f'{first} foot = {int(input)//3} yard'
        context={
          'form':form,
          'm_form':measurement_form,
          'input':True,
          'answer':answer
        }      
      else:
        if request.POST['measurements']=='mass':
          measurement_form=ConversionMassForm()
          context={'form':form,'m_form':measurement_form,'input':True}
          if 'input' in request.POST:
            first=request.POST['measure1']
            second=request.POST['measure2']
            input=request.POST['input']
            answer=''
            if input and int(input)>=0:
              if first =='pound' and second=='kilogram':
                answer=f'{first} yard = {int(input)*0.453592} foot'
              if first =='yard' and second=='foot':
                answer=f'{first} kilogram = {int(input)*2.2062} pound'
            context={
              'form':form,
              'm_form':measurement_form,
              'input':True,
              'answer':answer
            }            
  else:  
    form=COnversionForm()
    context={'form':form,'input':False}
  return render(request,'dashboard/conversion.html',context)    


def register(request):
  if request.method=='POST':
    form=userRegisterationForm(request.POST)
    if form.is_valid():
      form.save()
      username=form.cleaned_data.get('username')
      messages.success(request,f"Account has been created for {username}")
      #redirect to login
  else:    
    form=userRegisterationForm()
  return render(request,"dashboard/register.html",{'form':form})

def profile(request):
  homeworks=Homework.objects.filter(is_finished=False,user=request.user)
  todos=Todo.objects.filter(is_finished=False,user=request.user)
  if len(homeworks)==0:
    homework_done=True
  else:
    homework_done=False
  if len(todos)==0:
    todo_done=True
  else:
    todo_done=False 
  context={'homeworks':homeworks,'todos':todos,'homework_done':homework_done,'todo_done':todo_done}     
  return render(request,'dashboard/profile.html')