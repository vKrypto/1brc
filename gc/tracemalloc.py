from fastapi import FastAPI
import tracemalloc

app = FastAPI()

# Start tracemalloc
tracemalloc.start()

@app.get("/memory-snapshot")
async def memory_snapshot(top: int = 10):
    """
    Returns the top memory allocations in the application.
    Parameters:
    - top (int): Number of top memory-consuming lines to return.
    """
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    # Format the response
    response = {
        "total_allocated_memory": f"{snapshot.statistics('lineno')[0].size / 1024:.2f} KB",
        "top_allocations": [
            {
                "file": stat.traceback[0].filename,
                "line": stat.traceback[0].lineno,
                "size_kb": stat.size / 1024,
                "count": stat.count,
            }
            for stat in top_stats[:top]
        ],
    }

    return response
