from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.views import get_or_create_cart
from cart.models import CartItem
from .models import Order, OrderItem, PaymentTransaction
from loyalty.models import Coupon, PointTransaction
from decimal import Decimal

def checkout_view(request):
    """Trang thanh toán đơn hàng"""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('variant__product', 'variant__color', 'variant__size', 'design', 'print_zone_front', 'print_zone_back').all()
    
    if not items.exists():
        messages.warning(request, "Giỏ hàng của bạn đang trống!")
        return redirect('products:catalog')

    subtotal = cart.get_subtotal()
    shipping_fee = Decimal('30000')

    coupon_code = request.session.get('applied_coupon')
    discount_amount = Decimal('0')
    coupon = None
    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code, is_active=True).first()
        if coupon:
            discount_amount = Decimal(str(coupon.calculate_discount(subtotal)))

    total_amount = max(Decimal('0'), subtotal - discount_amount + shipping_fee)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email', '')
        city = request.POST.get('city', '')
        district = request.POST.get('district', '')
        ward = request.POST.get('ward', '')
        street_address = request.POST.get('street_address', '')
        payment_method = request.POST.get('payment_method', 'COD')
        note = request.POST.get('note', '')

        full_address = f"{street_address}, {ward}, {district}, {city}".strip(', ')

        # Tính điểm thưởng Nếp Club (1 điểm cho mỗi 1.000₫)
        points_earned = int(total_amount // 1000)

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            shipping_address=full_address,
            payment_method=payment_method,
            payment_status='PAID' if payment_method == 'COD' else 'UNPAID',
            order_status='CONFIRMED' if payment_method == 'COD' else 'AWAITING_PAYMENT',
            subtotal=subtotal,
            discount_amount=discount_amount,
            shipping_fee=shipping_fee,
            total_amount=total_amount,
            coupon_code=coupon.code if coupon else '',
            points_earned=points_earned,
            note=note
        )

        # Chuyển các item trong giỏ hàng thành OrderItem
        for item in items:
            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                design=item.design,
                product_name=item.variant.product.name,
                color_name=item.variant.color.name,
                size_name=item.variant.size.name,
                print_zone_front_name=item.print_zone_front.name if item.print_zone_front else '',
                print_zone_back_name=item.print_zone_back.name if item.print_zone_back else '',
                quantity=item.quantity,
                unit_base_price=item.unit_base_price,
                front_print_price=item.front_print_price,
                back_print_price=item.back_print_price,
            )

        # Tích điểm cho thành viên nếu đã đăng nhập
        if request.user.is_authenticated and points_earned > 0:
            request.user.points_balance += points_earned
            request.user.save()
            PointTransaction.objects.create(
                user=request.user,
                points=points_earned,
                transaction_type='EARN',
                description=f"Tích điểm từ đơn hàng #{order.order_code}"
            )

        # Tăng số lượt dùng coupon
        if coupon:
            coupon.used_count += 1
            coupon.save()
            request.session.pop('applied_coupon', None)

        # Xóa giỏ hàng sau khi đặt thành công
        cart.items.all().delete()

        return redirect('orders:success', order_code=order.order_code)

    return render(request, 'orders/checkout.html', {
        'items': items,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'discount_amount': discount_amount,
        'coupon': coupon,
        'total_amount': total_amount,
    })


def order_success_view(request, order_code):
    """Trang xác nhận đặt hàng thành công & hướng dẫn thanh toán"""
    order = get_object_or_404(Order, order_code=order_code)
    return render(request, 'orders/success.html', {
        'order': order,
    })


@login_required
def my_orders_view(request):
    """Xem danh sách đơn hàng đã mua của tài khoản"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'orders/my_orders.html', {
        'orders': orders,
    })
