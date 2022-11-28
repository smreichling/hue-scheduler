
class InitializationException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class InvalidBridgeAddressException(InitializationException):
    msg: str
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__("Specified bridge is invalid: %s" % msg)

class InvalidGroupNameException(InitializationException):
    group: str
    def __init__(self, group: str) -> None:
        self.group = group
        super().__init__("Specified room or zone %s does not exist" % group)

class InvalidColorException(InitializationException):
    color: str
    def __init__(self, color: str) -> None:
        self.color = color
        super().__init__("Specified color %s is unknown" % color)
