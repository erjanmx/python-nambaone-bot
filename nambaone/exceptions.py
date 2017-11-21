
class ClientException(Exception):
    """Base class for exceptions in this module."""
    pass


class FileDownloadException(ClientException):
    pass


class FileUploadException(ClientException):
    """File upload exception"""
    pass
