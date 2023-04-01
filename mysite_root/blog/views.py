from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST

from django.core.mail import send_mail


# Create your views here.
class PostListView(ListView):
    '''
        Alternative to post list view
    '''

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = 'blog/post/list.html'





'''def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 1) # how many posts I want on a single page.
    page_number = request.GET.get('page', 1)# which page I want to get when I go on first page. 
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)#show the first page
    except EmptyPage:
        # If page number is out of range deliever last page of results
        posts = paginator.page(paginator.num_pages)    
    #assert False
    return render(request, 'blog/post/list.html', {'posts':posts})'''


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    # Lists of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    #assert False
    return render(request, 'blog/post/detail.html', {'post':post, 
                                                    'comments': comments,
                                                    'form':form})


def post_share(request, post_id):
    #Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status= Post.Status.PUBLISHED)

    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form field passed validation
            cd = form.cleaned_data
            # .....send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['message']}"
            send_mail(subject, message, 'ahmadfarazjanjua780@gmail.com', [cd['to']])
            sent = True
            #assert False     
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post':post, 
                                                    'form':form,
                                                    'sent':sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    
    comment = None
    # A Comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post 
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',{'post':post,
                                                     'form':form,
                                                     'comment':comment})    
    


# send_mial syntax:
#              It takes the subject, message, sender and list of recipients/receivers as required arguments


# We use request.build_absolute_uri() to build complete URL, including the HTTP schema and hostname


#---------------------------->>>>My confusion and questions<<<<--------------------------------
#---------------------------->>>>>post_share(request, post_id)<<<------------------------------

# Mai soch rha tha k hum post_share view mai:
#                                  post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
# q use kr rhy hain.
# Answer: 
#      1: Ayk to hum ny single post share karni hai to us ki id k liy.
#      2: Hum post ko email k variable send karny k liy kr rhy hian.


# We use:
#       request.build_absolute_uri()
#                to build a complete URL, Including the "HTTP schema" and "hostname".



