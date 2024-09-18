from django.db import models
from django.contrib.auth.models import User

from book.models import Book





class BorrowBooks(models.Model):
    user=models.ForeignKey(User,related_name='Borrow',on_delete=models.CASCADE)
    
    
    book=models.ForeignKey(Book,related_name='Borrow',on_delete=models.CASCADE)
    borrow_date=models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False) 

    def __str__(self):
        user_name = self.user.first_name if self.user.first_name else self.user.username
        return f"{user_name} borrowed {self.book.book_name}"


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)






