import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QProgressBar, QRadioButton, QButtonGroup, QMessageBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QMetaObject, QSettings
from PyQt5.QtGui import QPalette, QColor
import os
from shutil import copy2, rmtree
from datetime import datetime
import filecmp

class Worker(QObject):
    finished = pyqtSignal()
    update_progress_bar_signal = pyqtSignal(int, int)
    update_status_signal = pyqtSignal(str)

    def __init__(self, source_folder, destination_folder, master_sync=False):
        super().__init__()
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.master_sync = master_sync
        self.progress_bar_value = 0
        self.progress_bar_maximum = 0
        self.deleted_files_count = 0
        self.deleted_directories_count = 0

    def run(self):
        source_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(self.source_folder) for f in filenames]

        if not source_files:
            self.update_status('No files to update.')
        else:
            total_files = len(source_files)
            self.update_progress_bar_signal.emit(0, None)
            start_time = datetime.now()
            self.update_status('')

            updated_files_copied = 0
            new_files_copied = 0
            skipped_files = 0

            if self.master_sync:
                # Delete files and directories not in the source directory or different in content
                self.delete_files_not_in_source(source_files)

            for index, file in enumerate(source_files):
                destination_path = os.path.join(self.destination_folder, os.path.relpath(file, self.source_folder))
                destination_directory = os.path.dirname(destination_path)
                os.makedirs(destination_directory, exist_ok=True)

                try:
                    if not os.path.exists(destination_path) or os.path.getmtime(file) > os.path.getmtime(destination_path) or os.path.getsize(file) != os.path.getsize(destination_path):
                        copy2(file, destination_path)
                        self.update_status(f'Copied: {file}')
                        if not os.path.exists(destination_path):
                            new_files_copied += 1
                        else:
                            updated_files_copied += 1
                    else:
                        # Output for skipped files
                        skipped_files += 1
                        self.update_status(f'Skipped (unchanged): {file}')
                except Exception as e:
                    self.update_status(f'Error copying {file}: {str(e)}')

                # Calculate overall progress and output the results
                overall_progress = int((index + 1) / total_files * 100)
                self.update_progress_bar_signal.emit(overall_progress, None)

            elapsed_time = datetime.now() - start_time
            self.update_status('\nCopy Completed')
            self.update_status(f'Summary:')
            self.update_status(f'Updated Files Copied: {updated_files_copied}')
            self.update_status(f'New Files Copied: {new_files_copied}')
            self.update_status(f'Skipped Files: {skipped_files}')
            self.update_status(f'Deleted Files from Destination: {self.deleted_files_count}')
            self.update_status(f'Deleted Folders from Destination: {self.deleted_directories_count}')

            self.finished.emit()

    def delete_files_not_in_source(self, source_files):
        destination_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(self.destination_folder) for f in filenames]
        destination_directories = [dp for dp, dn, filenames in os.walk(self.destination_folder)]

        # Identify files and directories in the destination that are not present in the source
        files_to_delete = set(destination_files) - set(source_files)
        directories_to_delete = set(destination_directories) - set(os.path.dirname(f) for f in source_files)

        for file_to_delete in files_to_delete:
            try:
                # Check if the file is not in the source directory before deletion
                relative_path = os.path.relpath(file_to_delete, self.destination_folder)
                source_file = os.path.join(self.source_folder, relative_path)

                if not os.path.exists(source_file):
                    if os.path.isfile(file_to_delete):
                        os.remove(file_to_delete)
                        self.deleted_files_count += 1
                        self.update_status(f'Deleted file: {file_to_delete}')
                    elif os.path.isdir(file_to_delete):
                        rmtree(file_to_delete)
                        self.deleted_directories_count += 1
                        self.update_status(f'Deleted directory: {file_to_delete}')
            except Exception as e:
                self.update_status(f'Error deleting {file_to_delete}: {str(e)}')

        for directory_to_delete in directories_to_delete:
            try:
                # Check if the directory is not in the source directory before deletion
                relative_path = os.path.relpath(directory_to_delete, self.destination_folder)
                source_directory = os.path.join(self.source_folder, relative_path)

                if not os.path.exists(source_directory):
                    rmtree(directory_to_delete)
                    self.deleted_directories_count += 1
                    self.update_status(f'Deleted directory: {directory_to_delete}')
            except Exception as e:
                self.update_status(f'Error deleting {directory_to_delete}: {str(e)}')

    def update_status(self, message):
        self.update_status_signal.emit(message)

    def update_progress_bar(self, value, maximum=None):
        self.progress_bar_maximum = maximum
        self.progress_bar_value = value
        QMetaObject.invokeMethod(self.progress_bar, "updateProgressBar", Qt.QueuedConnection)

    def get_progress_bar_value(self):
        return self.progress_bar_value

    def get_progress_bar_maximum(self):
        return self.progress_bar_maximum


class DirectorySyncApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.load_last_used_directories()

    def init_ui(self):
        self.setWindowTitle('Directory Sync')
        self.setGeometry(100, 100, 600, 450)

        layout = QVBoxLayout()

        source_layout = QHBoxLayout()
        destination_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()

        self.label_source = QLabel('Source Directory:')
        self.combobox_source = QComboBox()
        self.button_browse_source = QPushButton('Browse...')
        self.button_browse_source.clicked.connect(self.browse_source)

        self.label_destination = QLabel('Destination Directory:')
        self.combobox_destination = QComboBox()
        self.button_browse_destination = QPushButton('Browse...')
        self.button_browse_destination.clicked.connect(self.browse_destination)

        source_layout.addWidget(self.label_source)
        source_layout.addWidget(self.combobox_source)
        source_layout.addWidget(self.button_browse_source)

        destination_layout.addWidget(self.label_destination)
        destination_layout.addWidget(self.combobox_destination)
        destination_layout.addWidget(self.button_browse_destination)

        self.button_sync_files = QPushButton('Sync Files')
        self.button_sync_files.clicked.connect(self.start_copy_thread)

        self.button_master_sync = QPushButton('Master Sync')
        self.button_master_sync.clicked.connect(self.show_master_sync_warning)

        self.button_clear_directories = QPushButton('Clear Used Directories')
        self.button_clear_directories.clicked.connect(self.clear_used_directories)

        self.progress_bar = QProgressBar()
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)

        buttons_layout.addWidget(self.button_sync_files)
        buttons_layout.addWidget(self.button_master_sync)
        buttons_layout.addWidget(self.button_clear_directories)

        layout.addLayout(source_layout)
        layout.addLayout(destination_layout)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_text)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def browse_source(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        self.combobox_source.addItem(folder_path)
        self.combobox_source.setCurrentText(folder_path)

    def browse_destination(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Destination Directory')
        self.combobox_destination.addItem(folder_path)
        self.combobox_destination.setCurrentText(folder_path)

    def start_copy_thread(self):
        self.disable_buttons()
        source_folder = self.combobox_source.currentText()
        destination_folder = self.combobox_destination.currentText()

        self.worker = Worker(source_folder, destination_folder)
        self.worker.status_text = self.status_text
        self.worker.progress_bar = self.progress_bar
        self.worker.update_progress_bar_signal.connect(self.update_progress_bar)
        self.worker.update_status_signal.connect(self.update_status)
        self.worker.finished.connect(self.enable_buttons)

        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.save_last_used_directories()

    def show_master_sync_warning(self):
        warning_message = "Proceeding with a Master Sync will delete files that are in the destination directory that are not in the source directory or have different content. Would you like to continue?"
        reply = QMessageBox.question(self, 'Master Sync Warning', warning_message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.disable_buttons()
            self.start_master_sync_thread()
        else:
            self.button_master_sync.setChecked(False)

    def start_master_sync_thread(self):
        source_folder = self.combobox_source.currentText()
        destination_folder = self.combobox_destination.currentText()

        self.worker = Worker(source_folder, destination_folder, master_sync=True)
        self.worker.status_text = self.status_text
        self.worker.progress_bar = self.progress_bar
        self.worker.update_progress_bar_signal.connect(self.update_progress_bar)
        self.worker.update_status_signal.connect(self.update_status)  # Connect the new signal
        self.worker.finished.connect(self.enable_buttons)

        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.save_last_used_directories()

    def clear_used_directories(self):
        settings = QSettings("MyComputer", "DirectorySyncApp")
        settings.remove("used_source_directories")
        settings.remove("used_destination_directories")

        # Clear the dropdown lists
        self.combobox_source.clear()
        self.combobox_destination.clear()

    def disable_buttons(self):
        self.button_sync_files.setEnabled(False)
        self.button_master_sync.setEnabled(False)
        self.button_clear_directories.setEnabled(False)

    def enable_buttons(self):
        self.button_sync_files.setEnabled(True)
        self.button_master_sync.setEnabled(True)
        self.button_clear_directories.setEnabled(True)

    def update_progress_bar(self, value, maximum):
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.status_text.append(message)

    def save_last_used_directories(self):
        source_folder = self.combobox_source.currentText()
        destination_folder = self.combobox_destination.currentText()

        # Save the current directories to the list
        used_source_directories = self.get_used_directories("used_source_directories")
        used_destination_directories = self.get_used_directories("used_destination_directories")

        # Check if the directories are not already in the list before adding
        if source_folder not in used_source_directories:
            used_source_directories.append(source_folder)

        if destination_folder not in used_destination_directories:
            used_destination_directories.append(destination_folder)

        # Save the updated lists
        settings = QSettings("MyComputer", "DirectorySyncApp")
        settings.setValue("used_source_directories", used_source_directories)
        settings.setValue("used_destination_directories", used_destination_directories)

    def load_last_used_directories(self):
        # Load the used directories from settings
        used_source_directories = self.get_used_directories("used_source_directories")
        used_destination_directories = self.get_used_directories("used_destination_directories")

        # Populate the dropdown with the loaded directories
        self.combobox_source.addItems(used_source_directories)
        self.combobox_destination.addItems(used_destination_directories)

    def get_used_directories(self, key):
        # Helper method to get a list of used directories from settings
        settings = QSettings("MyComputer", "DirectorySyncApp")
        return settings.value(key, [])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DirectorySyncApp()
    window.show()
    sys.exit(app.exec_())
