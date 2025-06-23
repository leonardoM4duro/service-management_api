def materialEntity(db_item) -> dict:
    return {
        "id": str(getattr(db_item, "id", getattr(db_item, "_id", ""))),
        "name": getattr(db_item, "name", None),
        "description": getattr(db_item, "description", None),
        "unit": getattr(db_item, "unit", None),
        "unit_price": getattr(db_item, "unit_price", None),
        "stock_quantity": getattr(db_item, "stock_quantity", None),
        "minimum_stock": getattr(db_item, "minimum_stock", None),
        "category": getattr(db_item, "category", None),
        "code": getattr(db_item, "code", None),
        "created_at": getattr(db_item, "created_at", None),
        "updated_at": getattr(db_item, "updated_at", None),
        "disabled": getattr(db_item, "disabled", False)
    }
    
def list_materialEntity(db_items) -> list:
    return [materialEntity(item) for item in db_items]
