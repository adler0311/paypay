import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.product import Product, ProductSize


def test_create_product(client: TestClient):
    response = client.post("/products/", json={
        "category": "Electronics",
        "price": 1000,
        "cost": 500,
        "name": "Test Product",
        "description": "A test product description",
        "barcode": "123456789",
        "expiration_date": "2023-12-31",
        "size": "small"
    })

    assert response.status_code == 201
    data = response.json()
    assert "id" in data


@pytest.fixture
def a_product(session: Session):
    product_create = {
        "category": "Electronics",
        "price": 1000,
        "cost": 500,
        "name": "Test Product",
        "description": "A test product description",
        "barcode": "123456789",
        "expiration_date": "2023-12-31",
        "size": "SMALL"
    }
    db_product = Product(**product_create)
    session.add(db_product)
    session.commit()
    return db_product

def test_update_product(client: TestClient, session: Session, a_product: Product):
    # given
    product_id = a_product.id

    # when
    response = client.patch(f"/products/{product_id}", json={
        "size": "large"
    })

    # then
    assert response.status_code == 200
    updated_db_product: Product = session.scalar(select(Product).where(Product.id == product_id))
    assert updated_db_product.size == ProductSize.LARGE



def test_delete_product(client: TestClient, session: Session, a_product: Product):
    # given
    product_id = a_product.id

    # when
    response = client.delete(f"/products/{product_id}")

    # then
    assert response.status_code == 200
    deleted_db_product: Product = session.scalar(select(Product).where(Product.id == product_id))
    assert deleted_db_product is None


def test_list_product(client: TestClient, session: Session, a_product: Product):
    # given

    # when
    response = client.get(f"/products")

    # then
    assert response.status_code == 200
    data = response.json()
    print(data)
