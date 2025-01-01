import ctypes
import json
import locale
import os
import platform
import shutil
import subprocess
import sys
import tkinter as tk
import uuid
from pathlib import Path
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

import psutil


class Messages:
    def __init__(self):
        self.EN_MESSAGES = {
            'title': "Cursor Reset Tool",
            'starting': "Starting installation...",
            'os_detected': "Detected OS:",
            'downloading': "Downloading latest release...",
            'installing': "Installing binary...",
            'cleaning': "Cleaning up...",
            'success': "Operation completed successfully!",
            'checking_processes': "Checking for running Cursor instances...",
            'found_processes': "Found running Cursor processes. Attempting to close...",
            'closed_processes': "Successfully closed all Cursor instances",
            'backup_created': "Backup created at:",
            'need_root': "This operation requires root privileges",
            'description': """This tool resets Cursor editor device identifiers.
Please ensure:
1. Cursor is completely closed
2. Important data is backed up
3. You have sufficient file access permissions""",
            'error_download': "Failed to download",
            'error_permission': "Permission denied",
            'error_unsupported_os': "Unsupported operating system",
            'error_process_close': "Failed to close Cursor processes",
            'language_select': "Select Language",
            'ready': "Ready",
            'reset_button': "Reset"
        }

        self.CN_MESSAGES = {
            'title': "Cursor 重置工具",
            'starting': "开始安装...",
            'os_detected': "检测到操作系统：",
            'downloading': "正在下载最新版本...",
            'installing': "正在安装...",
            'cleaning': "正在清理...",
            'success': "操作成功完成！",
            'checking_processes': "正在检查运行中的Cursor进程...",
            'found_processes': "发现正在运行的Cursor进程，尝试关闭...",
            'closed_processes': "成功关闭所有Cursor实例",
            'backup_created': "备份已创建于：",
            'need_root': "此操作需要root权限",
            'description': """此工具用于重置 Cursor 编辑器的设备识别码。
使用前请确保：
1. Cursor 已完全关闭
2. 已备份重要数据
3. 具有足够的文件访问权限""",
            'error_download': "下载失败",
            'error_permission': "权限被拒绝",
            'error_unsupported_os': "不支持的操作系统",
            'error_process_close': "无法关闭Cursor进程",
            'language_select': "选择语言",
            'ready': "就绪",
            'reset_button': "重置"
        }

        self.RU_MESSAGES = {
            'title': "Инструмент сброса Cursor",
            'starting': "Начало установки...",
            'os_detected': "Обнаружена ОС:",
            'downloading': "Загрузка последней версии...",
            'installing': "Установка...",
            'cleaning': "Очистка...",
            'success': "Операция успешно завершена!",
            'checking_processes': "Проверка запущенных процессов Cursor...",
            'found_processes': "Обнаружены запущенные процессы Cursor. Попытка закрытия...",
            'closed_processes': "Все процессы Cursor успешно закрыты",
            'backup_created': "Резервная копия создана в:",
            'need_root': "Для этой операции требуются права администратора",
            'description': """Этот инструмент сбрасывает идентификаторы устройства редактора Cursor.
Пожалуйста, убедитесь что:
1. Cursor полностью закрыт
2. Важные данные сохранены
3. У вас есть необходимые права доступа""",
            'error_download': "Ошибка загрузки",
            'error_permission': "Отказано в доступе",
            'error_unsupported_os': "Неподдерживаемая операционная система",
            'error_process_close': "Не удалось закрыть процессы Cursor",
            'language_select': "Выберите язык",
            'ready': "Готово",
            'reset_button': "Сбросить"
        }

        self.current_language = 'en'
        self.messages = self.EN_MESSAGES

    def set_language(self, lang: str):
        """Set the current language"""
        self.current_language = lang
        if lang == 'en':
            self.messages = self.EN_MESSAGES
        elif lang == 'cn':
            self.messages = self.CN_MESSAGES
        elif lang == 'ru':
            self.messages = self.RU_MESSAGES

    def get(self, key: str) -> str:
        return self.messages.get(key, key)


