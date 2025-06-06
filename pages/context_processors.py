from events.models import RemindMeUpcomingEvent, MarkedAsReadRemindMeNotification
from payments.models import CartPaymentCases,CartPayment
def cart_and_notifications(request):
    # Ensure request and request.user exist
    if not request or not hasattr(request, 'user') or request.user.is_anonymous:
        # Default values for unauthenticated users or missing request
        cart_count = 0
        notification_count = 0
        marked_as_read_notification = 0
    else:
        # Authenticated user logic
        cart = CartPayment.objects.filter(user=request.user).first()
        cart_count = (
            CartPaymentCases.objects.filter(user=cart.user).count()
            if cart
            else 0
        )
        notification= RemindMeUpcomingEvent.objects.filter(
            your_name=request.user, is_passed=False,is_viewed=False
        )
        all_notification_count = notification.count()
        marked_as_read_notification = MarkedAsReadRemindMeNotification.objects.filter(
            user=request.user
        ).count()
       
        notification_count = all_notification_count - marked_as_read_notification 
    
    return {
        'cart_count': cart_count,
        'notification_count': notification_count,
        'marked_as_read_notification': marked_as_read_notification,
    }

