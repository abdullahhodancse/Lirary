
from django.shortcuts import render, redirect
from .forms import  UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .import forms
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404 
from book.models import Book
from .models import BorrowBooks,Account
from django.views.generic import ListView






def singup(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Account Created Successfully')
            form.save()
            print(form.cleaned_data)
            return redirect('user_login')

    else:
         form=UserRegistrationForm()
    return render(request, 'sing_up.html',{'form':form,'type':'login'})

class UserLogInView(LoginView):
    template_name='sing_up.html'
    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self,form):
        messages.success(self.request,'LogIn Successfull')
        return super().form_valid(form) 

    def form_invalid(self,form):
        messages.success(self.request,'LogIn Unsuccessfull')
        return super().form_invalid(form) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type']='Login'  

        return context        

        
def Passwordchange(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"PassWord Updated Successlly")  
            update_session_auth_hash(request,form.user)
            return redirect('profile')  
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'password_change.html',{'form':form}) 

def logout(request):
    auth_logout(request)
    return redirect('user_login')   

def UpdateData(request):
    if request.method=="POST":
        profile_form=forms.UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Profile Data Is Updated SuccessFully!")
            return redirect("profile")
    else:
        profile_form=forms.UserUpdateForm(instance=request.user)
    return render(request,'data_update.html',{'form':profile_form})    

# def Borrow(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     if request.user.is_authenticated:
#         account = get_object_or_404(Account, user=request.user)
        
        

#         if account.balance < book.price:
#             messages.error(request, 'Insufficient balance to borrow this book.')
#             return redirect('profile')

#         # Create a borrow record
#         BorrowBooks.objects.create(user=request.user, book=book)

#         # Update book quantity
#         book.quantity -= 1
#         book.save()

#         # Deduct the price from the user's account
#         account.balance -= book.price
#         account.save()

#         messages.success(request, f'You have successfully borrowed .')
#         return redirect('profile')
#     else:
#         return redirect('login')


class ProfileView(ListView):
    model = BorrowBooks
    template_name = 'profile.html'
    context_object_name = 'Borrow'

    def get_queryset(self):
        return BorrowBooks.objects.filter(user=self.request.user).select_related('book')

def Borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.user.is_authenticated:
        account = get_object_or_404(Account, user=request.user)
        
        # Check if the user has already borrowed this book and not returned it
        existing_borrow = BorrowBooks.objects.filter(user=request.user, book=book, is_returned=False).exists()
        if existing_borrow:
            messages.error(request, 'You have already borrowed this book ')
            return redirect('profile')

        if account.balance < book.price:
            messages.error(request, 'Insufficient balance to borrow this book.')
            return redirect('profile')

        # Create a borrow record
        BorrowBooks.objects.create(user=request.user, book=book)

        # Update book quantity
        book.quantity -= 1
        book.save()

        # Deduct the price from the user's account
        account.balance -= book.price
        account.save()

        messages.success(request, f'You have successfully borrowed the book.')
        return redirect('profile')
    else:
        return redirect('login')


from django.core.exceptions import MultipleObjectsReturned

def ReturnBook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.user.is_authenticated:
        # Get the existing BorrowBooks instance for the current user and book that hasn't been returned yet
        try:
            borrow_instance = BorrowBooks.objects.get(user=request.user, book=book, is_returned=False)
        except BorrowBooks.DoesNotExist:
            messages.error(request, 'This book has already been returned or you have not borrowed it yet.')
            return redirect('profile')

        # Mark the borrow record as returned
        borrow_instance.is_returned = True
        borrow_instance.save()

        # Update book quantity (increase the quantity by 1)
        book.quantity += 1
        book.save()

        messages.success(request, f'You have successfully returned the book.')
        return redirect('profile')
    else:
        return redirect('login')
