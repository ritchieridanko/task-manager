class APIException(Exception):
  def __init__(self, status_code: int, error_code: str, message: str):
    self.status_code: int = status_code
    self.error_code: str = error_code
    self.message: str = message
