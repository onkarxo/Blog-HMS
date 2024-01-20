from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import BlogPost
from .forms import BlogPostForm


User = get_user_model() 
#SIGNUP PAGE
def SignupPage(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_picture = request.FILES.get('profile_picture')
        user_type = request.POST.get('userType')  # Retrieve user type

        if password1 != password2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            try:
                # Create a user object
                my_user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    profile_picture=profile_picture
                )

                # Set user password
                my_user.set_password(password1)
                my_user.save()  # Save the user

                # Assign user to the selected group (patient or doctor)
                group = Group.objects.get(name=user_type)
                group.user_set.add(my_user)

                return redirect('login')

            except Group.DoesNotExist:
                messages.error(request, 'Group does not exist. Please select a valid group.')
                # Redirect back to signup page or handle the error appropriately
                return redirect('signup')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                # Redirect back to signup page or handle the error appropriately
                return redirect('signup')

    return render(request, 'signup.html')

#LOGIN PAGE
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

#LOGOUT PAGE
def LogoutPage(request):
    logout(request)
    return redirect('login')

#HOME PAGE
@login_required(login_url='login')
def HomePage(request):
    user = request.user

    # Check if the user is in the 'doctor' group
    if user.groups.filter(name='doctor').exists():
        return redirect('doctor_dashboard')

    # Check if the user is in the 'patient' group
    elif user.groups.filter(name='patient').exists():
        return redirect('view_blog_posts')

    # Default behavior (if the user doesn't belong to any known group)
    else:
        context = {'user': user}
        return render(request, 'home.html', context)

#PROFILE PAGE
def profile_page(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)

#DOCTOR HOME 
@login_required(login_url='login')
def doctor_dashboard(request):
    user = request.user
    # Retrieve blog posts for the current doctor
    doctor_posts = BlogPost.objects.filter(author=user)

    context = {'user': user, 'doctor_posts': doctor_posts}
    return render(request, 'doctor_dashboard.html', context)


#PATIENT HOME
@login_required(login_url='login')
def view_blog_posts(request, category=None):
    # Retrieve only published (non-draft) blog posts
    if category:
        blog_posts = BlogPost.objects.filter(is_draft=False, category=category)
    else:
        blog_posts = BlogPost.objects.filter(is_draft=False)

    # Get unique categories for filtering links
    categories = BlogPost.objects.filter(is_draft=False).values_list('category', flat=True).distinct()

    context = {'blog_posts': blog_posts, 'categories': categories}
    return render(request, 'view_blog_posts.html', context)

#CREATING BLOG POST
@login_required(login_url='login')
def create_blog_post(request):
    # Ensure only doctors can create blog posts
    if not request.user.groups.filter(name='doctor').exists():
        return redirect('home')  # Redirect non-doctors to home page

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard after creating post
    else:
        form = BlogPostForm()

    return render(request, 'create_blog_post.html', {'form': form})

#EDITING BLOG POST
@login_required(login_url='login')
def edit_blog_post(request, post_id):
    # Ensure only doctors can edit blog posts
    if not request.user.groups.filter(name='doctor').exists():
        return redirect('home')  # Redirect non-doctors to home page

    blog_post = get_object_or_404(BlogPost, id=post_id)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, 'edit_blog_post.html', {'form': form, 'blog_post': blog_post})

#VIEWING FULL BLOG POST
def full_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    context = {'post': post}
    return render(request, 'full_blog_post.html', context)

