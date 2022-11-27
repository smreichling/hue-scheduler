
class InvalidBridgeAddressException(Exception):
    msg: str
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__("Specified bridge is invalid: %s" % msg)

class InvalidGroupNameException(Exception):
    def __init__(self, group: str) -> None:
        self.group = group
        super().__init__("Specified room or zone %s does not exist" % group)