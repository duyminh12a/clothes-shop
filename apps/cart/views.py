from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .models import Cart, CartItem
from products.models import ProductVariant, PrintZone, Product
from studio.models import Design
from loyalty.models import Coupon
import json

def get_or_create_cart(request):
    """Lấy hoặc tạo mới giỏ hàng theo User hoặc Session"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_detail_view(request):
    """Trang xem giỏ hàng"""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('variant__product', 'variant__color', 'variant__size', 'design', 'print_zone_front', 'print_zone_back').all()
    
    subtotal = cart.get_subtotal()
    shipping_fee = 30000 if subtotal > 0 else 0
    
    # Kiểm tra coupon nếu có lưu trong session
    coupon_code = request.session.get('applied_coupon')
    discount_amount = 0
    coupon = None
    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code, is_active=True).first()
        if coupon:
            discount_amount = coupon.calculate_discount(subtotal)
            
    total = max(0, subtotal - discount_amount + shipping_fee)

    return render(request, 'cart/detail.html', {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'discount_amount': discount_amount,
        'coupon': coupon,
        'total': total,
    })


@csrf_exempt
@require_POST
def add_to_cart_api(request):
    """API thêm áo vào giỏ hàng (kèm hoặc không kèm thiết kế)"""
    cart = get_or_create_cart(request)
    
    try:
        body = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'error': 'JSON không hợp lệ'}, status=400)

    product_id = body.get('product_id')
    color_id = body.get('color_id')
    size_id = body.get('size_id')
    quantity = int(body.get('quantity', 1))
    design_id = body.get('design_id')
    print_zone_front_id = body.get('print_zone_front_id')
    print_zone_back_id = body.get('print_zone_back_id')

    product = Product.objects.filter(id=product_id).first()
    if not product:
        product = Product.objects.filter(product_type_id=product_id).first()
    if not product:
        product = Product.objects.first()

    # Tìm variant phù hợp
    variant = ProductVariant.objects.filter(product=product, color_id=color_id, size_id=size_id).first()
    if not variant:
        variant = ProductVariant.objects.filter(product=product).first()
        if not variant:
            return JsonResponse({'error': 'Sản phẩm hoặc biến thể không tồn tại'}, status=404)

    design = Design.objects.filter(id=design_id).first() if design_id else None
    pz_front = PrintZone.objects.filter(id=print_zone_front_id).first()
    pz_back = PrintZone.objects.filter(id=print_zone_back_id).first()

    # Tạo hoặc tăng số lượng cart item
    cart_item = CartItem.objects.create(
        cart=cart,
        variant=variant,
        design=design,
        quantity=quantity,
        print_zone_front=pz_front,
        print_zone_back=pz_back,
        unit_base_price=variant.get_price(),
        front_print_price=pz_front.extra_price if pz_front else 0,
        back_print_price=pz_back.extra_price if pz_back else 0,
    )

    return JsonResponse({
        'status': 'success',
        'cart_count': cart.get_total_items(),
        'message': f'Đã thêm {variant.product.name} ({variant.color.name}, Size {variant.size.name}) vào giỏ hàng!'
    })


@csrf_exempt
@require_POST
def update_cart_item_api(request, item_id):
    """Cập nhật số lượng món trong giỏ"""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    try:
        body = json.loads(request.body.decode('utf-8'))
        qty = int(body.get('quantity', 1))
        if qty <= 0:
            item.delete()
        else:
            item.quantity = qty
            item.save()
    except Exception:
        return JsonResponse({'error': 'Dữ liệu không hợp lệ'}, status=400)

    return JsonResponse({
        'status': 'success',
        'item_total': item.get_total_price() if item.id else 0,
        'subtotal': cart.get_subtotal(),
        'cart_count': cart.get_total_items(),
    })


@csrf_exempt
@require_POST
def remove_cart_item_api(request, item_id):
    """Xóa món khỏi giỏ hàng"""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    
    return JsonResponse({
        'status': 'success',
        'subtotal': cart.get_subtotal(),
        'cart_count': cart.get_total_items(),
        'message': 'Đã xóa sản phẩm khỏi giỏ hàng'
    })


@csrf_exempt
@require_POST
def apply_coupon_api(request):
    """Áp dụng mã giảm giá"""
    try:
        body = json.loads(request.body.decode('utf-8'))
        code = body.get('code', '').strip().upper()
    except Exception:
        return JsonResponse({'error': 'Dữ liệu không hợp lệ'}, status=400)

    cart = get_or_create_cart(request)
    subtotal = cart.get_subtotal()

    coupon = Coupon.objects.filter(code=code, is_active=True).first()
    if not coupon:
        return JsonResponse({'error': 'Mã giảm giá không tồn tại hoặc đã hết hạn'}, status=400)

    if subtotal < coupon.min_order_amount:
        return JsonResponse({'error': f'Mã này chỉ áp dụng cho đơn từ {coupon.min_order_amount:,.0f}₫'}, status=400)

    discount = coupon.calculate_discount(subtotal)
    request.session['applied_coupon'] = code

    return JsonResponse({
        'status': 'success',
        'discount_amount': discount,
        'code': coupon.code,
        'message': f'Áp dụng thành công mã {coupon.code} (-{discount:,.0f}₫)'
    })
