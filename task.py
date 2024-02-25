import threading
import wx

class Task(threading.Thread):
    def __init__(self, parent_frame):
        threading.Thread.__init__(self)
        self.parent_frame = parent_frame
        self.daemon = True


    def run(self) -> None:
        try:
            self.parent_frame.generator.update_config(self.parent_frame.new_config)
            self.parent_frame.generator.start()
        except Exception as e:
            print(e)
            wx.CallAfter(self.parent_frame.task_error)
            return

        wx.CallAfter(self.parent_frame.task_completed)
