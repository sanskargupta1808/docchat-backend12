from fastapi import APIRouter

router = APIRouter()

# Simulated in-memory store
query_log = {}

@router.get("/analytics/queries")
def get_most_common_queries():
    # Simulate top queries
    return {
        "top_queries": sorted(query_log.items(), key=lambda x: x[1], reverse=True)[:5]
    }