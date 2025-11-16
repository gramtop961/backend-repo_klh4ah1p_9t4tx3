import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Mousepad, Order

app = FastAPI(title="Mousepad Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Mousepad Store Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected"
            response["collections"] = db.list_collection_names()
        else:
            response["database"] = "❌ Not Connected"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Public catalog endpoints
@app.get("/api/mousepads")
def list_mousepads():
    docs = get_documents("mousepad")
    # Convert ObjectId to str
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return {"items": docs}

@app.post("/api/mousepads", status_code=201)
def create_mousepad(item: Mousepad):
    try:
        new_id = create_document("mousepad", item)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class CreateOrderRequest(Order):
    pass

@app.post("/api/orders", status_code=201)
def create_order(order: CreateOrderRequest):
    try:
        # Basic validation: ensure referenced mousepads exist
        total_calc = 0.0
        for it in order.items:
            if it.quantity <= 0:
                raise HTTPException(status_code=400, detail="Quantity must be >= 1")
            total_calc += it.quantity * it.unit_price
        if abs(total_calc - order.total) > 0.01:
            raise HTTPException(status_code=400, detail="Total does not match sum of items")

        order_id = create_document("order", order)
        return {"id": order_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: seed a few designs if empty
@app.post("/api/seed")
def seed_products():
    try:
        if db["mousepad"].count_documents({}) > 0:
            return {"status": "already-seeded"}
        samples = [
            Mousepad(
                design="Nebula Drift",
                price=39.99,
                description="Vibrant deep-space swirls on a smooth micro‑weave surface.",
                images=[
                    "https://images.unsplash.com/photo-1450849608880-6f787542c88a?q=80&w=1600&auto=format&fit=crop",
                ],
                stock_qty=25,
            ),
            Mousepad(
                design="Midnight Circuit",
                price=39.99,
                description="Minimal cyber lines in electric blue over matte black.",
                images=[
                    "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?q=80&w=1600&auto=format&fit=crop",
                ],
                stock_qty=30,
            ),
            Mousepad(
                design="Sakura Flow",
                price=39.99,
                description="Calming pastel petals flowing across your desk.",
                images=[
                    "https://images.unsplash.com/photo-1497250681960-ef046c08a56e?q=80&w=1600&auto=format&fit=crop",
                ],
                stock_qty=18,
            ),
        ]
        for s in samples:
            create_document("mousepad", s)
        return {"status": "seeded", "count": len(samples)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
