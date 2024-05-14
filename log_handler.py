import os
class loghandle:
    
    def __init__(self):
        self.setpath = []
    def pathset(self, string):
        self.setpath.append(string)
        
    def log(self, error):
        if len(self.setpath[0:]) >= 1:
            def write(error):
                dir = self.setpath[0]
                try:
                    refreshed_time = str(datetime.datetime.now().date())
                    log_write = open(dir+"/logs/LOG "+refreshed_time+".txt", "a+")
                    string = str(error)
                    log_write.write("\nLOGGED -"+refreshed_time+" - "+string)
                    log_write.close()
                except Exception as e:
                    try:
                        os.mkdir('logs')
                        write(error)
                    except:
                        return (str(e))
                        

            try:
                dic = self.setpath
                try:
                    import datetime
                    write(error)
                except ImportError as e:
                    try:
                        return ("Error -- "+str(e))
                        
                    except:
                        return ("Error - Imports not available")
            except KeyboardInterrupt or ValueError as e:
                return ("Error -- "+str(e))
            except RuntimeError as fatal:
                return "FATAL ERROR CONTACT DEVELOPER ---- "+str(fatal)
            except FileNotFoundError:
                os.mkdir('logs')
                write(error)
            except FileExistsError:
                write(error)
            except:
                return
        else:
            return (self.setpath)