from suppliers.models import Suppliers
import pytest

@pytest.mark.django_db
class TestModels:
    
    def teste_suppliers(self):
        name = "Supplier teste"
        new_supplier = Suppliers.objects.create(
            name=name
        )

        assert new_supplier.name == name
        assert new_supplier.created_at is not None
        assert new_supplier.updated_at is not None