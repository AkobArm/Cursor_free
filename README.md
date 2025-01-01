# 🚀 Cursor Reset Trial

[![Release](https://img.shields.io/github/v/release/AkobArm/Cursor_free)](https://github.com/AkobArm/Cursor_free/releases/latest)
[![License](https://img.shields.io/github/license/AkobArm/Cursor_free)](LICENSE)
[![Stars](https://img.shields.io/github/stars/AkobArm/Cursor_free?style=flat-square&logo=github)](https://github.com/AkobArm/Cursor_free/stargazers)



[English](#english) | [中文](#chinese) | [Русский](#russian)

<div align="center">
  <img src="https://camo.githubusercontent.com/496f1515f3e17ce1afe69703f2f708409cf48325a64b654e1788d9e2ea8c17c6/68747470733a2f2f61692d637572736f722e636f6d2f77702d636f6e74656e742f75706c6f6164732f323032342f30392f6c6f676f2d637572736f722d61692d706e672e77656270" alt="Cursor Free" width="120">
</div>

## 🌟 English

### 📝 Description

A powerful GUI tool that resets Cursor Editor device identifiers when you encounter the message:

> Too many free trial accounts used on this machine.
> Please upgrade to pro. We have this limit in place
> to prevent abuse. Please let us know if you believe
> this is a mistake.
### 💫 Features

- 🖥️ User-friendly graphical interface
- 🔄 Automatic process management
- 💾 Automatic configuration backup
- 🔑 New device ID generation
- 🌏 Multi-language support (English, Chinese & Russian)
- 🖥️ Cross-platform compatibility
- 🛡️ Elevated privileges handling
- 🎨 Modern centered UI design

<div align="center">
    <img src=gui.png alt="Cursor Free" width="600">
</div>

### 💻 System Support

- Windows ✅ (x64)
- macOS ✅ (Intel & M-series)
- Linux ✅ (x64 & ARM64)

### 📥 Installation

#### Automatic Installation (Recommended)

## Prerequisites

- Python 3.9 or higher
- Required Python packages:  ```
  psutil  ```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AkobArm/Cursor_free.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the tool:
```bash
python main.py
```

### 🔧 Technical Details

#### Configuration Files

The tool manages Cursor's configuration at:

- Windows: `%APPDATA%\Cursor\User\globalStorage\storage.json`
- macOS: `~/Library/Application Support/Cursor/User/globalStorage/storage.json`
- Linux: `~/.config/Cursor/User/globalStorage/storage.json`

#### Modified Fields
```json
{
  "telemetry.machineId": "<new-uuid>",
  "telemetry.macMachineId": "<new-uuid>",
  "telemetry.devDeviceId": "<new-uuid>",
  "telemetry.sqmId": "<new-uuid>"
}
```

#### Safety Features

- 🔒 Automatic configuration backup
- ⚡ Safe process termination
- 📝 Atomic file operations
- ⚠️ Error handling and rollback

### 📦 Latest Updates (v0.0.2)

- ✨ Added Russian language support
- 🎨 Improved UI layout with centered buttons
- 🔧 Enhanced macOS permissions handling
- 💅 Refined language selection interface
- 🚀 Improved startup experience with language selection dialog

## 🌏 Chinese

### 📝 描述

当遇到以下提示时，这个强大的GUI工具可以重置Cursor编辑器的设备标识符：

> Too many free trial accounts used on this machine.
> Please upgrade to pro. We have this limit in place
> to prevent abuse. Please let us know if you believe
> this is a mistake.
[... Chinese version continues with same structure as English ...]

## 🌏 Russian

### 📝 Описание

Мощный инструмент с графическим интерфейсом для сброса идентификаторов устройства редактора Cursor, когда вы сталкиваетесь с сообщением:

> Too many free trial accounts used on this machine.
> Please upgrade to pro. We have this limit in place
> to prevent abuse. Please let us know if you believe
> this is a mistake.

### 💫 Возможности

- 🖥️ Удобный графический интерфейс
- 🔄 Автоматическое управление процессами
- 💾 Автоматическое резервное копирование
- 🔑 Генерация новых ID устройства
- 🌏 Многоязычная поддержка
- 🖥️ Кроссплатформенность
- 🛡️ Обработка прав администратора

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not officially associated with Cursor Editor. Use at your own risk. Always backup your data before using this tool.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/AkobArm/Cursor_free/issues) on GitHub.