class CursorResetter:
    def __init__(self, log_func, messages):
        self.log_func = log_func
        self.messages = messages
        self.config_path = self.get_config_path()

    def get_config_path(self) -> Path:
        """Get configuration file path based on OS"""
        system = platform.system().lower()

        if system == "windows":
            base_path = os.getenv("APPDATA")
            return Path(base_path) / "Cursor" / "User" / "globalStorage" / "storage.json"
        elif system == "darwin":
            return Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "storage.json"
        elif system == "linux":
            return Path.home() / ".config" / "Cursor" / "User" / "globalStorage" / "storage.json"
        else:
            raise OSError(self.messages.get('error_unsupported_os'))

    def check_root_privileges(self) -> bool:
        """Check if script has root/admin privileges"""
        try:
            return os.geteuid() == 0
        except AttributeError:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def request_root_privileges(self):
        """Request root/admin privileges"""
        if platform.system().lower() == "darwin":
            if not self.check_root_privileges():
                script_path = os.path.abspath(sys.argv[0])
                command = f"""osascript -e 'do shell script "python3 \\"{script_path}\\"" with administrator privileges'"""
                try:
                    subprocess.run(command, shell=True, check=True)
                    sys.exit(0)
                except subprocess.CalledProcessError:
                    raise PermissionError(self.messages.get('error_permission'))
        elif platform.system().lower() == "windows":
            if not self.check_root_privileges():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(0)
        else:
            if not self.check_root_privileges():
                try:
                    subprocess.run(['pkexec', sys.executable] + sys.argv, check=True)
                    sys.exit(0)
                except subprocess.CalledProcessError:
                    raise PermissionError(self.messages.get('error_permission'))

    def close_cursor_processes(self) -> bool:
        """Close all running Cursor processes"""
        self.log_func(self.messages.get('checking_processes'))
        cursor_processes = []

        for proc in psutil.process_iter(['name']):
            try:
                if "cursor" in proc.name().lower():
                    cursor_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if cursor_processes:
            self.log_func(self.messages.get('found_processes'))
            for proc in cursor_processes:
                try:
                    proc.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return False

            psutil.wait_procs(cursor_processes, timeout=3)
            self.log_func(self.messages.get('closed_processes'))
            return True
        return True

    def backup_config(self):
        """Create backup of the configuration file"""
        if self.config_path.exists():
            backup_path = self.config_path.with_suffix('.json.backup')
            shutil.copy2(self.config_path, backup_path)
            self.log_func(f"{self.messages.get('backup_created')} {backup_path}")

    def update_config(self) -> bool:
        """Update configuration with new identifiers"""
        try:
            if not self.config_path.exists():
                self.log_func("Configuration file not found!")
                return False

            self.backup_config()

            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            new_ids = {
                "telemetry.macMachineId": str(uuid.uuid4()),
                "telemetry.machineId": str(uuid.uuid4()),
                "telemetry.devDeviceId": str(uuid.uuid4()),
                "telemetry.sqmId": str(uuid.uuid4()),
                "lastModified": "2024-01-01T00:00:00.000Z",
                "version": "1.0.1"
            }

            config.update(new_ids)

            for key, value in new_ids.items():
                self.log_func(f"New {key}: {value}")

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)

            return True

        except Exception as e:
            self.log_func(f"Error updating configuration: {e}")
            return False


class CursorResetterGUI:
    def __init__(self, root):
        self.root = root
        self.messages = Messages()
        self.root.title(self.messages.get('title'))
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.show_language_selection()

    def show_language_selection(self):
        """Show language selection dialog"""
        self.lang_window = tk.Toplevel(self.root)
        self.lang_window.title(self.messages.get('language_select'))
        self.lang_window.geometry("300x200")
        self.lang_window.transient(self.root)
        self.lang_window.grab_set()

        frame = ttk.Frame(self.lang_window, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            frame,
            text=self.messages.get('language_select'),
            font=('Arial', 12, 'bold')
        ).grid(row=0, column=0, pady=10)

        languages = [
            ("English", 'en'),
            ("中文", 'cn'),
            ("Русский", 'ru')
        ]

        for i, (lang_name, lang_code) in enumerate(languages):
            btn = ttk.Button(
                frame,
                text=lang_name,
                command=lambda code=lang_code: self.select_language(code)
            )
            btn.grid(row=i+1, column=0, pady=5, padx=20, sticky="ew")

    def select_language(self, lang: str):
        """Handle language selection"""
        self.messages.set_language(lang)
        self.lang_window.destroy()
        self.setup_ui()

    def setup_ui(self):
        """Setup GUI interface"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(self.messages.get('title'))
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Title
        title_label = ttk.Label(
            main_frame,
            text=self.messages.get('title'),
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=10)

        # Description
        desc_label = ttk.Label(
            main_frame,
            text=self.messages.get('description'),
            wraplength=550,
            justify=tk.LEFT
        )
        desc_label.grid(row=1, column=0, pady=10)

        self.reset_button = ttk.Button(
            main_frame,
            text=self.messages.get('reset_button'),
            command=self.reset_cursor
        )
        self.reset_button.grid(row=2, column=0, pady=10)


        self.lang_button = ttk.Button(
            main_frame,
            text=self.messages.get('language_select'),
            command=self.show_language_selection
        )
        self.lang_button.grid(row=2, column=1, pady=10, padx=5)


        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)

        self.log_text = ScrolledText(
            log_frame,
            width=60,
            height=10,
            wrap=tk.WORD
        )
        self.log_text.pack(expand=True, fill=tk.BOTH)


        self.status_var = tk.StringVar(value=self.messages.get('ready'))
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN
        )
        status_bar.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

    def log(self, message: str):
        """Add log message"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()

    def reset_cursor(self):
        """Main reset operation"""
        self.reset_button.state(['disabled'])
        self.status_var.set(self.messages.get('starting'))

        try:
            # Check privileges
            if not self.resetter.check_root_privileges():
                self.resetter.request_root_privileges()
                return

            # Close Cursor processes
            if not self.resetter.close_cursor_processes():
                raise RuntimeError(self.messages.get('error_process_close'))

            # Update configuration
            if self.resetter.update_config():
                messagebox.showinfo(
                    self.messages.get('title'),
                    self.messages.get('success')
                )
                self.status_var.set(self.messages.get('success'))
            else:
                raise RuntimeError("Failed to update configuration")

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )
            self.status_var.set("Error")
        finally:
            self.reset_button.state(['!disabled'])


def main():
    root = tk.Tk()
    app = CursorResetterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
