from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from products.models import Product, ProductType, Color, Size, PrintZone, ProductVariant
from .models import TemplateCategory, DesignTemplate, StickerCategory, Sticker, Design
import json
import base64
from django.core.files.base import ContentFile

def studio_view(request):
    """Trang công cụ thiết kế áo Nếp Studio"""
    product_types = ProductType.objects.filter(is_active=True).exclude(slug='tui-canvas-tote').prefetch_related('products', 'print_zones').order_by('display_order')
    default_product = Product.objects.filter(is_active=True, slug='ao-custom-classic').first() or Product.objects.filter(is_active=True).first()
    
    colors = Color.objects.all().order_by('display_order')
    sizes = Size.objects.all().order_by('display_order')
    
    # Chuẩn bị danh sách forms data chi tiết cho JavaScript
    forms_list = []
    for pt in product_types:
        prod = pt.products.filter(is_active=True).first()
        if prod:
            pz_list = []
            for pz in pt.print_zones.all().order_by('display_order'):
                pz_list.append({
                    'id': pz.id,
                    'name': pz.name,
                    'dimensions': pz.dimensions,
                    'width': pz.aspect_width,
                    'height': pz.aspect_height,
                    'fee': float(pz.extra_price),
                })
            forms_list.append({
                'id': pt.id,
                'slug': pt.slug,
                'name': pt.name,
                'productId': prod.id,
                'basePrice': float(prod.base_price),
                'fit': prod.fit_type or 'Phối unisex',
                'fabric': prod.fabric_info or 'Cotton tự nhiên',
                'description': pt.description,
                'printZones': pz_list,
            })
            
    sizes_list = []
    for s in sizes:
        sizes_list.append({
            'id': s.id,
            'name': s.name,
            'stock': 25,
        })
    
    # Lấy các khổ in
    print_zones = PrintZone.objects.filter(product_type=default_product.product_type) if default_product else []
    
    # Lấy template & stickers
    template_categories = TemplateCategory.objects.prefetch_related('templates').all()
    sticker_categories = StickerCategory.objects.prefetch_related('stickers').all()

    # Nếu người dùng muốn sửa thiết kế cũ
    design_id = request.GET.get('design_id')
    initial_design = None
    if design_id:
        initial_design = Design.objects.filter(id=design_id).first()

    return render(request, 'studio/index.html', {
        'product_types': product_types,
        'default_product': default_product,
        'colors': colors,
        'sizes': sizes,
        'forms_json': json.dumps(forms_list, ensure_ascii=False),
        'sizes_json': json.dumps(sizes_list, ensure_ascii=False),
        'print_zones': print_zones,
        'template_categories': template_categories,
        'sticker_categories': sticker_categories,
        'initial_design': initial_design,
    })


@require_GET
def get_templates_api(request):
    """API lấy danh sách mẫu thiết kế có sẵn"""
    templates = DesignTemplate.objects.all().select_related('category')
    data = []
    for t in templates:
        data.append({
            'id': t.id,
            'name': t.name,
            'slogan': t.slogan,
            'category': t.category.name,
            'preview_url': t.get_preview(),
            'canvas_json_front': t.canvas_json_front,
            'canvas_json_back': t.canvas_json_back,
            'tags': t.tags,
        })
    return JsonResponse({'templates': data})


@require_GET
def get_stickers_api(request):
    """API lấy danh sách sticker và icon nghệ thuật"""
    stickers = Sticker.objects.all().select_related('category')
    data = []
    for s in stickers:
        data.append({
            'id': s.id,
            'name': s.name,
            'category': s.category.name,
            'image_url': s.get_image_url(),
            'svg_code': s.svg_code,
        })
    return JsonResponse({'stickers': data})


@csrf_exempt
@require_POST
def upload_image_api(request):
    """API tải ảnh từ máy tính người dùng lên để in áo"""
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Không có file ảnh nào được gửi lên'}, status=400)
    
    image_file = request.FILES['image']
    # Giới hạn dung lượng 10MB
    if image_file.size > 10 * 1024 * 1024:
        return JsonResponse({'error': 'File ảnh vượt quá giới hạn 10MB'}, status=400)

    # Đọc ảnh sang base64 data URL để trực tiếp vẽ lên canvas Fabric.js an toàn
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    content_type = image_file.content_type
    data_url = f"data:{content_type};base64,{encoded_string}"

    return JsonResponse({
        'status': 'success',
        'data_url': data_url,
        'filename': image_file.name
    })


@csrf_exempt
@require_POST
def save_design_api(request):
    """API lưu trữ bản thiết kế của người dùng"""
    try:
        body = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'error': 'Dữ liệu JSON không hợp lệ'}, status=400)

    name = body.get('name', 'Chiếc áo của tôi')
    product_id = body.get('product_id')
    color_id = body.get('color_id')
    print_zone_front_id = body.get('print_zone_front_id')
    print_zone_back_id = body.get('print_zone_back_id')
    
    canvas_json_front = json.dumps(body.get('canvas_json_front', {}))
    canvas_json_back = json.dumps(body.get('canvas_json_back', {}))
    preview_front = body.get('preview_front', '')
    preview_back = body.get('preview_back', '')

    product = Product.objects.filter(id=product_id).first() or Product.objects.first()
    color = Color.objects.filter(id=color_id).first()
    pz_front = PrintZone.objects.filter(id=print_zone_front_id).first()
    pz_back = PrintZone.objects.filter(id=print_zone_back_id).first()

    design = Design.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key or '',
        name=name,
        product=product,
        color=color,
        print_zone_front=pz_front,
        print_zone_back=pz_back,
        canvas_json_front=canvas_json_front,
        canvas_json_back=canvas_json_back,
        preview_front=preview_front,
        preview_back=preview_back,
        is_saved=True
    )

    return JsonResponse({
        'status': 'success',
        'design_id': design.id,
        'design_name': design.name,
        'message': 'Đã lưu thiết kế thành công!'
    })
