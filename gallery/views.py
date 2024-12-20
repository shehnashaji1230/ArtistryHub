from django.shortcuts import render,redirect,get_object_or_404
from gallery.forms import RegisterForm,SignInForm,ProfileForm,CategoryForm,ArtWorkForm,DiscountForm,ReviewForm
from django.views.generic import View,FormView
from django.contrib.auth import authenticate,login,logout
from .models import UserProfile,Category,ArtWork,Review,WishList

# Create your views here.
class SignUpView(View):
    template_name='register.html'
    form_class=RegisterForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{'form':form_instance})
    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return render(request,self.template_name,{'form':form_instance})
        return render(request,self.template_name,{'form':form_instance})

class SignInView(FormView):
    template_name='signin.html'
    form_class=SignInForm
    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST)
        if form_instance.is_valid():
            uname=form_instance.cleaned_data.get('username')
            pwd=form_instance.cleaned_data.get('password')

            # authenticate
            user_obj=authenticate(username=uname,password=pwd)
            if user_obj:
                login(request,user_obj)
                # redirect based on user_role
                if user_obj.role=='artist':
                    return redirect('artist-dashboard')
                elif user_obj.role=='customer':
                    return redirect('customer-dashboard')
            else:
                return render(request,self.template_name,{'form':form_instance})
        return render(request,self.template_name,{'form':form_instance})




class ArtistDashboardView(View):
    template_name='artist_dashboard.html'
    def get(self,request,*args,**kwargs):
        qs=ArtWork.objects.all()
        return render(request,self.template_name,{"arts":qs})

class CustomerDashboardView(View):
    template_name='customer_dashboard.html'
    def get(self,request,*args,**kwargs):
         categories=Category.objects.all()
         selected_category=request.GET.get('category')
         if selected_category:
             artworks=ArtWork.objects.filter(category_object=selected_category)
         else:
             artworks=ArtWork.objects.all()
         return render(request,self.template_name,{'artworks':artworks,'categories':categories,'selected':selected_category})

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('login')

class ProfileEditView(View):
    template_name='profile-edit.html'
    form_class=ProfileForm
    def get(self,request,*args,**kwargs):
        # get logged in user
        user_profile=request.user.profile
        form_instance=self.form_class(instance=user_profile)
        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
        user_profile=request.user.profile
        form_instance=self.form_class(request.POST,instance=user_profile,files=request.FILES)
        if form_instance.is_valid():
            form_instance.save()

            # redirect to corresponding user dashboard
            
            user_role=user_profile.owner.role
            if user_role=='artist':
                return redirect('artist-dashboard')
            elif user_role=='customer':
                return redirect('customer-dashboard')

class MyProfileView(View):
      template_name="myprofile.html"
      def get(self,request,*args,**kwargs):
      
        qs=UserProfile.objects.filter(owner=request.user)
        return render(request,self.template_name,{"profile":qs})
        

class CategoryView(View):
    form_class=CategoryForm
    template_name='category.html'
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
        form_instance=CategoryForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            Category.objects.create(**data)
            
            return redirect('artist-dashboard')
        return render(request,self.template_name,{'form':form_instance})
        
class ArtWorkCreateView(View):
    template_name='artworkadd.html'
    form_class=ArtWorkForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        print(request.user.role)
        return render(request,self.template_name,{'form':form_instance})
    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST,files=request.FILES)
        if form_instance.is_valid():
            # add owner to form
            form_instance.instance.owner=request.user
            if request.user.role=="artist":
                form_instance.save()
                return redirect('artist-dashboard')
        return render(request,self.template_name,{'form':form_instance})

class MyArtWorkListView(View):
    template_name="myartlist.html"
    def get(self,request,*args,**kwargs):
        qs=ArtWork.objects.filter(owner=request.user)
        return render(request,self.template_name,{'art':qs})

class ArtWorkUpdateView(View):
    template_name='artworkupdate.html'
    form_class=ArtWorkForm
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        art_obj=ArtWork.objects.get(id=id)
        form_instance=self.form_class(instance=art_obj)
        return render(request,self.template_name,{'form':form_instance}) 
    def post(self,request,*args,**kwargs):
        id =kwargs.get('pk')
        art_obj=ArtWork.objects.get(id=id)
        form_instance=self.form_class(request.POST,instance=art_obj,files=request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('artwork-list')
        return render(request,self.template_name,{'form':form_instance}) 

class MyArtWorkDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        ArtWork.objects.get(id=id).delete()
        return redirect('artwork-list')

class Add_DiscountView(View):
    template_name='discount.html'
    form_class=DiscountForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('artist-dashboard')
        return render(request,self.template_name,{'form':form_instance})


# customer functionality

class ArtWorkDetailView(View):
    template_name='artdetail.html'
    
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=ArtWork.objects.get(id=id)
        reviews=Review.objects.filter(art_object=qs).order_by('-date_posted')
        return render(request,self.template_name,{'artworks':qs,'review':reviews})

class ReviewCreateView(View):
    template_name='review.html'
    form_class=ReviewForm
    def get(self,request,*args,**kwargs):
        
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.instance.owner=request.user
            form.save()
            return redirect('customer-dashboard')
        else:
             return render(request,self.template_name,{'form':form})

class AddToWishListView(View):
    def get(self, request, art_id):
        # Get the artwork object
        artwork = get_object_or_404(ArtWork, id=art_id)
        
        # Get or create the user's wishlist
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        
        # Add the artwork to the wishlist if not already added
        if artwork not in wishlist.art_object.all():
            wishlist.art_object.add(artwork)
        
        # Redirect to the artwork detail page after adding
        return redirect('art-detail', pk=art_id)

class CustomerWishListView(View):
    template_name='customer_wishlist.html'
    def get(self,request,*args,**kwargs):

        # fetch user's wishlist
        wishlist=WishList.objects.filter(user=request.user).first()

        # if user has wishlist retrieve artworks
        if wishlist:
            artworks=wishlist.art_object.all()
        else:
            artworks=[]
        return render(request,self.template_name,{'artworks':artworks})