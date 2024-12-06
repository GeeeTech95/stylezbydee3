from whitenoise.storage import CompressedManifestStaticFilesStorage

class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            # If a referenced file is missing, return the original name
            self.missing_file_error(name)
            return name

    def missing_file_error(self, name):
        # Log a warning instead of raising an error
        import logging
        logger = logging.getLogger('django')
        logger.warning(f"Missing file referenced: {name}")
