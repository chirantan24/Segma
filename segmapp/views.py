from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from segmapp import forms
from django import forms as f
from django.http import HttpResponse, HttpResponseRedirect
from segmapp import models
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,CreateView,DeleteView,ListView,DetailView,UpdateView
from django.utils import timezone
from django.http import Http404
import time
class index(LoginRequiredMixin,ListView):
    login_url='login'
    model=models.Post
    template_name='index.html'
    context_object_name = 'posts'
    paginate_by = 3
    def get_context_data(self,**kwargs):
        context=super(index,self).get_context_data(**kwargs)
        context['b']=self.request.user.is_authenticated
        context['user']=self.request.user
        return context
    def get_queryset(self,*args,**kwargs):
        public=models.Bio.objects.filter(private=False)
        users=[self.request.user]
        for i in public:
            users.append(i.user)
        following=models.Relation.objects.filter(follower=self.request.user)
        for i in following:
            users.append(i.following)
        return models.Post.objects.filter(writer__in=users).order_by('-time_created')
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    template_name='signup.html'
    success_url=reverse_lazy('login')
class CreatePost(LoginRequiredMixin,CreateView):
    login_url='login'
    template_name='createpost.html'
    model=models.Post
    fields=('title','text','file')
    success_url=reverse_lazy('index')

    def get_context_data(self,**kwargs):
        context=super(CreatePost,self).get_context_data(**kwargs)
        context['user']=self.request.user
        return context
    def get_form(self, form_class=None):
        form = super(CreatePost, self).get_form(form_class)
        form.fields['text'].widget = f.Textarea(attrs={"placeholder" : "Enter your text here..","rows" : 8,"cols":50    },);
        form.fields['text'].label='';
        form.fields['title'].widget= f.TextInput(attrs={"placeholder" : "Enter Title Here.."})
        return form
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.writer_id=self.request.user.id;
        self.object.time_created=timezone.now();
        self.object.save()
        return super(CreatePost,self).form_valid(form)
class ListPosts(LoginRequiredMixin,ListView):
    login_url='login'
    model=models.Post
    context_object_name = 'posts'
    paginate_by = 3
    def get_context_data(self,**kwargs):
        context=super(ListPosts,self).get_context_data(**kwargs)
        context['u']=User.objects.get(id=self.kwargs['pk'])
        return context
    def get_queryset(self,*args,**kwargs):
        return models.Post.objects.all().filter(writer=models.User.objects.get(id=self.kwargs['pk'])).order_by('-time_created');
class EditPosts(LoginRequiredMixin,UpdateView):
    login_url='login'
    model=models.Post
    template_name='createpost.html'
    form_class=forms.PostEditForm
    success_url=reverse_lazy('index')
    def get_context_data(self,**kwargs):
        context=super(EditPosts,self).get_context_data(**kwargs)
        if context['object'].writer == self.request.user:
            return context
        else:
            raise Http404

class DetailPosts(LoginRequiredMixin,DetailView):
    login_url='login'
    model=models.Post
    def get_context_data(self,**kwargs):
        context=super(DetailPosts,self).get_context_data(**kwargs)
        f=models.Relation.objects.filter(follower=self.request.user,following=context['object'].writer).count()
        if context['object'].writer == self.request.user or f:
            return context
        else:
            raise Http404
class PostsDelete(LoginRequiredMixin,DeleteView):
    model=models.Post;
    login_url='login'
    success_url=reverse_lazy('index')
    def get_context_data(self,**kwargs):
        context=super(PostsDelete,self).get_context_data(**kwargs)
        print (context)
        if context['object'].writer == self.request.user:
            return context
        else:
            raise Http404
def comment(request,slug):
    if not request.user.is_authenticated:
        return reverse_lazy('login')
    post=get_object_or_404(models.Post,id=slug)
    if post.writer!=request.user :
        raise Http404;
    if request.method == "POST":
        c=forms.CommentForm(data=request.POST)

        if c.is_valid() :
            temp=c.save()
            temp.commenter=request.user
            temp.time_created=timezone.now()
            temp.post=post
            temp.save()
            c=forms.CommentForm()
            # return reverse_lazy('app:comment',kwargs={'slug':post.id})
    else:
        c=forms.CommentForm()
    return render(request,'segmapp/comment.html',context={'form':c,'user':request.user,'post':post,'object':post,'b':True,'l':True})
