from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from app.models import Employer, Job_finder, User, Post, Comment, CV, Report, Dashboard, CITY_CHOICES
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from app.form import EUpdateForm, JFUpdateForm, PostForm, CVForm
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from collections import Counter
from django.utils import timezone

# Create your views here.

def base():
    post_list = Post.objects.filter(is_hidden=False)
    cf = Counter([obj.field for obj in post_list]).most_common(3)
    slr = Counter([obj.salary for obj in post_list]).most_common(7)
    ct = Counter([obj.city for obj in post_list]).most_common(6)
    return cf,slr,ct

def home(request):
    user =request.user
    employer = None

    # Check if the user is an employer and has an employer profile
    if user.is_authenticated and hasattr(user, 'employer'):
        employer = user.employer

    # Get all posts and exclude hidden posts of other users
    if employer:
        posts = Post.objects.filter(Q(is_hidden=False) | Q(employer=employer)).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_hidden=False).order_by('-created_at')

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    nums = 'n' * posts.paginator.num_pages
    cf,slr,ct = base()
    context = {'posts': posts, 'nums': nums, 'user': request.user, 'cf': cf, 'slr': slr, 'ct':ct}
    # Check if there is a "not owner" message in the messages
    for message in messages.get_messages(request):
        if message.extra_tags == 'not_owner':
            context['not_owner_message'] = message
    return render(request,'app/home.html',context)

def register_finder(request):
    cf,slr,ct = base()
    if( request.method == "POST" ):
        check = request.POST.get("checkbox", False)
        f_name = request.POST.get("fname")
        gender = request.POST.get("gender")
        name = request.POST.get("uname")
        password = request.POST.get("pass")
        r_password = request.POST.get("rpass")
        date = request.POST.get("inputDate")
        addr = request.POST.get("addr")
        city = request.POST.get("city")
        intro = request.POST.get("intro")

        check_user = User.objects.filter(username=name).exists()
        check_blank = False
        if ' ' in name or ' ' in password:
            check_blank = True

        if check == False:
            messages.error(request, "Please accept the terms")
        elif(password != r_password):
            messages.error(request, 'Passwords must match')
        elif check_user:
            messages.error(request, 'Username existed, please choose another username')
        elif len(name) == 0:
            messages.error(request, 'Username is required')
        elif len(password) == 0:
            messages.error(request, 'Password is required')
        elif check_blank:
            messages.error(request, 'Blanks (\' \') are not allowed in Username or Password')
        elif len(f_name) == 0:
            messages.error(request, 'Please fill in Full name')
        elif gender == 'Choose your Gender':
            messages.error(request, 'Please choose your Gender')
        elif len(addr) == 0:
            messages.error(request, 'Please fill in Address')
        elif city == "Choose your City":
            messages.error(request, 'Please choose your City')
        else:
            user = User.objects.create_user(username=name, password=password)
            user.is_job_finder = True
            user.save()
            jf = Job_finder.objects.create(user=user)
            jf.address = addr
            jf.full_name = f_name
            jf.city = city
            jf.date_of_birth = date
            jf.gender = gender
            jf.introduction = intro
            jf.save()
            return redirect('login')
    context = {'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/user/register_finder.html',context)

