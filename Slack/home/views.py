from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=="POST" :
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")

    return render(request, 'home/contact.html')

# Search Index (Static Content)
SEARCH_INDEX = [
    {
        'title': 'Home',
        'url': '/',
        'content': 'CoLab - Connect. Collaborate. Create. Why CoLab? A platform designed to streamline your workflow and boost productivity. Ready to set sail with CoLab? Join CoLab Today.'
    },
    {
        'title': 'About',
        'url': '/about',
        'content': 'About CoLab. CoLab is a modern collaboration platform designed to bring teams together. Whether you\'re a small startup or a large enterprise, our tools help you stay connected, aligned, and productive.'
    },
    {
        'title': 'Contact',
        'url': '/contact',
        'content': 'Contact Us. Get in touch with our team. Name, Email, Phone, Message. Submit your query.'
    },
    {
        'title': 'Chat',
        'url': '/chat/',
        'content': 'CoLab Chat. Real-time messaging for your teams. Channels, Direct Messages, File Sharing.'
    }
]

def search(request):
    query = request.GET.get('query', '')
    results = []
    
    if query:
        for page in SEARCH_INDEX:
            if query.lower() in page['content'].lower() or query.lower() in page['title'].lower():
                # Simple Highlighting and Snippet extraction
                content = page['content']
                start_index = content.lower().find(query.lower())
                
                # Create a snippet (50 chars before and after)
                start = max(0, start_index - 50)
                end = min(len(content), start_index + 50 + len(query))
                snippet = content[start:end]
                
                # Add ellipsis
                if start > 0: snippet = '...' + snippet
                if end < len(content): snippet = snippet + '...'
                
                # Highlight (Case insensitive replace is tricky, simplistic approach for now or use regex)
                import re
                def replacer(match):
                    return f'<mark>{match.group()}</mark>'
                
                highlighted_snippet = re.sub(re.escape(query), replacer, snippet, flags=re.IGNORECASE)
                
                results.append({
                    'title': page['title'],
                    'url': page['url'],
                    'snippet': highlighted_snippet
                })

    return render(request, 'home/search.html', {'query': query, 'results': results})

def handleSignup(request):
    if request.method == 'POST':
        #Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #CHECK FOR ERRORNEOUS INPUTS
        #Username must be under 10 characters
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        #Username must be AlphaNumeric
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')
        
        #passwords should match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        #Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')
    
def handleLogin(request):
    if request.method == 'POST':
        #Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, please try again")
            return redirect('home')
        
    return HttpResponse('404 - Not Found')
    
def handleLogout(request):
    logout(request) 
    messages.success(request, "Successfully Logged Out")
    return redirect('home')
    
    