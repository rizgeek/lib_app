from rest_framework.response import Response
from rest_framework import status
from books.models import Copies, CopyStatus
from collections import Counter
from books_transactions.models import Histories, FlagTransaction
from django.contrib.auth.models import User
from books_transactions.api.controller.borrowed import BorrowBook
from lib_users.permissions import IsInGroup


class ReturnedBook :

    def __init__(self) -> None:
        self.borrowed = BorrowBook()

    def returned_books(self, request):
        IsInGroup.check_access(request, self, 'librarian')
        
        copies_ids = request.data.get('copies_ids')
        email = request.data.get('email')
        
        if not copies_ids or not email:
            return self.borrowed._missing_input_response()

        user = self.borrowed._get_user(email)
        if not user:
            return self._user_not_found_response(email)
        
        self._change_status_transactions(user, copies_ids)
        
        return Response({
            'message' : 'book returned successfully'
        }, status=status.HTTP_200_OK)
    

    
    def _change_status_transactions(self, user, copies_ids) :
        objects = Histories.objects.filter(book_copies__in=copies_ids, user=user, status=FlagTransaction.active)

        for obj in objects :
            obj.book_copies.status = CopyStatus.AVAILABLE
            obj.status = FlagTransaction.returned

            obj.book_copies.save()
            obj.save()

