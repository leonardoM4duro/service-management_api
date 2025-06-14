def clientEntity(db_item) -> dict:
    return {
        "id": str(getattr(db_item, "id", getattr(db_item, "_id", ""))),
        "name": getattr(db_item, "name", None),
        "email": getattr(db_item, "email", None),
        "phone": getattr(db_item, "phone", None),
        "address": getattr(db_item, "address", None),
        "created_at": getattr(db_item, "created_at", None),
        "updated_at": getattr(db_item, "updated_at", None),
        "city": getattr(db_item, "city", None),
        "state": getattr(db_item, "state", None),
        "zip_code": getattr(db_item, "zip_code", None)
    }
    
def list_clientEntity(db_items) -> list:
    return [clientEntity(item) for item in db_items]