def register_company(request):
    cf,slr,ct = base()
    if( request.method == "POST" ):
        check = request.POST.get("checkbox", False)
        c_name = request.POST.get("cname")
        name = request.POST.get("uname")
        password = request.POST.get("pass")
        r_password = request.POST.get("rpass")
        addr = request.POST.get("addr")
        city = request.POST.get("city")
        intro = request.POST.get("intro")

        check_user = User.objects.filter(username=name).exists()
        check_blank = False
        if ' ' in name or ' ' in password:
            check_blank = True

        if check == False:
            messages.error(request, "Please accept the terms")
        elif(password != r_password):
            messages.error(request, 'Passwords must match')
        elif check_user:
            messages.error(request, 'Username existed, please choose another username')
        elif len(name) == 0:
            messages.error(request, 'Username is required')
        elif len(password) == 0:
            messages.error(request, 'Password is required')
        elif check_blank:
            messages.error(request, 'Blanks (\' \') are not allowed in Username or Password')
        elif len(c_name) == 0:
            messages.error(request, 'Please fill in Company Name')
        elif len(addr) == 0:
            messages.error(request, 'Please fill in Address')
        elif city == "Choose your City":
            messages.error(request, 'Please choose your City')
        else:
            user = User.objects.create_user(username=name, password=password)
            user.is_employer = True
            user.save()
            em = Employer.objects.create(user=user)
            em.address = addr
            em.company_name = c_name
            em.city = city
            em.introduction = intro
            em.save()
            return redirect('login')
    context = {'cf': cf, 'slr': slr, 'ct':ct}   
    return render(request,'app/user/register_company.html',context)

def login_user(request):
    cf,slr,ct = base()
    if request.method == "POST":
        uname = request.POST.get("uname")
        password = request.POST.get("pass")
    
        user = authenticate(request, username=uname, password=password)

        if user is not None and user.is_job_finder:
            auth_login(request, user)
            return redirect('home')
        elif user is not None and user.is_employer:
            auth_login(request, user)
            return redirect('home')
        elif user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Username doesn\'t exist or Password is incorrect')
    context = {'cf': cf, 'slr': slr, 'ct':ct}      
    return render(request,'app/user/login.html',context)

@login_required(login_url="/login/")
def profile(request,username):
    cf,slr,ct = base()
    user2 = User.objects.get(username=username) 
    if user2.is_authenticated:
        if user2.is_job_finder:
            if request.method == 'POST':
                action = request.POST.get('pf')
                if action == 'update':
                    u_form = JFUpdateForm(request.POST, instance=user2.job_finder)
                    if u_form.is_valid():
                        u_form.save()
                        messages.success(request, 'Your account has been updated!',extra_tags='update')
                        return redirect('profile', username=username)
                elif action == 'report':
                    Report.objects.create(
                    reporter = request.user,
                    is_user = True,
                    content = request.POST.get('rp_content'),
                    reported_user = user2)
                    u_form = JFUpdateForm(instance=user2.job_finder)
                    messages.success(request, 'Reported user!',extra_tags='report')
            else:
                u_form = JFUpdateForm(instance=user2.job_finder)

            jf = Job_finder.objects.get(user=user2)
            context = {'user2':user2,'jf': jf, 'u_form': u_form, 'cf': cf, 'slr': slr, 'ct':ct, 'city_choices': CITY_CHOICES}
            return render(request, 'app/user/profileJF.html', context)
        
        elif user2.is_employer:
            if request.method == 'POST':
                action = request.POST.get('pf')
                if action == 'update':
                    u_form = EUpdateForm(request.POST, instance=user2.employer)
                    if u_form.is_valid():
                        u_form.save()
                        messages.success(request, 'Your account has been updated!', extra_tags='update')
                        return redirect('profile',username=username)
                elif action == 'report':
                    Report.objects.create(
                    reporter = request.user,
                    is_user = True,
                    content = request.POST.get('rp_content'),
                    reported_user = user2)
                    u_form = EUpdateForm(instance=user2.employer)
                    messages.success(request, 'Reported user!',extra_tags='report')
            else:
                u_form = EUpdateForm(instance=user2.employer)

            em = Employer.objects.get(user=user2)
            context = {'user2':user2,'em': em, 'u_form': u_form, 'cf': cf, 'slr': slr, 'ct':ct, 'city_choices': CITY_CHOICES}
            return render(request, 'app/user/profileE.html', context)
        
    return redirect('home')

def logout_user(request):
    logout(request)

    return redirect('home')

