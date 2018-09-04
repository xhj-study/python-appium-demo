import logging
import time
import threading
from Base.BaseIosPhone import get_ios_PhoneInfo
from Base.BaseRunner import *
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class iOSLog:
    def __init__(self, udid):
        get_phone = get_ios_PhoneInfo(udid)
        phone_name = get_phone["device"] + "_" + get_phone["release"] + "_" + "iOS" + "_" + get_phone["udid"]
        global logger, resultPath, logPath
        resultPath = PATH("../Log/")
        logPath = os.path.join(resultPath, (phone_name + "_" + time.strftime('%Y%m%d%H%M%S', time.localtime())))
        # with open(resultPath + "/reportpath.txt", "w") as w:
        #     w.write(logPath)
        #     w.close()
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        self.checkNo = 0
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # create handler,write log
        fh = logging.FileHandler(os.path.join(logPath, "outPut.log"))
        # Define the output format of formatter handler
        formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

        #获取系统日志，过滤当前app的log
        syslog_path = os.path.join(PATH("../Log/CrashInfo/iOS/"), "syslog.log")
        sys_cmd = 'idevicesyslog -u ' + get_phone["udid"] + " |grep 'XiaoYing' > %s" % (syslog_path)
        os.popen(sys_cmd)

    def getMyLogger(self):
        """get the logger
        :return:logger
        """
        return self.logger

    def buildStartLine(self, caseNo):
        """build the start log
        :param caseNo:
        :return:
        """
        startLine = "----  " + caseNo + "   " + "   " + \
                    "  ----"
        # startLine = "----  " + caseNo + "   " + "START" + "   " + \
        #             "  ----"
        self.logger.info(startLine)

    def buildEndLine(self, caseNo):
        """build the end log
        :param caseNo:
        :return:
        """
        endLine = "----  " + caseNo + "   " + "END" + "   " + \
                  "  ----"
        self.logger.info(endLine)
        self.checkNo = 0

    def writeResult(self, result):
        """write the case result(OK or NG)
        :param result:
        :return:
        """
        reportPath = os.path.join(logPath, "report.txt")
        flogging = open(reportPath, "a")
        try:
            flogging.write(result + "\n")
        finally:
            flogging.close()
        pass

    def resultOK(self, caseNo):
        self.writeResult(caseNo + ": OK")

    def resultNG(self, caseNo, reason):
        self.writeResult(caseNo + ": NG--" + reason)

    def checkPointOK(self, driver, caseName, checkPoint):
        """write the case's checkPoint(OK)
        :param driver:
        :param caseName:
        :param checkPoint:
        :return:
        """
        self.checkNo += 1

        self.logger.info("[CheckPoint_" + str(self.checkNo) + "]: " + checkPoint + ": OK")
        print("==用例_%s检查点成功==" % caseName)
        # take shot 默认去掉成功截图
        # self.screenshotOK(driver, caseName)

    def checkPointNG(self, driver, caseName, checkPoint):
        """write the case's checkPoint(NG)
        :param driver:
        :param caseName:
        :param checkPoint:
        :return:
        """
        self.checkNo += 1

        self.logger.info("[CheckPoint_" + str(self.checkNo) + "]: " + checkPoint + ": NG")

        # take shot
        return self.screenshotNG(driver, caseName)

    def screenshotOK(self, driver, caseName):
        """screen shot
        :param driver:
        :param caseName:
        :return:
        """
        screenshotPath = os.path.join(logPath, caseName)
        screenshotName = "CheckPoint_" + str(self.checkNo) + "_OK.png"

        # wait for animations to complete before taking screenshot
        time.sleep(1)
        # driver.get_screenshot_as_file(os.path.join(screenshotPath, screenshotName))
        driver.get_screenshot_as_file(os.path.join(screenshotPath + screenshotName))

    def screenshotNG(self, driver, caseName):
        """screen shot
        :param driver:
        :param caseName:
        :return:
        """
        screenshotPath = os.path.join(logPath, caseName)
        screenshotName = "CheckPoint_" + str(self.checkNo) + "_NG.png"

        # wait for animations to complete before taking screenshot
        time.sleep(1)
        driver.get_screenshot_as_file(os.path.join(screenshotPath + screenshotName))
        return os.path.join(screenshotPath + screenshotName)

    def screenshotERROR(self, driver, caseName):
        """screen shot
        :param driver:
        :param caseName:
        :return:
        """
        screenshotPath = os.path.join(logPath, caseName)
        screenshotName = "ERROR.png"

        # wait for animations to complete before taking screenshot
        time.sleep(1)
        driver.get_screenshot_as_file(os.path.join(screenshotPath, screenshotName))

class myIosLog:
    """
    This class is used to get log
    """

    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def getLog(udid):
        if myIosLog.log is None:
            myIosLog.mutex.acquire()
            myIosLog.log = iOSLog(udid)
            myIosLog.mutex.release()
        return myIosLog.log


if __name__ == "__main__":
    pass
    # logTest = myIosLog.getLog("5214866ccb9342f87f4c2aab093c25f7e252fd85")
    # logger = logTest.getMyLogger()