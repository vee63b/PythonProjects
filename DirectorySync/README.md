# DirectorySync
This Python script was written to automate syncing files and directories between one device to another or my personal NAS (SMB2 File Share on Windows Server 2019), I've tried to keep everything commented in case you need to readjust for your own needs. The executable was generated using the following method/commands:



*You will need the Windows SDK for the signtool.exe (https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/) recommended to add the path for both Win SDK and pyinstaller to path so you can use the command from anywhere*

Powershell:
1: Export-PfxCertificate -Cert $cert -FilePath "C:\Path-To-Your-Where-You-Store-Your-Certs\SignedByVentura.pfx" -Password (ConvertTo-SecureString -String "PASSWORD" -Force -AsPlainText)
*Create your own Personal Code Signing Certificate if you package your own exe otherwise Windows will flag is as malware, replace the path and "PASSWORD" with your own path and cert password*

2: pyinstaller --onefile --noconsole --distpath="." DirectorySync.py
*Whitelist your working directory or at your own risk temporarily disable Windows Realtime Protection, also run Powershell as admin. Otherwise the package will fail with "File "C:\Users\YOURUSERNAME\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\win32ctypes\pywin32\pywintypes.py", line 37, in pywin32error raise error(exception.winerror, exception.function, exception.strerror) win32ctypes.pywin32.pywintypes.error: (225, '', 'Operation did not complete successfully because the file contains a virus or potentially unwanted software')*

3: signtool sign /f "C:\Path-To-Your-Where-You-Store-Your-Certs\SignedByVentura.pfx" /p PASSWORD /t http://timestamp.digicert.com /v "C:\Users\ventura\GIT\PythonProjects\DirectorySync\PyQt5\DirectorySync.exe"
*After you've packaged the .py into an .exe you will need to sign it with the cert created in step 1, use your paths and the password you created in step 1*
