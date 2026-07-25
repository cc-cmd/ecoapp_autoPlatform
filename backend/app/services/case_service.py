"""Test case management service.

Handles CRUD operations for test cases and their associated scripts.
"""

from sqlalchemy.orm import Session as DBSession

from app.models.test_case import TestCase
from app.errors import NotFoundError, ValidationError


class CaseService:
    """Test case business logic."""

    def __init__(self, db_session: DBSession):
        self.db = db_session

    def list_cases(
        self,
        page: int = 1,
        size: int = 20,
        search: str | None = None,
        category_id: str | None = None,
        priority: str | None = None,
        is_automated: bool | None = None,
    ) -> tuple[list[TestCase], int]:
        """List test cases with optional filtering and pagination.

        Args:
            page: Page number (1-based).
            size: Items per page.
            search: Optional fuzzy search on name.
            category_id: Optional filter by category.
            priority: Optional filter by priority level.
            is_automated: Optional filter by automation status.

        Returns:
            Tuple of (list of TestCase, total count).
        """
        # TODO: Implement case listing
        #   - Build base query: select(TestCase)
        #   - Apply filters conditionally (search via ilike / pg_trgm)
        #   - Apply pagination: .offset((page-1)*size).limit(size)
        #   - Execute count query for total
        #   - Return (items, total)
        raise NotImplementedError

    def get_case(self, case_id: str) -> TestCase:
        """Get a single test case by ID.

        Args:
            case_id: Test case UUID.

        Returns:
            TestCase instance.

        Raises:
            NotFoundError: If the case does not exist.
        """
        # TODO: Implement get_case
        #   - db.get(TestCase, case_id)
        #   - Raise NotFoundError if None
        raise NotImplementedError

    def create_case(
        self,
        name: str,
        created_by: str,
        priority: str | None = None,
        steps: str | None = None,
        category_id: str | None = None,
    ) -> TestCase:
        """Create a new test case.

        Args:
            name: Test case name.
            created_by: UUID of the creating user.
            priority: Priority level (default P2).
            steps: Optional test steps description.
            category_id: Optional category UUID.

        Returns:
            Newly created TestCase instance.

        Raises:
            ValidationError: If required fields are missing or invalid.
        """
        # TODO: Implement case creation
        #   - Validate name is not empty
        #   - Create TestCase instance with provided data
        #   - db.add() + db.flush()
        #   - Return the created instance
        raise NotImplementedError

    def update_case(self, case_id: str, data: dict) -> TestCase:
        """Update an existing test case (partial update).

        Args:
            case_id: Test case UUID.
            data: Dictionary of fields to update.

        Returns:
            Updated TestCase instance.

        Raises:
            NotFoundError: If the case does not exist.
            ValidationError: If update data is invalid.
        """
        # TODO: Implement case update
        #   - Get existing case (raise NotFound if missing)
        #   - Apply allowed fields from data dict
        #   - db.flush()
        #   - Return updated case
        raise NotImplementedError

    def delete_case(self, case_id: str) -> None:
        """Delete a test case and its associated script file.

        Args:
            case_id: Test case UUID.

        Raises:
            NotFoundError: If the case does not exist.
        """
        # TODO: Implement case deletion
        #   - Get existing case (raise NotFound if missing)
        #   - If script_path exists, delete the file from disk
        #   - db.delete(case)
        #   - db.flush()
        raise NotImplementedError

    def upload_script(self, case_id: str, file_storage) -> str:
        """Upload and store a Python script for a test case.

        The script is validated for security (AST check) and saved to
        the configured upload folder with the case UUID as filename.

        Args:
            case_id: Test case UUID.
            file_storage: A Werkzeug FileStorage instance.

        Returns:
            Relative path to the stored script.

        Raises:
            NotFoundError: If the case does not exist.
            ScriptValidationError: If the script fails validation.
        """
        # TODO: Implement script upload
        #   - Get case (raise NotFound if missing)
        #   - Read file content
        #   - Run validate_script() from app.utils.validators
        #   - Save file to UPLOAD_FOLDER / {case_id}.py
        #   - Update case.script_path and case.is_automated = True
        #   - Return relative path
        raise NotImplementedError

    def get_script_path(self, case_id: str) -> str | None:
        """Get the absolute filesystem path to a case's script.

        Args:
            case_id: Test case UUID.

        Returns:
            Absolute path string, or None if no script exists.

        Raises:
            NotFoundError: If the case does not exist.
        """
        # TODO: Implement get_script_path
        #   - Get case (raise NotFound if missing)
        #   - Return absolute path if script_path set, else None
        raise NotImplementedError

    def get_execution_history(
        self, case_id: str, page: int = 1, size: int = 20
    ) -> tuple[list, int]:
        """Get paginated execution history for a test case.

        Args:
            case_id: Test case UUID.
            page: Page number (1-based).
            size: Items per page.

        Returns:
            Tuple of (list of TestRun dicts, total count).
        """
        # TODO: Implement execution history
        #   - Verify case exists (raise NotFound if missing)
        #   - Query test_runs filtered by test_case_id
        #   - Apply pagination
        #   - Return (runs, total)
        raise NotImplementedError
