class Config:
    """Global configuration for the anonymize-data library."""

    default_mask_char: str = "*"
    strict_mode: bool = False
    fallback_masking: bool = True

    @classmethod
    def setup(
        cls,
        mask_char: str = "*",
        strict_mode: bool = False,
        fallback_masking: bool = True,
    ) -> None:
        """Helper to configure global settings."""
        cls.default_mask_char = mask_char
        cls.strict_mode = strict_mode
        cls.fallback_masking = fallback_masking