def settings(request):
    cf,slr,ct = base()
    if request.method == 'POST':
        action = request.POST.get('Security')
        
        if action == 'ChangePassword' :
            old_password = request.POST.get('old_pass')
            new_password = request.POST.get('pass')
            confirm_password = request.POST.get('rpass')
           
            u = request.user
    
            user_change = authenticate(request, username=u.username, password=old_password)

            if user_change is not None:
                if len(new_password) == 0:
                    messages.error(request, "New password is required", extra_tags='changepassword')
                elif new_password != confirm_password:
                    messages.error(request, "Passwords must match", extra_tags='changepassword')
                else:
                    user_change.set_password(new_password)
                    user_change.save()
                    auth_login(request, user_change)
                    logout(request)
                    return redirect('login')
            elif user_change is None:
                messages.error(request, "Invalid password", extra_tags='changepassword')

        elif action == 'DeleteAccount': 
            delete_password = request.POST.get('dpass')
            u = request.user

            user_delete = authenticate(request,username=u.username,password = delete_password)

            if user_delete is not None:
                user_delete.delete()
                logout(request)
                return redirect('home')
            elif user_delete is None :
                messages.error(request, "Invalid password", extra_tags='deleteaccount')
    context = {'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/settings.html',context)

@login_required(login_url="/login/") 
def post(request, post_id):
    cf,slr,ct = base()
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    user = request.user
    is_owner = user == post.employer.user if user.is_authenticated else False
    liked_comments = Comment.objects.filter(post=post, likes=user)
    disliked_comments = Comment.objects.filter(post=post, dislikes=user)
    context = {
        'post': post,
        'comments': comments,
        'is_owner': is_owner,
        'liked_comments': liked_comments,
        'disliked_comments': disliked_comments,
        'company_name': post.company_name,
        'job_applied': post.job,
        'cf': cf, 'slr': slr, 'ct':ct
    }   
    post.is_liked = user in post.likes.all()
    post.is_disliked = user in post.dislikes.all()
    

    if request.method == 'POST':
        action = request.POST.get('action') 
        #like/dislike post
        if action == 'like':
            if user in post.likes.all():
                post.likes.remove(user)
                post.is_liked = False
            else:
                post.likes.add(user)
                post.dislikes.remove(user)
                post.is_liked = True
                post.is_disliked = False
            return redirect('post', post_id=post_id)

        elif action == 'dislike':
            if user in post.dislikes.all():
                post.dislikes.remove(user)
                post.is_disliked = False
            else:
                post.dislikes.add(user)
                post.likes.remove(user)
                post.is_disliked = True
                post.is_liked= False
            return redirect('post', post_id=post_id)
        #like/dislike comments

        elif action =='like_comment':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            if user in comment.likes.all():
                comment.likes.remove(user)
            else:
                comment.likes.add(user)
                comment.dislikes.remove(user)

            # Update the liked_comments and disliked_comments after processing the like action
            liked_comments = Comment.objects.filter(post=post, likes=user)
            disliked_comments = Comment.objects.filter(post=post, dislikes=user)

            return redirect('post', post_id=post_id)

        elif action == 'dislike_comment':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            if user in comment.dislikes.all():
                comment.dislikes.remove(user)
            else:
                comment.dislikes.add(user)
                comment.likes.remove(user)

            # Update the liked_comments and disliked_comments after processing the dislike action
            liked_comments = Comment.objects.filter(post=post, likes=user)
            disliked_comments = Comment.objects.filter(post=post, dislikes=user)

            return redirect('post', post_id=post_id)
        # Process comment submission
        elif action == 'comment':
            content = request.POST.get('comment_content')
            comment = Comment(user=request.user, post=post, content=content)
            comment.save()
            return redirect('post', post_id=post_id)
        # Handle hiding and unhiding the post
        elif is_owner and action == 'hide':
            post.is_hidden = True
            post.save()
            return redirect('post', post_id=post_id)

        elif is_owner and action == 'unhide':
            post.is_hidden = False
            post.save()
            return redirect('post', post_id=post_id)
        #Handle delete post
        elif is_owner and action=='delete':
            post.delete()
            return redirect('home')
        elif not is_owner and action == 'report':
           Report.objects.create(
                    reporter = request.user,
                    is_post = True,
                    content = request.POST.get('rp_content'),
                    reported_post = post)
           messages.success(request, 'Reported post!',extra_tags='report_post')
    return render(request, 'app/post/post.html', context)

