from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from products.models import Product, ProductVariant, Color, Size, ProductType, PrintZone, SizeChart
from orders.models import Order, OrderItem
from loyalty.models import Coupon, MembershipTier, PointTransaction
from studio.models import DesignTemplate, TemplateCategory, Sticker
from cms.models import Banner, Review, ContactMessage
from accounts.models import User
from decimal import Decimal
import json

def staff_required(view_func):
    """Yêu cầu người dùng là nhân viên quản trị (is_staff)"""
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/tai-khoan/dang-nhap/'
    )(view_func)
    return decorated_view_func


@staff_required
def dashboard_overview(request):
    """Trang tổng quan KPI, thống kê & đơn hàng gần nhất"""
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(order_status='PENDING').count()
    processing_orders = Order.objects.filter(order_status='PROCESSING').count()
    completed_orders = Order.objects.filter(order_status='COMPLETED').count()
    
    total_revenue = Order.objects.filter(order_status__in=['CONFIRMED', 'PROCESSING', 'SHIPPING', 'COMPLETED']).aggregate(s=Sum('total_amount'))['s'] or 0
    total_users = User.objects.count()
    total_products = Product.objects.count()

    recent_orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')[:8]
    low_stock_variants = ProductVariant.objects.select_related('product', 'color', 'size').filter(stock_quantity__lte=15).order_by('stock_quantity')[:6]

    return render(request, 'admin_panel/overview.html', {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_products': total_products,
        'recent_orders': recent_orders,
        'low_stock_variants': low_stock_variants,
        'active_menu': 'overview',
    })


@staff_required
def order_list_view(request):
    """Danh sách & quản lý đơn hàng"""
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q', '').strip()

    orders = Order.objects.prefetch_related('items').order_by('-created_at')
    if status_filter:
        orders = orders.filter(order_status=status_filter)
    if search_query:
        orders = orders.filter(
            Q(order_code__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(customer_phone__icontains=search_query)
        )

    status_choices = Order.STATUS_CHOICES

    return render(request, 'admin_panel/orders.html', {
        'orders': orders,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': status_choices,
        'active_menu': 'orders',
    })


@staff_required
def order_detail_view(request, order_code):
    """Chi tiết đơn hàng, duyệt trạng thái và xuất file in"""
    order = get_object_or_404(Order.objects.prefetch_related('items__design'), order_code=order_code)

    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        new_payment_status = request.POST.get('payment_status')
        if new_status:
            order.order_status = new_status
        if new_payment_status:
            order.payment_status = new_payment_status
        order.save()
        messages.success(request, f"Đã cập nhật trạng thái đơn #{order.order_code} thành công!")
        return redirect('admin_panel:order_detail', order_code=order.order_code)

    return render(request, 'admin_panel/order_detail.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
        'payment_status_choices': Order.PAYMENT_STATUS_CHOICES,
        'active_menu': 'orders',
    })


@staff_required
def product_list_view(request):
    """Quản lý sản phẩm & biến thể: tìm kiếm, lọc danh mục, chỉnh sửa, xóa"""
    q = request.GET.get('q', '').strip()
    type_slug = request.GET.get('type', '').strip()
    status = request.GET.get('status', '').strip()

    products_qs = Product.objects.select_related('product_type').prefetch_related('variants__color', 'variants__size').all()

    if q:
        products_qs = products_qs.filter(
            Q(name__icontains=q) |
            Q(fabric_info__icontains=q) |
            Q(fit_type__icontains=q) |
            Q(badge__icontains=q) |
            Q(description__icontains=q)
        )

    if type_slug:
        products_qs = products_qs.filter(product_type__slug=type_slug)

    if status == 'active':
        products_qs = products_qs.filter(is_active=True)
    elif status == 'inactive':
        products_qs = products_qs.filter(is_active=False)

    products = products_qs.order_by('-is_featured', 'product_type__display_order', '-created_at')

    # Thống kê nhanh số lượng
    total_count = Product.objects.count()
    active_count = Product.objects.filter(is_active=True).count()
    inactive_count = Product.objects.filter(is_active=False).count()
    featured_count = Product.objects.filter(is_featured=True).count()

    product_types = ProductType.objects.filter(is_active=True).order_by('display_order')

    return render(request, 'admin_panel/products.html', {
        'products': products,
        'product_types': product_types,
        'current_q': q,
        'current_type': type_slug,
        'current_status': status,
        'total_count': total_count,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'featured_count': featured_count,
        'active_menu': 'products',
    })


@staff_required
def product_create_view(request):
    """Thêm sản phẩm mới vào danh mục Trang phục & Phôi may sẵn"""
    product_types = ProductType.objects.filter(is_active=True).order_by('display_order')
    colors = Color.objects.all().order_by('display_order')
    sizes = Size.objects.all().order_by('display_order')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        product_type_id = request.POST.get('product_type')
        base_price = Decimal(request.POST.get('base_price', 250000))
        badge = request.POST.get('badge', '').strip()
        color_hex = request.POST.get('color_hex', '#F5F0E8').strip()
        thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        fabric_info = request.POST.get('fabric_info', 'Cotton 100% (240gsm)').strip()
        fit_type = request.POST.get('fit_type', 'Phối unisex').strip()
        description = request.POST.get('description', '').strip()
        is_featured = 'is_featured' in request.POST
        is_active = 'is_active' in request.POST

        ptype = get_object_or_404(ProductType, id=product_type_id)
        product = Product(
            name=name,
            product_type=ptype,
            base_price=base_price,
            badge=badge,
            color_hex=color_hex,
            thumbnail_url=thumbnail_url,
            fabric_info=fabric_info,
            fit_type=fit_type,
            description=description,
            is_featured=is_featured,
            is_active=is_active,
        )

        if 'thumbnail_image' in request.FILES:
            product.thumbnail_image = request.FILES['thumbnail_image']

        product.save()

        # Tự động tạo biến thể mặc định cho các size
        default_color = Color.objects.filter(hex_code__iexact=color_hex).first() or Color.objects.first()
        for s in sizes:
            ProductVariant.objects.get_or_create(
                product=product,
                color=default_color,
                size=s,
                defaults={'stock_quantity': 30}
            )

        messages.success(request, f"Đã thêm sản phẩm '{product.name}' thành công!")
        return redirect('admin_panel:products')

    return render(request, 'admin_panel/product_form.html', {
        'product_types': product_types,
        'colors': colors,
        'sizes': sizes,
        'is_edit': False,
        'active_menu': 'products',
    })


