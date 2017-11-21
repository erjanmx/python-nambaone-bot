
class ClientException(Exception):
    """Base class for exceptions in this module."""
    pass


class FileNotFoundException(ClientException):
    pass


class FileUploadException(ClientException):
    """File upload exception"""
    pass
