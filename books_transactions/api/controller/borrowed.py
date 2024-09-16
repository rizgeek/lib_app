from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from books.models import Copies, CopyStatus
from collections import Counter
from books_transactions.models import Histories, FlagTransaction
from django.contrib.auth.models import User
from lib_users.permissions import IsInGroup


class BorrowBook :

    def borrow_books(self, request):
        IsInGroup.check_access(request, self, 'librarian')

        copies_ids = request.data.get('copies_ids')
        email = request.data.get('email')

        
        if not copies_ids or not email:
            return self._missing_input_response()

        user = self._get_user(email)
        if not user:
            return self._user_not_found_response(email)

        try:
            available_copies, missing_ids = self._check_copies(copies_ids)
            if missing_ids:
                return self._copies_not_available_response(available_copies, missing_ids)

            duplicate_books, duplicate_copies = self._check_duplicate_books(available_copies)
            if duplicate_books:
                return self._duplicate_books_response(duplicate_copies)
            

            if not self._can_borrow_more(user, copies_ids):
                return self._borrowing_limit_exceeded_response()

            self._save_to_histories_and_update_status(available_copies, user)
            return Response({'message': "Borrowed Books success"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return self._error_response(str(e))

    def _missing_input_response(self):
        return Response({'message': 'Please input email and copies ids'}, status=status.HTTP_400_BAD_REQUEST)

    def _get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def _user_not_found_response(self, email):
        return Response({'message': f'User with email: {email} does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _check_copies(self, copies_ids):
        available_copies = Copies.objects.filter(id__in=copies_ids, status=CopyStatus.AVAILABLE)
        available_ids = available_copies.values_list('id', flat=True)
        missing_ids = set(copies_ids) - set(available_ids)
        return available_copies, missing_ids

    def _copies_not_available_response(self, available_copies, missing_ids):
        return Response({
            'success': False,
            'message': 'Some copies are not available.',
            'available_copies': list(available_copies.values()),
            'missing_ids': list(missing_ids)
        }, status=status.HTTP_400_BAD_REQUEST)

    def _check_duplicate_books(self, available_copies):
        book_ids = available_copies.values_list('book_id', flat=True)
        book_count = Counter(book_ids)
        duplicate_books = [book_id for book_id, count in book_count.items() if count > 1]
        duplicate_copies = available_copies.filter(book_id__in=duplicate_books) if duplicate_books else None
        return duplicate_books, duplicate_copies

    def _duplicate_books_response(self, duplicate_copies):
        return Response({
            'success': False,
            'message': 'Some copies belong to the same book.',
            'duplicate_books': list(duplicate_copies.values('id', 'book_id'))
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def _can_borrow_more(self, user, new_copies_ids):
        thirty_days_ago = datetime.now() - timedelta(days=30)

        borrowed_books_count = Histories.objects.filter(
            user=user,
            status=FlagTransaction.active,
            start_date__gte=thirty_days_ago
        ).count()
        return (borrowed_books_count + len(new_copies_ids)) <= 10
    

    def _borrowing_limit_exceeded_response(self):
        return Response({
            'success': False,
            'message': 'You cannot borrow more than 10 books within a 30-day period.'
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def _save_to_histories_and_update_status(self, available_copies, user):
        for copy in available_copies:
            Histories.objects.create(book_copies=copy, user=user)
            copy.status = CopyStatus.NOT_AVAILABLE
            copy.save()

    def _error_response(self, error_message):
        return Response({'message': f'An error occurred: {error_message}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
