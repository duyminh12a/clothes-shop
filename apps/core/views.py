from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product, ProductType, Color, Size
from studio.models import DesignTemplate, TemplateCategory
from cms.models import Banner, Review, FAQ, ContactMessage
from loyalty.models import MembershipTier

def home_view(request):
    """Trang chủ Nếp Form chuẩn theo hình mẫu thiết kế"""
    banner = Banner.objects.filter(is_active=True).first()
    
    # Lấy 8 sản phẩm may sẵn nổi bật từ catalog
    featured_products = list(Product.objects.filter(
        is_active=True, 
        is_featured=True, 
        product_type__is_studio_form=False
    ).select_related('product_type').order_by('product_type__display_order', 'id')[:8])
    
    if len(featured_products) < 8:
        existing_ids = [p.id for p in featured_products]
        additional = list(Product.objects.filter(
            is_active=True,
            product_type__is_studio_form=False
        ).exclude(id__in=existing_ids).select_related('product_type').order_by('product_type__display_order', 'id')[:8 - len(featured_products)])
        featured_products.extend(additional)
    
    featured_templates = DesignTemplate.objects.filter(is_featured=True).order_by('id')[:3]
    reviews = Review.objects.filter(is_approved=True)[:4]
    faqs = FAQ.objects.filter(is_active=True)[:4]
    tiers = MembershipTier.objects.all().order_by('min_points')
    
    # Sản phẩm mặc định cho studio widget trang chủ
    default_product = Product.objects.filter(slug="ao-custom-classic").first() or Product.objects.filter(product_type__is_studio_form=True).first() or Product.objects.first()
    colors = Color.objects.all()[:4]

    return render(request, 'home/index.html', {
        'banner': banner,
        'featured_products': featured_products,
        'featured_templates': featured_templates,
        'reviews': reviews,
        'faqs': faqs,
        'tiers': tiers,
        'default_product': default_product,
        'colors': colors,
    })


def about_view(request):
    """Trang Về Nếp - Giới thiệu thương hiệu & xưởng may"""
    return render(request, 'pages/about.html')


def faq_view(request):
    """Trang hỏi đáp thường gặp"""
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'pages/faq.html', {'faqs': faqs})


def contact_view(request):
    """Trang liên hệ và gửi góp ý"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, "Cảm ơn bạn đã nhắn tin cho Nếp! Chúng mình sẽ phản hồi sớm nhất có thể.")
        return redirect('core:contact')

    return render(request, 'pages/contact.html')
