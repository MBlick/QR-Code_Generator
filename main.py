
import os
import time
import qrcode
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import fileHandling
import myVariables
import myFunctions

# get the user's desktop path and define the folder to monitor
desktopPathUser = os.path.expanduser('~') + "\\Desktop"
nameFolderToMonitor = "Create QR-Code"
folderToMonitor = desktopPathUser + "\\" + nameFolderToMonitor

# create the folder "Create QR-Code", if it does not exist yet
try:
  os.makedirs(folderToMonitor, exist_ok=True)
except OSError as error:
  print("Error creating folder on desktop: " + error)

class QRCodeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # get the path of the new file or URL
            filePath = event.src_path

            fileName, oldExtension = fileHandling.getFileName(filePath)
            if (not fileHandling.checkExtension(oldExtension)):
                print("Wrong filetype!")
                fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)
            else:
                # extract data and generate qr code
                try:
                    # open the file and extract the relevant data
                    data = myFunctions.extractURL(filePath, oldExtension)

                    # generate QR code
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=5
                    )
                    qr.add_data(data)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    # convert to 24-bit RGB mode (so it can be read better by some qr-code readers (iOS folder f.e.))
                    img = img.convert('RGB')
                    # save the QR code image on the desktop
                    img.save(desktopPathUser + "\\" + fileName + myVariables.NEWEXTENSION)

                    # print out result to the console
                    print("QR code generated for " + filePath + " and saved as " + fileName + myVariables.NEWEXTENSION + " on desktop.")

                    # delete the old file after the qr code got generated
                    fileHandling.deleteFile(filePath)
                    
                # exception handling
                except FileNotFoundError as error:
                    print("Error: File not found - " + str(error)) # catch error if the file has been removed unintentionally (very unlikely due to the speed of processing)
                    fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)
                except OSError as error:
                    print("Error reading file: " + str(error))
                    fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)
                except UnicodeDecodeError as error:
                    print("Error decoding file: " + str(error))
                    fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)
                except:
                    print("General error: " + str(error))
                    fileHandling.moveFile(filePath, desktopPathUser + "\\" + fileName + oldExtension)

# create and start the observer
eventHandler = QRCodeHandler()
observer = Observer()
observer.schedule(eventHandler, folderToMonitor, recursive=True)
observer.start()

try:
    while True:
        time.sleep(.5)
except KeyboardInterrupt:
    observer.stop()

observer.join()