import subprocess
import re

from source.utils import *

class ADB_commands:
    @staticmethod
    def getConnectedDevices():
        result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE)

        print(result.stdout.decode("utf-8"))

        return ADB_commands.parseDevices(result.stdout.decode("utf-8"))

    @staticmethod
    def parseDevices(adb_devices_output):

        if not isinstance(adb_devices_output, str):
            raise Exception("Wrong adb devices string argument, str expected")

        list_str = "List of devices attached"
        list_index = adb_devices_output.find(list_str)

        if list_index == -1:
            raise Exception("Wrong adb devices string argument")

        str_for_search = adb_devices_output[list_index + len(list_str):]

        devices_list = []
        r1 = re.findall(r"\n\w+\t", str_for_search)
        for item in r1:
            devices_list.append(str(item).replace("\n", "").replace("\t", ""))

        devices_list += re.findall(r'[0-9]+(?:\.[0-9]+){3}', str_for_search)

        return devices_list

    @staticmethod
    def installContentProviderProxyApp():
        print("Installing content provider proxy app ...")

        result = subprocess.run(["adb", "install", CONTENT_PROVIDER_APK_PATH], stdout=subprocess.PIPE)

        return returnCodeToStatus(result.returncode)

    @staticmethod
    def uninstallContentProviderProxyApp():
        print("Uninstalling content provider proxy app ...")

        result = subprocess.run(["adb", "uninstall", CONTENT_PROVIDER_APP_PKG], stdout=subprocess.PIPE)

        return returnCodeToStatus(result.returncode)

    @staticmethod
    def runContentProviderProxyApp():
        print("Starting content provider proxy app ...")

        # adb shell am start -n com.example.callscontentprovider/com.example.callscontentprovider.MainActivity
        run_cmd = ["adb", "shell", "am", "start", "-n", CONTENT_PROVIDER_APP_PKG + "/" + CONTENT_PROVIDER_APP_ACTIVITY]
        run_result = subprocess.run(run_cmd, stdout=subprocess.PIPE)

        if run_result == Status.ERROR:
            return Status.ERROR

        # adb shell pm grant com.example.callscontentprovider android.permission.READ_CALL_LOG
        permission_cmd = ["adb", "shell", "pm", "grant", CONTENT_PROVIDER_APP_PKG, READ_CALL_PERMISSION]
        result = subprocess.run(permission_cmd, stdout=subprocess.PIPE)

        return returnCodeToStatus(result.returncode)

    @staticmethod
    def exportData(device, provider):
        # ./adb-export.sh -e content://com.demo.user.provider/calls
        print("Exporting data from a device {} using provider {} ...".format(device, provider))

        # TODO Change adb-export script to take device as argument
        proc = subprocess.Popen(['bash {} {}'.format(ADB_EXPORT_SCRIPT, createProviderCmd(provider))], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        result = proc.communicate()[0]

        out_str = "Output folder with CSV:"
        out_index = result.find(out_str)

        if out_index == -1:
            return [Status.ERROR, ""]

        log_data = result[result.find("Result:"):]
        print(log_data)

        begining_index = out_index + len(out_str)
        last_index = result.find("\n", out_index + len(out_str))
        if last_index == -1:
            data_csv_dir = result[begining_index:].replace(" ", "")
        else:
            data_csv_dir = result[begining_index:last_index].replace(" ", "")

        data_csv_file = data_csv_dir + "/data.csv"

        return [Status.OK, data_csv_file]

    @staticmethod
    def getData(device, provider):
        # Install content provider proxy app
        status = ADB_commands.installContentProviderProxyApp()
        if status == Status.ERROR:
            print("Error while installing content provider app")
            return [Status.ERROR, ""]

        # Run content provider proxy app and grant permission
        status = ADB_commands.runContentProviderProxyApp()
        if status == Status.ERROR:
            print("Error while starting content provider app")
            ADB_commands.uninstallContentProviderProxyApp()
            return [Status.ERROR, ""]

        # Get call logs using adb-export
        status, csv_data = ADB_commands.exportData(device, provider)
        if status == Status.ERROR:
            print("Error while exporting data")
            ADB_commands.uninstallContentProviderProxyApp()
            return [Status.ERROR, ""]

        ADB_commands.uninstallContentProviderProxyApp()

        print("Data writed to {}".format(csv_data))

        return [Status.OK, csv_data]
