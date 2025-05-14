from typing import List
from datetime import datetime
from sqlalchemy import select, text, func

from src.api.dependencies import SessionFactoryDependency
from src.db.tables import PurchasesTable, PurchaseItemsTable
from src.models.purchases import PurchaseCreate, PurchaseModel, PurchaseItemModel

async def create_purchase(
    session_factory: SessionFactoryDependency,
    purchase: PurchaseCreate
) -> PurchaseModel:
    async with session_factory() as session:
        
        result = await session.execute(select(func.max(PurchasesTable.purchase_id)))
        max_id = result.scalar() or 0
        next_id = max_id + 1
        
        
        new_purchase = PurchasesTable(
            purchase_id=next_id,
            customer_id=purchase.customer_id,
            store_id=purchase.store_id,
            purchase_date=datetime.now()
        )
        session.add(new_purchase)
        await session.flush()

        
        result = await session.execute(select(func.max(PurchaseItemsTable.purchase_items_id)))
        max_item_id = result.scalar() or 0
        next_item_id = max_item_id + 1

        
        items = []
        for i, product in enumerate(purchase.products, start=0):
            item = PurchaseItemsTable(
                purchase_items_id=next_item_id + i,
                purchases_id=new_purchase.purchase_id,
                product_id=product.product_id,
                product_count=1,  
                product_price=product.price
            )
            session.add(item)
            items.append(
                PurchaseItemModel(
                    purchase_items_id=next_item_id + i,
                    purchases_id=new_purchase.purchase_id,
                    product_id=product.product_id,
                    product_count=1,
                    product_price=product.price
                )
            )

        await session.commit()

        return PurchaseModel(
            purchase_id=new_purchase.purchase_id,
            customer_id=new_purchase.customer_id,
            store_id=new_purchase.store_id,
            purchase_date=new_purchase.purchase_date,
            items=items
        )

async def get_user_purchases(
    session_factory: SessionFactoryDependency,
    user_id: int
) -> List[PurchaseModel]:
    async with session_factory() as session:
        
        query = select(PurchasesTable).where(PurchasesTable.customer_id == user_id)
        result = await session.execute(query)
        purchases = result.scalars().all()

        
        purchase_models = []
        for purchase in purchases:
            items_query = select(PurchaseItemsTable).where(
                PurchaseItemsTable.purchases_id == purchase.purchase_id
            )
            items_result = await session.execute(items_query)
            items = items_result.scalars().all()

            purchase_models.append(
                PurchaseModel(
                    purchase_id=purchase.purchase_id,
                    customer_id=purchase.customer_id,
                    store_id=purchase.store_id,
                    purchase_date=purchase.purchase_date,
                    items=[
                        PurchaseItemModel(
                            purchase_items_id=item.purchase_items_id,
                            purchases_id=item.purchases_id,
                            product_id=item.product_id,
                            product_count=item.product_count,
                            product_price=item.product_price
                        ) for item in items
                    ]
                )
            )

        return purchase_models 