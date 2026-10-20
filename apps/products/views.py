from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .models import Product, ProductType, ProductVariant, Color, Size, SizeChart, PrintZone
from studio.models import DesignTemplate, TemplateCategory

def catalog_view(request):
    """Trang xem mẫu có sẵn / catalog sản phẩm"""
    category_slug = request.GET.get('category')
    type_slug = request.GET.get('type')
    
    templates = DesignTemplate.objects.all().select_related('category')
    if category_slug:
        templates = templates.filter(category__slug=category_slug)
        
    categories = TemplateCategory.objects.all()
    
    # Chỉ lấy các sản phẩm may sẵn (loại trừ các phôi nội bộ dùng riêng cho Studio)
    products_qs = Product.objects.filter(is_active=True, product_type__is_studio_form=False).select_related('product_type')
    if type_slug:
        products = list(products_qs.filter(product_type__slug=type_slug).order_by('-is_featured', 'id'))
    else:
        products = list(products_qs.order_by('product_type__display_order', '-is_featured', 'id'))
        
    product_types = ProductType.objects.filter(is_active=True, is_studio_form=False, products__is_active=True).distinct().order_by('display_order')

    return render(request, 'products/catalog.html', {
        'templates': templates,
        'categories': categories,
        'products': products,
        'product_types': product_types,
        'current_category': category_slug,
        'current_type': type_slug,
    })


def product_detail_view(request, slug):
    """Trang chi tiết sản phẩm đơn"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    colors = Color.objects.filter(productvariant__product=product).distinct()
    if not colors.exists():
        colors = Color.objects.all().order_by('display_order')[:5]

    sizes = Size.objects.filter(productvariant__product=product).distinct()
    if not sizes.exists():
        sizes = Size.objects.all().order_by('display_order')[:5]

    print_zones = PrintZone.objects.filter(product_type=product.product_type)
    
    # Lấy tồn kho mẫu
    variants = product.variants.select_related('color', 'size').all()
    variant_stock_map = {f"{v.color_id}_{v.size_id}": v.stock_quantity for v in variants}

    return render(request, 'products/detail.html', {
        'product': product,
        'colors': colors,
        'sizes': sizes,
        'print_zones': print_zones,
        'variant_stock_map': variant_stock_map,
    })


@require_GET
def calculate_size_api(request):
    """
    API gợi ý kích cỡ áo thông minh dựa trên chiều cao và cân nặng
    Trả về JSON: { suggested_size: 'L', stock_info: 'Màu Đen còn 14 áo size L.', note: '...' }
    """
    try:
        height = float(request.GET.get('height', 0))
        weight = float(request.GET.get('weight', 0))
        product_id = request.GET.get('product_id')
        color_id = request.GET.get('color_id')
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Dữ liệu chiều cao hoặc cân nặng không hợp lệ'}, status=400)

    if height <= 0 or weight <= 0:
        return JsonResponse({'error': 'Vui lòng nhập chiều cao và cân nặng lớn hơn 0'}, status=400)

    # Tìm size phù hợp theo bảng SizeChart
    size_charts = SizeChart.objects.all().select_related('size')
    suggested_size_obj = None
    matched_note = ""

    # Tính điểm match dựa trên khoảng cách min/max
    best_diff = 999999
    for sc in size_charts:
        if (sc.min_height <= height <= sc.max_height) and (sc.min_weight <= weight <= sc.max_weight):
            suggested_size_obj = sc.size
            matched_note = sc.recommendation_note
            break
        else:
            # Thuật toán tính khoảng cách trọng số
            center_h = (sc.min_height + sc.max_height) / 2
            center_w = (sc.min_weight + sc.max_weight) / 2
            diff = abs(height - center_h) * 0.4 + abs(weight - center_w) * 0.6
            if diff < best_diff:
                best_diff = diff
                suggested_size_obj = sc.size
                matched_note = sc.recommendation_note

    size_name = suggested_size_obj.name if suggested_size_obj else "L"

    # Tìm tồn kho của size và màu tương ứng
    stock_text = f"Còn nhiều áo size {size_name}."
    stock_count = 20
    if product_id and color_id:
        variant = ProductVariant.objects.filter(product_id=product_id, color_id=color_id, size__name=size_name).first()
        if variant:
            stock_count = variant.stock_quantity
            color_name = variant.color.name
            stock_text = f"Màu {color_name} còn {stock_count} áo size {size_name}."

    return JsonResponse({
        'suggested_size': size_name,
        'stock_info': stock_text,
        'stock_count': stock_count,
        'note': matched_note or "Gợi ý theo chiều cao và cân nặng trong bảng size tham khảo của Nếp."
    })
