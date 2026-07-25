"""Category model.

Tree-structured category hierarchy using adjacency list
(parent_id self-referencing foreign key).
"""

import uuid

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class Category(db.Model):
    """Test case category (tree node).

    Attributes:
        id: UUID primary key.
        name: Category display name.
        parent_id: FK to parent Category (None for root nodes).
        sort_order: Ordering within siblings.
    """

    __tablename__ = "categories"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name = db.Column(db.String(128), nullable=False)
    parent_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    # Self-referencing tree
    parent = db.relationship(
        "Category",
        remote_side="Category.id",
        backref=db.backref("children", lazy="dynamic"),
    )
    # Cases in this category
    test_cases = db.relationship(
        "TestCase", back_populates="category", lazy="dynamic"
    )

    # ------------------------------------------------------------------
    # Tree helpers
    # ------------------------------------------------------------------

    def to_tree(self) -> dict:
        """Recursively serialize self + children into a nested tree structure.

        Children are sorted by ``sort_order``.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "sort_order": self.sort_order,
            "children": sorted(
                (c.to_tree() for c in self.children),
                key=lambda x: x["sort_order"],
            ),
        }

    def to_dict(self) -> dict:
        """Return a flat JSON-serialisable representation."""
        return {
            "id": str(self.id),
            "name": self.name,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "sort_order": self.sort_order,
        }

    def __repr__(self) -> str:
        return f"<Category {self.name!r}>"
