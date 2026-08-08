from fastapi import Query


def get_current_user():
    return {"id": 1, "name": "Habib"}


def get_pagination(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    category: str = Query(default=None),
    search: str = Query(default=None),
):
    return {"page": page, "limit": limit, "category": category, "search": search}