class DeleteComment(LoginRequiredMixin,DeleteView):
    model=models.Comment
    login_url='login'
    def get_success_url(self):
        obj=super(DeleteComment,self).get_object().post
        return reverse_lazy('app:comment',kwargs={'slug':obj.pk})
    def get_context_data(self,**kwargs):
        context=super(DeleteComment,self).get_context_data(**kwargs)
        if context['object'].post.writer == self.request.user or context['object'].commenter==self.request.user:
            return context
        else:
            raise Http404

class SearchResults(LoginRequiredMixin,ListView):
    model=User
    login_url='login'
    paginate_by =4
    template_name='search_results.html'
    def get_context_data(self,**kwargs):
        context=super(SearchResults,self).get_context_data(**kwargs)
        context['s']=self.request.GET.get('s');
        return context;
    def get_queryset(self):
        s=self.request.GET.get('s')
        return User.objects.filter(username__icontains=s)
class UserDetail(LoginRequiredMixin,DetailView):
    model=User
    login_url='login'
    template_name='user_detail.html'
    def get_context_data(self,**kwargs):
        context=super(UserDetail,self).get_context_data(**kwargs)
        b=models.Relation.objects.filter(follower=context['object']).count()
        a=models.Relation.objects.filter(following=context['object']).count()
        context['following']=b
        context['followers']=a
        return context
def follow(request,pk):
    following=User.objects.get(id=pk)
    follower=request.user
    t=models.Request(to=following,by=follower)
    t.save()
    return render(request,'index.html')
class RequestList(LoginRequiredMixin,ListView):
    model=models.Request
    paginate_by =4
    login_url='login'
    def get_queryset(self):
        user=self.request.user
        return models.Request.objects.filter(to__exact=user)
def accept(request,pk):
    r=models.Request.objects.get(id=pk)
    follower=r.by
    following=r.to
    t=models.Relation(follower=follower,following=following)
    t.save()
    r.delete()
    return render(request,'index.html')
class RequestDetail(LoginRequiredMixin,DetailView):
    model=models.Request
    login_url='login'
    template_name='segmapp/accept_request.html'
    def get_context_data(self,**kwargs):
        context=super(RequestDetail,self).get_context_data(**kwargs)
        b=models.Relation.objects.filter(follower=context['object'].by).count()
        a=models.Relation.objects.filter(following=context['object'].by).count()
        context['following']=b
        context['followers']=a
        context['u']=context['object'].by
        return context
class Followerlist(LoginRequiredMixin,ListView):
    model=models.Relation
    login_url='login'
    template_name='segmapp/followerlist.html'
    paginate_by =4
    def get_queryset(self):
        return models.Relation.objects.filter(following=self.kwargs['pk'])

class Followinglist(LoginRequiredMixin,ListView):
    model=models.Relation
    login_url='login'
    template_name='segmapp/followinglist.html'
    paginate_by =4
    def get_queryset(self):
        return models.Relation.objects.filter(follower=self.kwargs['pk'])

class make_bio(LoginRequiredMixin,CreateView):
    model=models.Bio
    login_url='login'
    template_name='segmapp/bio_create.html'
    success_url=reverse_lazy('index')
    form_class=forms.BioForm
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user;
        self.object.save()
        return super(make_bio,self).form_valid(form)
class update_bio(LoginRequiredMixin,UpdateView):
    model=models.Bio
    login_url='login'
    template_name='segmapp/bio_create.html'
    success_url=reverse_lazy('index')
    form_class=forms.BioForm
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user;
        self.object.save()
        return super(make_bio,self).form_valid(form)
class BioDetail(LoginRequiredMixin,DetailView):
    model=models.Bio
    login_url='login'
    template_name='user_detail.html'
    def get_context_data(self,**kwargs):
        context=super(BioDetail,self).get_context_data(**kwargs)
        context['followers']=models.Relation.objects.filter(following=context['object'].user).count()
        context['following']=models.Relation.objects.filter(follower=context['object'].user).count()
        context['f']=models.Relation.objects.filter(following=context['object'].user,follower=self.request.user).count()
        context['u']=context['object'].user
        context['user']=self.request.user
        return context
def reject(request,pk):
    r=models.Request.objects.get(id=pk)
    r.delete()
    return render(request,'index.html')