def publish(request):
    cf,slr,ct = base()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)   
        if form.is_valid():
            form.instance.employer = request.user.employer
            form.instance.introduction=request.user.employer.introduction
            form.instance.city=request.user.employer.city
            form.instance.company_name=request.user.employer.company_name
            form.save()
            messages.success(request, "Post created and published successfully")
            return redirect('home')
        else:
            messages.error(request, "Please complete all information")
    context = {'form':form, 'cf': cf, 'slr': slr, 'ct':ct}
    return render(request, 'app/post/publish.html', context)

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Check if the user is the author of the post
    if request.user != post.employer.user:
        messages.error(request, "You do not have permission to edit this post.", extra_tags='not_owner')
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'app/post/edit_post.html', {'form': form})

def about(request):
    cf,slr,ct = base()
    context = {'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/about.html',context)

def search(request):
    cf,slr,ct = base()
    if request.GET.get('apply') == 'applied':
        messages.error(request,'Sort applied')
    searched = request.GET.get('searched', "")
    check = False
    sort = request.GET.get('sort',"")
    category = request.GET.get('category',"")
    searched_cate = ''


    if any(category == x[0] for x in cf) and sort == 'postdate':
        check = True
        searched_cate = 'Field: ' + category
        posts = Post.objects.filter(Q(field=category) & Q(is_hidden=False)).order_by('-created_at')
        count = Post.objects.filter(Q(field=category) & Q(is_hidden=False)).order_by('-created_at').count()
    elif any(category == x[0] for x in cf):
        searched_cate = 'Field: ' + category
        posts = Post.objects.filter(Q(field=category) & Q(is_hidden=False))
        count = Post.objects.filter(Q(field=category) & Q(is_hidden=False)).count()
    elif any(category == x[0] for x in slr) and sort == 'postdate':
        check = True
        searched_cate = 'Salary: ' + category
        posts = Post.objects.filter(Q(salary=category) & Q(is_hidden=False)).order_by('-created_at')
        count = Post.objects.filter(Q(salary=category) & Q(is_hidden=False)).order_by('-created_at').count()
    elif any(category == x[0] for x in slr):
        searched_cate = 'Salary: ' + category
        posts = Post.objects.filter(Q(salary=category) & Q(is_hidden=False))
        count = Post.objects.filter(Q(salary=category) & Q(is_hidden=False)).count()
    elif any(category == x[0] for x in ct) and sort == 'postdate':
        check = True
        searched_cate = 'City: ' + category
        posts = Post.objects.filter(Q(city=category) & Q(is_hidden=False)).order_by('-created_at')
        count = Post.objects.filter(Q(city=category) & Q(is_hidden=False)).order_by('-created_at').count()
    elif any(category == x[0] for x in ct):
        searched_cate = 'City: ' + category
        posts = Post.objects.filter(Q(city=category) & Q(is_hidden=False))
        count = Post.objects.filter(Q(city=category) & Q(is_hidden=False)).count()
    elif sort == 'postdate':
        check = True
        posts = Post.objects.filter(Q(caption__icontains=searched) & Q(is_hidden=False)).order_by('-created_at')
        count = Post.objects.filter(Q(caption__icontains=searched) & Q(is_hidden=False)).order_by('-created_at').count
    else:
        posts = Post.objects.filter(Q(caption__icontains=searched) & Q(is_hidden=False))
        count = Post.objects.filter(Q(caption__icontains=searched) & Q(is_hidden=False)).count
    p = Paginator(posts, 10)
    page = request.GET.get('page',1)
    try:
        posts = p.page(page)
    except EmptyPage:
        posts = p.page(p.num_pages)
    except:
        posts = p.page(1)
    nums = 'n' * posts.paginator.num_pages
    context = {'searched':searched, 'posts':posts,'nums':nums, 'count':count,'check': check, 'sort': sort, 'category': category,
               'searched_cate': searched_cate, 'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/search.html',context)

