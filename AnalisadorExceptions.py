class LexicoError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg
    
    def __str__(self) -> str:
        return f"Erro Léxico: {self.msg}"

class SintaticoError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg
    
    def __str__(self) -> str:
        return f"Erro Sintático: {self.msg}"