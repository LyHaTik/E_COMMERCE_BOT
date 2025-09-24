from shared.db.models import Order


def serialize_order(order: Order):
    return {
        "id": order.id,
        "order_number": order.order_number,
        "user_id": order.user_id,
        "total": order.total,
        "delivery_method": order.delivery_method,
        "status": order.status,
        "contact_name": order.contact_name,
        "contact_phone": order.contact_phone,
        "address": order.address
    }