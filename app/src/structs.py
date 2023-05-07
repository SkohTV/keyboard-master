





class User:
  def __init__(self, name: str, hashed_password: str) -> None:
    self.name = name
    self.hashed_password = hashed_password