from __future__ import annotations

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class DemoModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "demo_models"


def test_base_mixins_define_expected_columns() -> None:
    columns = DemoModel.__table__.columns.keys()

    assert "id" in columns
    assert "created_at" in columns
    assert "updated_at" in columns
