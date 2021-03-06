


import syslog


class Syslogger:

    openstatus = False

    def openSyslogFile(self):
        syslog.openlog(ident="AESIR",logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL0)
        syslog.syslog('Started AESIR Screenshot Tool.')
        self.openstatus = True

    def writesyslogFile(self, message):

        if self.openstatus:
            syslog.syslog(message)
        else:
            self.openSyslogFile()
            self.writesyslogFile(message)