from markdown2 import Markdown
from django.shortcuts import render, redirect
import markdown, random
from . import util



def markdown_to_html(md_file):
    md_content = util.get_entry(md_file)
    markdowner = Markdown()

    if md_content == None:
        return None
    else: 
        return markdowner.convert(md_content)
        

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):

    html_request = markdown_to_html(title)

    if html_request == None:
        return render (request, 'encyclopedia/error.html')
    else:
        
        return render (request, 'encyclopedia/entry.html',{
            "title": title.capitalize(),
            "content": html_request,
        })


def search(request):

    if request.method == "POST":
        searched = request.POST['q']
        html_request = markdown_to_html(searched) 
        
        if html_request is not None:
            return redirect('entry', searched)
    
        else:

            coincidences=[]
            for entries in util.list_entries():
                if searched in entries.lower():
                    coincidences.append(entries.capitalize())

            if len(coincidences) is not 0: 
                return render(request, 'encyclopedia/search.html',{
                "entries": coincidences
                })

            else:
                return render (request, 'encyclopedia/error.html',{
                    'message':'There is no results'
                })

def new_page(request):
    if request.method == "GET":
        return render(request,'encyclopedia/new_page.html')
    else:
        title = request.POST['title']
        content = request.POST['content']

        if title in util.list_entries():
            return render (request, 'encyclopedia/error.html',{
                'message': 'This entry already exists'
            })

        else: 
            util.save_entry(title.capitalize(),content)


            return redirect('entry', title.capitalize())

def edit_page(request,page_title):
    if request.method == "GET":
        content = util.get_entry(page_title)
        return render(request,'encyclopedia/edit.html',{
            'title': page_title,
            'content': content
        })
    elif request.method=="POST":
        title = request.POST['new_title']
        content = request.POST['new_content']

        util.save_entry(title.capitalize(),content)

        return redirect('entry', title.capitalize())


def random_page(request):
    entries = util.list_entries()
    index = random.randint(0, len(entries)-1)

    return redirect('entry', entries[index])