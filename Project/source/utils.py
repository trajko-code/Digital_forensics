from enum import Enum
import os


CONTENT_PROVIDER_APK_PATH = os.path.abspath(os.path.dirname( __file__ )) + "/../ContentProviderApp/app/build/outputs/apk/debug/app-debug.apk"
CONTENT_PROVIDER_APP_PKG = "com.example.callscontentprovider"
CONTENT_PROVIDER_APP_ACTIVITY = CONTENT_PROVIDER_APP_PKG + ".MainActivity"
READ_CALL_PERMISSION = "android.permission.READ_CALL_LOG"
CUSTOM_PROVIDER_NAME = "com.demo.user.provider"
ADB_EXPORT_SCRIPT = os.path.abspath(os.path.dirname( __file__ )) + "/../adb-export/adb-export.sh"
CSV_FILE_NAME = "data.csv"

# Content providers
CALLS_PROVIDER = CUSTOM_PROVIDER_NAME+"/calls"
CONTACTS_PROVIDER = "com.android.contacts/contacts"
CONTACTS_DATA_PROVIDER = "com.android.contacts/data"
CALENDAR_PROVIDER = "com.android.calendar/calendars"

def createProviderCmd(provider):
    return "-e content://" + provider

class Status(Enum):
    OK = 0
    ERROR = 1

def returnCodeToStatus(retCode):
    if retCode == 0:
        return Status.OK
    else:
        return Status.ERROR

class Data_type(Enum):
    CALL = 0
    CONTACTS = 1