@staff_required
def product_edit_view(request, product_id):
    """Chỉnh sửa thông tin sản phẩm: hình ảnh, giá, mô tả, chất liệu, huy hiệu, trạng thái"""
    product = get_object_or_404(Product, id=product_id)
    product_types = ProductType.objects.filter(is_active=True).order_by('display_order')

    if request.method == 'POST':
        product.name = request.POST.get('name', '').strip()
        product_type_id = request.POST.get('product_type')
        if product_type_id:
            product.product_type = get_object_or_404(ProductType, id=product_type_id)
        product.base_price = Decimal(request.POST.get('base_price', product.base_price))
        product.badge = request.POST.get('badge', '').strip()
        product.color_hex = request.POST.get('color_hex', product.color_hex).strip()
        product.thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        product.fabric_info = request.POST.get('fabric_info', '').strip()
        product.fit_type = request.POST.get('fit_type', '').strip()
        product.description = request.POST.get('description', '').strip()
        product.is_featured = 'is_featured' in request.POST
        product.is_active = 'is_active' in request.POST

        if 'thumbnail_image' in request.FILES:
            product.thumbnail_image = request.FILES['thumbnail_image']

        product.save()

        messages.success(request, f"Đã cập nhật sản phẩm '{product.name}' thành công!")
        return redirect('admin_panel:products')

    return render(request, 'admin_panel/product_form.html', {
        'product': product,
        'product_types': product_types,
        'is_edit': True,
        'active_menu': 'products',
    })


@staff_required
def product_delete_view(request, product_id):
    """Xóa sản phẩm khỏi hệ thống"""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Đã xóa sản phẩm '{product_name}' thành công!")
        return redirect('admin_panel:products')

    return redirect('admin_panel:products')


@staff_required
def product_toggle_active_api(request, product_id):
    """Bật/tắt trạng thái hiển thị (Đang bán / Đã ẩn) nhanh qua AJAX"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.is_active = not product.is_active
        product.save(update_fields=['is_active'])
        return JsonResponse({
            'status': 'success',
            'is_active': product.is_active,
            'message': f"Đã {'hiện' if product.is_active else 'ẩn'} sản phẩm '{product.name}'"
        })
    return JsonResponse({'error': 'Invalid method'}, status=405)


@staff_required
def quick_update_stock_api(request):
    """API cập nhật nhanh số lượng tồn kho variant"""
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            variant_id = body.get('variant_id')
            new_stock = int(body.get('stock', 0))
            variant = ProductVariant.objects.get(id=variant_id)
            variant.stock_quantity = max(0, new_stock)
            variant.save()
            return JsonResponse({'status': 'success', 'stock': variant.stock_quantity})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)


@staff_required
def coupon_list_view(request):
    """Quản lý mã giảm giá"""
    coupons = Coupon.objects.all().order_by('-created_at')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        discount_type = request.POST.get('discount_type', 'PERCENT')
        discount_value = Decimal(request.POST.get('discount_value', 10))
        min_order = Decimal(request.POST.get('min_order_amount', 0))
        max_uses = int(request.POST.get('max_uses', 100))

        if Coupon.objects.filter(code=code).exists():
            messages.error(request, f"Mã '{code}' đã tồn tại!")
        else:
            Coupon.objects.create(
                code=code,
                discount_type=discount_type,
                discount_value=discount_value,
                min_order_amount=min_order,
                max_uses=max_uses,
                is_active=True
            )
            messages.success(request, f"Đã tạo mã giảm giá '{code}' thành công!")
            return redirect('admin_panel:coupons')

    return render(request, 'admin_panel/coupons.html', {
        'coupons': coupons,
        'active_menu': 'coupons',
    })


@staff_required
def templates_list_view(request):
    """Quản lý kho mẫu thiết kế Studio"""
    templates = DesignTemplate.objects.select_related('category').all().order_by('-created_at')
    categories = TemplateCategory.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        slogan = request.POST.get('slogan', '')
        category_id = request.POST.get('category_id')
        tags = request.POST.get('tags', '')
        
        category = get_object_or_404(TemplateCategory, id=category_id)
        DesignTemplate.objects.create(
            name=name,
            slogan=slogan,
            category=category,
            tags=tags,
            is_featured=True
        )
        messages.success(request, f"Đã thêm mẫu thiết kế '{name}' vào Studio!")
        return redirect('admin_panel:templates')

    return render(request, 'admin_panel/templates.html', {
        'templates': templates,
        'categories': categories,
        'active_menu': 'templates',
    })


@staff_required
def settings_view(request):
    """Cài đặt thông tin cửa hàng, banners và FAQs"""
    banners = Banner.objects.all().order_by('display_order')
    faqs = FAQ.objects.all().order_by('display_order')
    messages_list = ContactMessage.objects.all().order_by('-created_at')[:10]

    return render(request, 'admin_panel/settings.html', {
        'banners': banners,
        'faqs': faqs,
        'messages_list': messages_list,
        'active_menu': 'settings',
    })
