from .db import get_db

def pagination(collection, current_page, filters = []):
    page_range_window = 6
    page_size = 10
    ctx = {}
    skip = (current_page - 1) * page_size
    col = get_db(collection)
    posts_count = col.count_documents({})
    total_pages = (posts_count + page_size - 1) // page_size
    left_page = max(1, current_page - page_range_window // 2)
    right_page = min(total_pages, current_page + page_range_window // 2)
    pagination_pipeline = [
        {"$sort": {"date": -1}},
        {"$skip": skip},
        {"$limit": page_size},
        *filters
    ]
    ctx["rows"] = col.aggregate(pagination_pipeline)
    ctx["pages"] = [left_page, right_page]
    ctx["current_page"] = current_page
    ctx["total_pages"] = total_pages
    return ctx
