from django.shortcuts import render
from .models import MembershipTier, Coupon, PointTransaction

def nep_club_view(request):
    """Trang thông tin chương trình thành viên Nếp Club"""
    tiers = MembershipTier.objects.all().order_by('min_points')
    coupons = Coupon.objects.filter(is_active=True).order_by('-discount_value')
    
    user_points = 0
    current_tier = None
    point_history = []

    if request.user.is_authenticated:
        user_points = request.user.points_balance
        # Tìm hạng hiện tại
        for tier in tiers:
            if user_points >= tier.min_points:
                current_tier = tier
        point_history = PointTransaction.objects.filter(user=request.user).order_by('-created_at')[:10]

    return render(request, 'loyalty/nep_club.html', {
        'tiers': tiers,
        'coupons': coupons,
        'user_points': user_points,
        'current_tier': current_tier,
        'point_history': point_history,
    })