def apply(request, post_id):
    cf,slr,ct = base()
    form = CVForm()
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CVForm(request.POST)
        print(request.POST)  # Print the raw form data to check if any fields are missing or incorrect
        if form.is_valid():
            form.instance.finder = request.user.job_finder
            form.instance.full_name = request.user.job_finder.full_name
            form.instance.gender = request.user.job_finder.gender
            form.instance.address = request.user.job_finder.address
            form.instance.date_of_birth = request.user.job_finder.date_of_birth
            form.save()

            form.instance.company_name = post.company_name
            form.instance.job_applied = post.job

            Dashboard.objects.create(
                #E
                employer=post.employer,
                caption=post.caption,
                user_name=request.user.username,
                cv=form.instance,
                status_E='PENDING',
                #JF
                job_finder=request.user.job_finder,
                company_name=post.company_name,
                job_applied=post.job,
                status_JF='PENDING',
                #ALL
                applied_time=timezone.now(),
                deny = post.deny,
                approve = post.approve
            )

            messages.success(request, "CV created successfully")
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request, "Please complete all information")

    context = {
        'job_finder' : request.user.job_finder,
        'form' : form,
        'cf': cf, 'slr': slr, 'ct':ct,
        'post' : post
    }
    return render(request, 'app/post/apply.html', context)

@login_required
def dashboard(request):
    cf,slr,ct = base()
    
    dashboard = Dashboard.objects.filter(employer=request.user.employer)

    dashboard = dashboard.order_by('-highlight', '-applied_time')

    context = {
        'cf': cf, 
        'slr': slr, 
        'ct':ct,
        'dashboard' : dashboard
        }

    return render(request,'app/post/dashboard.html',context)

@login_required(login_url="/login/") 
def history(request):
    cf, slr, ct = base()

    # Retrieve all application history of the current user
    application_history = Dashboard.objects.filter(job_finder=request.user.job_finder)

    context = {
        'cf': cf,
        'slr': slr,
        'ct': ct,
        'application_history': application_history
    }
    return render(request, 'app/post/history.html', context)

@login_required(login_url="/login/") 
def cancel_application(request, application_id):
    application = get_object_or_404(Dashboard, id=application_id)

    # Check if the application status is pending
    if application.status_JF == 'PENDING':
        application.delete()

    return redirect('history')

def view_cv(request, cv_id):
    cf,slr,ct = base()
    cv = get_object_or_404(CV, pk=cv_id)
    dashboard = get_object_or_404(Dashboard, cv=cv_id)
    context = {
        'cf': cf, 
        'slr': slr, 
        'ct':ct,
        'cv' : cv,
        'db' : dashboard
    }
    
    if "deny" in request.POST:
        dashboard.status_E = "DENIED"
        dashboard.status_JF = "DENIED"
        dashboard.save()
        return redirect('dashboard')
    if "approve" in request.POST:
        dashboard.status_E = "ACCEPTED"
        dashboard.status_JF = "ACCEPTED"
        dashboard.save()
        return redirect('dashboard')
    if "highlight" in request.POST:
        dashboard.highlight = not(dashboard.highlight)
        dashboard.save()
        return redirect('dashboard')
    return render(request,'app/post/view_cv.html',context)

def term_of_service(request):
    cf,slr,ct = base()
    context = {'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/term_of_service.html',context)