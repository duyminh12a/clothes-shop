from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Address
from studio.models import Design

def login_view(request):
    """Trang đăng nhập"""
    next_url = request.POST.get('next') or request.GET.get('next')

    # Nếu người dùng đã đăng nhập sẵn
    if request.user.is_authenticated:
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        if request.user.is_staff:
            return redirect('admin_panel:products')
        return redirect('accounts:my_designs')

    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=identifier, password=password)
        if not user:
            # Thử tìm theo email
            user_obj = User.objects.filter(email__iexact=identifier).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Chào mừng bạn trở lại, {user.get_full_name() or user.username}!")
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            if user.is_staff:
                return redirect('admin_panel:products')
            return redirect('accounts:my_designs')
        else:
            messages.error(request, "Tên đăng nhập, email hoặc mật khẩu không chính xác.")

    return render(request, 'accounts/login.html', {'next_url': next_url})


def register_view(request):
    """Trang đăng ký thành viên mới"""
    if request.user.is_authenticated:
        return redirect('accounts:my_designs')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        referral_code = request.POST.get('referral_code', '').strip().upper()

        if password != confirm_password:
            messages.error(request, "Mật khẩu xác nhận không khớp.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email này đã được sử dụng.")
            return render(request, 'accounts/register.html')

        # Xử lý người giới thiệu
        referrer = None
        if referral_code:
            referrer = User.objects.filter(referral_code=referral_code).first()

        username = email.split('@')[0]
        # Đảm bảo username là duy nhất
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name,
            phone=phone,
            referred_by=referrer,
            points_balance=50 if referrer else 20  # Tặng 20 điểm chào mừng
        )

        login(request, user)
        messages.success(request, "Đăng ký thành công! Bạn đã nhận được điểm thưởng Nếp Club.")
        return redirect('accounts:my_designs')

    return render(request, 'accounts/register.html')


def logout_view(request):
    """Đăng xuất"""
    logout(request)
    messages.info(request, "Bạn đã đăng xuất tài khoản an toàn.")
    return redirect('/')


@login_required
def my_designs_view(request):
    """Trang 'Thiết kế của tôi' - lưu các mẫu áo đã tạo"""
    designs = Design.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'accounts/my_designs.html', {
        'designs': designs,
    })


@login_required
def profile_view(request):
    """Trang thông tin tài khoản & Nếp Club cá nhân"""
    return render(request, 'accounts/profile.html', {
        'user': request.user,
    })
