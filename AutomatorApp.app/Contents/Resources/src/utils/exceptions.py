"""Custom exception classes for Medical Supplement Advisor."""


class ValidationError(Exception):
    """Raised when validation fails.

    Used for validating data structures, reference ranges, supplements, and dosage rules.
    """

    def __init__(self, message: str, field: str | None = None):
        super().__init__(message)
        self.message = message
        self.field = field

    def __str__(self) -> str:
        if self.field:
            return f"ValidationError in field '{self.field}': {self.message}"
        return f"ValidationError: {self.message}"


class DataLoaderError(Exception):
    """Raised when data loading fails.

    Used for errors loading JSON files from data directory.
    """

    def __init__(self, message: str, file_path: str | None = None):
        super().__init__(message)
        self.message = message
        self.file_path = file_path

    def __str__(self) -> str:
        if self.file_path:
            return f"DataLoaderError: {self.message} (file: {self.file_path})"
        return f"DataLoaderError: {self.message}"


class RuleEngineError(Exception):
    """Raised when rule engine encounters an error.

    Used for errors during rule matching or application.
    """

    def __init__(self, message: str, rule_id: str | None = None):
        super().__init__(message)
        self.message = message
        self.rule_id = rule_id

    def __str__(self) -> str:
        if self.rule_id:
            return f"RuleEngineError in rule '{self.rule_id}': {self.message}"
        return f"RuleEngineError: {self.message}"


class AnalysisError(Exception):
    """Raised when blood test analysis fails.

    Used for errors during blood test status determination.
    """

    def __init__(self, message: str, test_name: str | None = None):
        super().__init__(message)
        self.message = message
        self.test_name = test_name

    def __str__(self) -> str:
        if self.test_name:
            return f"AnalysisError for test '{self.test_name}': {self.message}"
        return f"AnalysisError: {self.message}"
