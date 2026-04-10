from shop.models import Carrier, Setting, Product


class CartService:

    @staticmethod
    def _parse_cart_key(cart_key):
        """'5_3' -> (5, 3)  |  '5' -> (5, None)"""
        parts = str(cart_key).split('_', 1)
        product_id = int(parts[0])
        price_id = int(parts[1]) if len(parts) > 1 and parts[1] else None
        return product_id, price_id

    @staticmethod
    def add_to_cart(request, cart_key, quantity):
        cart = request.session.get("cart", {})
        cart_key = str(cart_key)
        if cart_key in cart:
            cart[cart_key] += quantity
        else:
            cart[cart_key] = quantity
        request.session["cart"] = cart

    @staticmethod
    def remove_from_cart(request, cart_key, quantity):
        cart = request.session.get("cart", {})
        cart_key = str(cart_key)
        if cart_key in cart:
            if cart[cart_key] <= quantity:
                del cart[cart_key]
            else:
                cart[cart_key] -= quantity
        request.session["cart"] = cart

    @staticmethod
    def clear_cart(request):
        request.session.pop("cart", None)

    @staticmethod
    def get_cart_details(request):
        from shop.models.ProductPrice import ProductPrice

        cart = request.session.get("cart", {})
        setting = Setting.objects.first()
        tax_rate = setting.taxe_rate / 100 if setting else 0

        result = {
            "items": [],
            "sub_total": 0,
            "carrier_name": 0,
            "shipping_price": 0,
            "taxe_amount": 0,
            "sub_total_ht": 0,
            "sub_total_ttc": 0,
            "sub_total_with_shipping": 0,
            "cart_count": 0,
        }

        carrier_id = request.session.get("carrier_id")
        carrier = Carrier.objects.filter(id=carrier_id).first() if carrier_id else None

        for cart_key, quantity in cart.items():
            product_id, price_id = CartService._parse_cart_key(cart_key)
            product = Product.objects.filter(id=product_id).first()

            if not product:
                continue

            if price_id:
                pp = ProductPrice.objects.filter(id=price_id, product_id=product_id).first()
                if pp:
                    sale_price = pp.price
                    reg_price = pp.regular_price if pp.regular_price else pp.price
                    price_label = pp.label
                else:
                    sale_price = product.solde_price
                    reg_price = product.regular_price
                    price_label = ''
            else:
                sale_price = product.solde_price
                reg_price = product.regular_price
                price_label = ''

            sub_total_ht = sale_price * quantity
            taxe_amount = sub_total_ht * tax_rate
            sub_total_ttc = sub_total_ht + taxe_amount

            result["items"].append({
                "product": {
                    "id": product.id,
                    "cart_key": cart_key,
                    "slug": product.slug,
                    "name": product.name,
                    "description": product.description,
                    "solde_price": sale_price,
                    "regular_price": reg_price,
                    "price_label": price_label,
                },
                "quantity": quantity,
                "sub_total": round(sub_total_ttc, 2),
                "taxe_amount": round(taxe_amount, 2),
                "sub_total_ht": round(sub_total_ht, 2),
                "sub_total_ttc": round(sub_total_ttc, 2),
            })
            result["sub_total_ht"] += round(sub_total_ht, 2)
            result["cart_count"] += quantity

        result["taxe_amount"] = round(result["sub_total_ht"] * tax_rate, 2)
        result["sub_total_ttc"] = round(result["sub_total_ht"] * (1 + tax_rate), 2)
        result["sub_total"] = result["sub_total_ttc"]

        if carrier:
            result["carrier_id"] = carrier.id
            result["carrier_name"] = carrier.name
            result["shipping_price"] = round(carrier.price, 2)
            result["sub_total_with_shipping"] = round(
                result["sub_total_ttc"] + carrier.price, 2
            )
        else:
            result["sub_total_with_shipping"] = result["sub_total_ttc"]

        return result
