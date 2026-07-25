"""Category management service.

Handles CRUD operations for the tree-structured category system.
"""

from sqlalchemy.orm import Session as DBSession

from app.models.category import Category
from app.errors import NotFoundError, ValidationError


class CategoryService:
    """Category business logic."""

    def __init__(self, db_session: DBSession):
        self.db = db_session

    def get_tree(self) -> list[dict]:
        """Get the full category tree.

        Returns:
            List of nested dicts representing root categories and their
            children.
        """
        # TODO: Implement get_tree
        #   - Query all categories ordered by sort_order
        #   - Call Category.to_tree(categories)
        #   - Return the nested structure
        raise NotImplementedError

    def create(
        self, name: str, parent_id: str | None = None, sort_order: int = 0
    ) -> Category:
        """Create a new category.

        Args:
            name: Category name.
            parent_id: Parent category UUID (None for root).
            sort_order: Ordering position among siblings.

        Returns:
            Newly created Category instance.

        Raises:
            ValidationError: If name is empty.
            NotFoundError: If parent_id does not exist.
        """
        # TODO: Implement create
        #   - Validate name is not empty
        #   - If parent_id specified, verify parent exists
        #   - Create and return Category
        raise NotImplementedError

    def rename(self, category_id: str, name: str) -> Category:
        """Rename a category.

        Args:
            category_id: Category UUID.
            name: New name.

        Returns:
            Updated Category instance.

        Raises:
            NotFoundError: If the category does not exist.
        """
        # TODO: Implement rename
        #   - Get category (raise NotFound if missing)
        #   - Update name
        #   - Return updated category
        raise NotImplementedError

    def delete(self, category_id: str) -> None:
        """Delete a category and all its descendants.

        Args:
            category_id: Category UUID.

        Raises:
            NotFoundError: If the category does not exist.
        """
        # TODO: Implement delete
        #   - Get category with all descendants
        #   - Delete all (cascade handled by FK or manually)
        #   - db.flush()
        raise NotImplementedError

    def move(
        self, category_id: str, new_parent_id: str | None, sort_order: int = 0
    ) -> Category:
        """Move a category under a new parent.

        Args:
            category_id: Category UUID to move.
            new_parent_id: New parent UUID (None for root).
            sort_order: New ordering position.

        Returns:
            Updated Category instance.

        Raises:
            NotFoundError: If category or new parent does not exist.
            ValidationError: If moving to own descendant.
        """
        # TODO: Implement move
        #   - Get category and potential new parent
        #   - Validate not moving to own descendant
        #   - Update parent_id and sort_order
        #   - Return updated category
        raise NotImplementedError
