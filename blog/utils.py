from blog.db import get_db

def pagination(collection, current_page, pipeline = []):
    page_size = 10
    ctx = {}
    col = get_db(collection)
    skip = (current_page - 1) * page_size
    pagination_pipeline = [
        {"$sort": {"date": -1}},
        {"$skip": skip},
        {"$limit": page_size}
    ]
    pipeline = pagination_pipeline + pipeline
    total_posts = col.count_documents({})
    ctx["rows"] = col.aggregate(pipeline)
    ctx["pages"] = (total_posts + page_size - 1) // page_size
    ctx ["current_page"] = current_page
    return ctx
