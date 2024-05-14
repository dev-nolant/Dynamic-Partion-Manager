class ConfigHandler:
    def __init__(self, path:str) -> None:
        self.path = path
        self.load_config()
    
    def load_config(self):
        self.config = open(self.path+"\partition.cfg", "r").readlines()
        # Preprocessing
        self.queue = [line.strip() for line in self.config if line.strip()]  # Remove new lines and empty slots
        self.queue = [line for line in self.queue if "--" not in line]  # Comment Handler

    def getActions(self, path=None):
        # Action Processing

        if path:
            self.__init__(self, path)

        actions = []
        for line in self.queue:
            if line.startswith('>'):
                action = line[1:].strip()  # Remove the ">" and any leading/trailing whitespace
                actions.append(action.split(':'))  # Split the action into key-value pair and add to the actions list

        return actions
    
    def update_path(self, new_path: str):
        self.path = new_path
        self.load_config()

    def getUserSize(self):
        actions = self.getActions()
        for action in actions:
            if action[0] == 'indv-partitions-size':
                return(action[1])

    def getPartitionsSize(self):
        actions = self.getActions()
        for action in actions:
            if action[0] == 'partitions-size':
                return(action[1])
    
    def getMaxPartitions(self):
        actions = self.getActions()
        for action in actions:
            if action[0] == 'max-partitions':
                return(action[1])
    
    def getMaxPremium(self):
        actions = self.getActions()
        for action in actions:
            if action[0] == 'premium-max':
                return(action[1])

    @staticmethod
    def addAction(path:str, action:str, value):
        config = open(path+"\\partition.cfg", "a")
        config.write(f"> {action}: {str(value)}\n\n")
        config.close()

    @staticmethod
    def addComment(path:str, value):
        config = open(path+"\\partition.cfg", "a")
        config.write(f"--{str(value)}--\n")
        config.close()

    @staticmethod
    def setupDefault(default_partition_allocated_space:str):

        import os
        from BM import BytesManager
        import math
        
        byteManager = BytesManager()
        cwd = os.getcwd()
        path = cwd+"\\partitions"
        
        default_partition_allocated_space = byteManager.ByteDetection(default_partition_allocated_space)
        
        if not os.path.exists(path):

            os.mkdir(path)

            config = open(path+"\\partition.cfg", "a")
            config.write("--Default Settings--\n\n")
            config.close()
            f = open(f"{path}\\default_partition", "wb")
            f.seek(default_partition_allocated_space)
            f.write(b"\0")
            f.close()

            # Default Partition Database Config
            ConfigHandler.addComment(path, "This is max partition size per database")
            ConfigHandler.addAction(path, "partitions-size", f"{math.ceil(byteManager.Gigabytes(default_partition_allocated_space, reversed=True))}GB")
            ConfigHandler.addComment(path, "This is max partitions size per user. This can be modified to accommidate for SaaS")
            ConfigHandler.addAction(path, "indv-partitions-size", "1GB")
            ConfigHandler.addComment(path," -1 to allow unlimited partitions, still limited to partitions size")
            ConfigHandler.addAction(path, "max-partitions", "10")
            ConfigHandler.addComment(path,"2GB is default. User will recieve an extra GB for premium")
            ConfigHandler.addAction(path, "premium-max", "2GB")
            return True
        else:
            return f"Cloud Instance Exists: ({path})"
