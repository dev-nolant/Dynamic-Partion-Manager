class BytesManager:
    def __init__(self) -> None:
        pass

    def Megabytes(self, megabytes:int, reversed=None):
        if not reversed:
            bytes = megabytes*1048576
            return int(bytes)
        else:
            return (megabytes / (1048576) ) + 1
    
    def Gigabytes(self, gigabytes:int, reversed=None):
        if not reversed:
            bytes = ((1073741824) * gigabytes) - 1
            return int(bytes)
        else:
            return (gigabytes / (1073741824) )
    
    
    def ByteDetection(self, byteType:str):
        byteType = byteType.lower()  # Convert byteType to lowercase
        if "gb" in byteType:
            return self.Gigabytes(int(byteType.replace("gb", "")))
        elif "mb" in byteType:
            return self.Megabytes(int(byteType.replace("mb", "")))