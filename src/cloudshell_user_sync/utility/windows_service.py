import socket
import win32serviceutil
import servicemanager
import win32event
import win32service
from cloudshell_user_sync.utility.schedule_handler import ScheduleHandler


class CloudshellSyncWinService(win32serviceutil.ServiceFramework):
    """Base class to create winservice in Python"""

    _svc_name_ = 'CloudshellUserSync'
    _svc_display_name_ = 'Cloudshell User Sync'
    _svc_description_ = 'Sync Cloudshell users with LDAP / Active Directory.'

    @classmethod
    def parse_command_line(cls):
        """
        ClassMethod to parse the command line
        """
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        """
        Constructor of the winservice
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.schedule_handler = ScheduleHandler()

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        """
        Override to add logic before the start
        eg. running condition
        """
        pass

    def stop(self):
        """
        Override to add logic before the stop
        eg. invalidating running condition
        """
        self.schedule_handler.stop_scheduler()

    def main(self):
        """
        Main class to be ovverridden to add logic
        """
        self.schedule_handler.run_scheduler()


# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    CloudshellSyncWinService.parse_command_line()
