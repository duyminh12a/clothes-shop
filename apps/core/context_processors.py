def global_context(request):
    """
    Cung cấp thông tin giỏ hàng, danh mục sản phẩm và trạng thái toàn site.
    """
    cart_count = 0
    if hasattr(request, 'session'):
        # Nếu có giỏ hàng trong database hoặc session
        from cart.models import Cart
        cart = None
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        elif request.session.session_key:
            cart = Cart.objects.filter(session_key=request.session.session_key).first()
            
        if cart:
            cart_count = cart.items.count()
            
    return {
        'SITE_NAME': 'Nếp Form',
        'SITE_TAGLINE': 'Xưởng áo của bạn',
        'CART_ITEMS_COUNT': cart_count,
    }
