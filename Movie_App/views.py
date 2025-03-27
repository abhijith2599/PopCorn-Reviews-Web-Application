from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.db.models import Avg,Count

from Movie_App.forms import *
from Movie_App.models import *


# Create your views here.


# def is_login(fn):

#     def wrapper(request,**kwargs):
#         data = Review.objects.filter(movie_id=kwargs.get('pk')).first()

#         if data and data.user_id==request.user:
#             return fn(request,**kwargs)
        
#         else:
#             return redirect('login')
        
#     return wrapper


def is_login(fn):
    def wrapper(request, **kwargs):

        if not request.user.is_authenticated:

            return redirect('login')  # Redirects if user is not logged in

        return fn(request, **kwargs)  # Proceeds normally if logged in

    return wrapper



# class Home_view(View):

#     def get(self,request):

#         return render(request,'index.html')
    

class Logout_view(View):

    def get(self,request):

        logout(request)

        return redirect('userpage')


class Userpage_view(View):

    def get(self,request):

        movie = Movies.objects.all()

        user_reviews = Review.objects.filter(user_id=request.user).select_related('movie_id') if request.user.is_authenticated else []
         # Create a dictionary with user's review details
        review_dict = {i.movie_id.id: i for i in user_reviews} # using dict to make movie id as key and the corresponding review as object
        
        # Create a dictionary with the average rating for each movie
        rating_data = Review.objects.values('movie_id').annotate(avg_rating=Avg('rating'), total_ratings=Count('id'))
        rating_dict = {entry['movie_id']: {'avg': entry['avg_rating'], 'count': entry['total_ratings']} for entry in rating_data}
        
        return render(request,'userpage.html',{'movie':movie,'review_dict':review_dict,'rating_dict':rating_dict}) # if using dict and with instead of user_review add review_dict
    

class  UserRegistration_view(View):

    def get(self,request):

        form = Register_Form

        return render(request,'signup.html',{'form':form})
    
    def post(self,request):

        form = Register_Form(request.POST)  

        if form.is_valid():

            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"User Registration Succesfull, Please LogIn")
            return redirect('userpage')
        
        else:

            return redirect('signup')
        

class Login_view(View):

    def get(self,request):

        form = Login_Form

        return render(request,'login.html',{'form':form})
    
    def post(self,request):

        form = Login_Form(request.POST)

        u_name = request.POST.get('username')
        pswrd = request.POST.get('password')

        user_obj = authenticate(request,username=u_name,password=pswrd)

        if user_obj:

            login(request,user_obj)
            messages.success(request,f'Welcome Great to have you back {request.user.first_name}')
            return redirect('userpage')
        
        else:

            messages.error(request,"Invalid Username and Password")

        return redirect('login')
    

# @method_decorator(decorator=is_login,name="dispatch")
class AddReview_view(View):

    def get(self,request,**kwargs):

        movie = Movies.objects.filter(id = kwargs.get('pk')).first()                                    # first return none if no movie exist, 
                                                                                                        #if not used with filter if no movie exist with the id it is still object, so if not: wont work. Can't use .get() instead of filter()
                                                                                                        # bcz .get() will throw an error if movie not exist, so we use .firts() bcz it return none if not exist not error
        if not movie:
            messages.error(request, "Movie not found!")     
            return redirect('userpage')
        all_reviews = Review.objects.filter(movie_id=movie)                                             # Fetch all reviews for the movie           
        user_review=None  
        form = None                                
                                                                                                        # We check if the movie exists before showing the review form.
                                                                                                        # If the movie doesn’t exist, we redirect the user to another page instead of showing a broken form.
        if request.user.is_authenticated:
            user_review = all_reviews.filter(user_id=request.user).first()                                  # Check if the logged-in user has already reviewed

            form = Review_form(instance=user_review) if user_review else Review_form()                      # Pre-fill form if review exists, else show empty form

        return render(request,'add_review.html',{'form':form,'movie':movie,'all_reviews':all_reviews,'user_review':user_review})
    
    @method_decorator(is_login,name='dispatch')
    def post(self,request,**kwargs):

        m_id = kwargs.get('pk')
        movie = Movies.objects.filter(id = m_id).first()
        if not movie:
            messages.error(request,'Movie not found')
            return redirect('userpage')
                                                                                                        # We check if the movie exists before showing the review form. 
                                                                                                        # If the movie doesn’t exist, we redirect the user to another page instead of showing a broken form.
        # Check if user has already reviewed
        user_review  = Review.objects.filter(user_id=request.user,movie_id=movie).first()
        form = Review_form(request.POST,instance=user_review)                                           # If a review exists, form updates it, else it creates a new review.  This is built into Django forms, which is why we don't need an explicit if-else statement.
                                                                                                        # instance=user_review automatically handles both cases.

        if form.is_valid():

                        # Remove any extra reviews (keeping the latest one)
            # duplicate_reviews = Review.objects.filter(user_id=request.user, movie_id=movie)  #Using movie_id=movie makes it clear that we are filtering using a Movies object instead of just an integer.
            # if duplicate_reviews.count() > 1:
            #     duplicate_reviews[1:].delete()   # Keep the first one, delete others

            # existing_review = duplicate_reviews.first()    
            # if existing_review:
            #     messages.error(request, "You have already reviewed this movie!")
            #     return redirect('userpage')
            
            # Review.objects.create(**form.cleaned_data, user_id=request.user, movie_id=movie)  # If we pass movie_id=movie_id (an integer), Django might accept it, but it's better to use the actual Movies object for clarity.

            review = form.save(commit=False)                                                            #When using ModelForm, calling form.save() automatically saves the form data into the database.
            review.user_id = request.user                                                               #If we don't want to save immediately, we use commit=False. This gives us a Review object, but it is not saved yet.
            review.movie_id = movie                                                                     #This allows us to manually assign values (user_id and movie_id).
            review.save()

            messages.success(request, "Review added successfully!")
            return redirect('userpage')
        
        messages.error(request,'not valid data')
        return render(request, 'add_review.html', {'form': form, 'movie': movie})
    


@method_decorator(decorator=is_login,name="dispatch")
class DeleteReview_view(View):

    def  get(self,request,**kwargs):

        try:
            Review.objects.get(id = kwargs.get('pk'),user_id=request.user).delete()
            messages.success(request,'Review deleted Sucessfully')

        except Review.DoesNotExist:
            messages.error(request,'Review Doesnot exist')

        return redirect('userpage')
    

@method_decorator(decorator=is_login,name="dispatch")
class UpdateReview_view(View):

    def get(self,request,**kwargs):

        review = Review.objects.filter(movie_id=kwargs.get('pk'),user_id=request.user).first()

        if not review:
            messages.error(request, "You haven't reviewed this movie yet.")
            return redirect('userpage')
        
        form = Review_form(instance=review)
        return render(request,'update.html',{'form':form})
    
    def post(self,request,**kwargs):

        review = Review.objects.filter(movie_id=kwargs.get('pk'),user_id=request.user).first()

        if not review:
            messages.error(request, "You haven't reviewed this movie yet.")
            return redirect('userpage')
        
        form = Review_form(request.POST,instance=review)

        if form.is_valid():

            form.save()
            messages.success(request,"Review Updated successfully")
            return redirect('userpage')
        
        messages.error(request,"Error updating review")
        return render(request,'update.html',{'form':form})