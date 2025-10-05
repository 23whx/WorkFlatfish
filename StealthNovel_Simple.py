"""
StealthNovel 简化版 - 隐蔽小说阅读器
带图形界面，支持多语言和自定义热键
"""

import sys
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit, QSpinBox, QComboBox,
    QGroupBox, QMessageBox, QDialog, QDialogButtonBox, QTabWidget,
    QLineEdit, QKeySequenceEdit
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QKeySequence


# 多语言字典
LANGUAGES = {
    'zh': {
        'title': 'StealthNovel - 隐蔽小说阅读器',
        'main_title': '📖 StealthNovel 隐蔽小说阅读器',
        'upload_btn': '📁 上传小说',
        'settings_btn': '⚙️ 设置',
        'file_not_loaded': '未加载小说',
        'reading_area': '阅读区域',
        'progress': '进度',
        'prev_btn': '⬅️ 上一步',
        'start_btn': '▶️ 开始阅读',
        'pause_btn': '⏸️ 暂停',
        'next_btn': '➡️ 下一步',
        'reset_btn': '🔄 重置',
        'help_text': '💡 提示：上传小说后，点击【开始阅读】进入隐蔽模式。使用方向键 → 或 ↓ 控制推进。',
        'settings_title': '设置',
        'display_mode': '显示模式',
        'display_mode_label': '选择显示模式：',
        'taskbar_mode': '任务栏标题',
        'popup_mode': '右下角弹窗',
        'normal_mode': '正常窗口',
        'advance_settings': '推进设置',
        'advance_method': '推进方式：',
        'advance_char': '逐字',
        'advance_line': '逐行',
        'auto_speed': '自动推进速度：',
        'language_settings': '语言设置',
        'select_language': '选择语言：',
        'hotkey_settings': '热键设置',
        'hotkey_next': '下一步：',
        'hotkey_prev': '上一步：',
        'hotkey_line': '下一行：',
        'hotkey_toggle': '开始/暂停：',
        'ok_btn': '确定',
        'cancel_btn': '取消',
        'success': '成功',
        'error': '错误',
        'loaded_file': '已加载',
        'lines': '行',
        'load_success': '小说加载成功！',
        'load_failed': '加载失败',
        'settings_saved': '设置已保存！',
        'progress_reset': '进度已重置到开头！',
        'select_file': '选择小说文件',
        'text_files': '文本文件 (*.txt);;所有文件 (*.*)',
    },
    'en': {
        'title': 'StealthNovel - Stealth Reader',
        'main_title': '📖 StealthNovel Stealth Reader',
        'upload_btn': '📁 Upload Novel',
        'settings_btn': '⚙️ Settings',
        'file_not_loaded': 'No novel loaded',
        'reading_area': 'Reading Area',
        'progress': 'Progress',
        'prev_btn': '⬅️ Previous',
        'start_btn': '▶️ Start',
        'pause_btn': '⏸️ Pause',
        'next_btn': '➡️ Next',
        'reset_btn': '🔄 Reset',
        'help_text': '💡 Tip: Upload a novel, then click [Start] to enter stealth mode. Use arrow keys → or ↓ to navigate.',
        'settings_title': 'Settings',
        'display_mode': 'Display Mode',
        'display_mode_label': 'Select display mode:',
        'taskbar_mode': 'Taskbar Title',
        'popup_mode': 'Corner Popup',
        'normal_mode': 'Normal Window',
        'advance_settings': 'Advance Settings',
        'advance_method': 'Advance method:',
        'advance_char': 'By Character',
        'advance_line': 'By Line',
        'auto_speed': 'Auto advance speed:',
        'language_settings': 'Language',
        'select_language': 'Select language:',
        'hotkey_settings': 'Hotkeys',
        'hotkey_next': 'Next:',
        'hotkey_prev': 'Previous:',
        'hotkey_line': 'Next Line:',
        'hotkey_toggle': 'Start/Pause:',
        'ok_btn': 'OK',
        'cancel_btn': 'Cancel',
        'success': 'Success',
        'error': 'Error',
        'loaded_file': 'Loaded',
        'lines': 'lines',
        'load_success': 'Novel loaded successfully!',
        'load_failed': 'Load failed',
        'settings_saved': 'Settings saved!',
        'progress_reset': 'Progress reset to beginning!',
        'select_file': 'Select Novel File',
        'text_files': 'Text Files (*.txt);;All Files (*.*)',
    },
    'ja': {
        'title': 'StealthNovel - ステルス小説リーダー',
        'main_title': '📖 StealthNovel ステルス小説リーダー',
        'upload_btn': '📁 小説をアップロード',
        'settings_btn': '⚙️ 設定',
        'file_not_loaded': '小説が読み込まれていません',
        'reading_area': '読書エリア',
        'progress': '進捗',
        'prev_btn': '⬅️ 前へ',
        'start_btn': '▶️ 開始',
        'pause_btn': '⏸️ 一時停止',
        'next_btn': '➡️ 次へ',
        'reset_btn': '🔄 リセット',
        'help_text': '💡 ヒント：小説をアップロードして【開始】をクリックしてステルスモードに入ります。矢印キー → または ↓ で操作します。',
        'settings_title': '設定',
        'display_mode': '表示モード',
        'display_mode_label': '表示モードを選択：',
        'taskbar_mode': 'タスクバータイトル',
        'popup_mode': '隅のポップアップ',
        'normal_mode': '通常ウィンドウ',
        'advance_settings': '進行設定',
        'advance_method': '進行方法：',
        'advance_char': '文字ごと',
        'advance_line': '行ごと',
        'auto_speed': '自動進行速度：',
        'language_settings': '言語',
        'select_language': '言語を選択：',
        'hotkey_settings': 'ホットキー',
        'hotkey_next': '次へ：',
        'hotkey_prev': '前へ：',
        'hotkey_line': '次の行：',
        'hotkey_toggle': '開始/一時停止：',
        'ok_btn': 'OK',
        'cancel_btn': 'キャンセル',
        'success': '成功',
        'error': 'エラー',
        'loaded_file': '読み込み済み',
        'lines': '行',
        'load_success': '小説が正常に読み込まれました！',
        'load_failed': '読み込み失敗',
        'settings_saved': '設定が保存されました！',
        'progress_reset': '進捗が最初にリセットされました！',
        'select_file': '小説ファイルを選択',
        'text_files': 'テキストファイル (*.txt);;すべてのファイル (*.*)',
    },
    'ko': {
        'title': 'StealthNovel - 은밀한 소설 리더',
        'main_title': '📖 StealthNovel 은밀한 소설 리더',
        'upload_btn': '📁 소설 업로드',
        'settings_btn': '⚙️ 설정',
        'file_not_loaded': '소설이 로드되지 않음',
        'reading_area': '읽기 영역',
        'progress': '진행률',
        'prev_btn': '⬅️ 이전',
        'start_btn': '▶️ 시작',
        'pause_btn': '⏸️ 일시정지',
        'next_btn': '➡️ 다음',
        'reset_btn': '🔄 재설정',
        'help_text': '💡 팁: 소설을 업로드한 후 【시작】을 클릭하여 은밀 모드로 들어갑니다. 화살표 키 → 또는 ↓로 조작합니다.',
        'settings_title': '설정',
        'display_mode': '표시 모드',
        'display_mode_label': '표시 모드 선택:',
        'taskbar_mode': '작업 표시줄 제목',
        'popup_mode': '모서리 팝업',
        'normal_mode': '일반 창',
        'advance_settings': '진행 설정',
        'advance_method': '진행 방법:',
        'advance_char': '문자별',
        'advance_line': '줄별',
        'auto_speed': '자동 진행 속도:',
        'language_settings': '언어',
        'select_language': '언어 선택:',
        'hotkey_settings': '단축키',
        'hotkey_next': '다음:',
        'hotkey_prev': '이전:',
        'hotkey_line': '다음 줄:',
        'hotkey_toggle': '시작/일시정지:',
        'ok_btn': '확인',
        'cancel_btn': '취소',
        'success': '성공',
        'error': '오류',
        'loaded_file': '로드됨',
        'lines': '줄',
        'load_success': '소설이 성공적으로 로드되었습니다!',
        'load_failed': '로드 실패',
        'settings_saved': '설정이 저장되었습니다!',
        'progress_reset': '진행률이 처음으로 재설정되었습니다!',
        'select_file': '소설 파일 선택',
        'text_files': '텍스트 파일 (*.txt);;모든 파일 (*.*)',
    }
}


class SettingsDialog(QDialog):
    """设置对话框"""
    
    def __init__(self, parent=None, current_lang='zh'):
        super().__init__(parent)
        self.current_lang = current_lang
        self.lang = LANGUAGES[current_lang]
        
        self.setWindowTitle(self.lang['settings_title'])
        self.setMinimumWidth(500)
        self.setMinimumHeight(450)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 创建标签页
        tabs = QTabWidget()
        
        # 显示设置标签页
        display_tab = self.create_display_tab()
        tabs.addTab(display_tab, self.lang['display_mode'])
        
        # 语言设置标签页
        language_tab = self.create_language_tab()
        tabs.addTab(language_tab, self.lang['language_settings'])
        
        # 热键设置标签页
        hotkey_tab = self.create_hotkey_tab()
        tabs.addTab(hotkey_tab, self.lang['hotkey_settings'])
        
        main_layout.addWidget(tabs)
        
        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText(self.lang['ok_btn'])
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(self.lang['cancel_btn'])
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)
        
        self.setLayout(main_layout)
    
    def create_display_tab(self):
        """创建显示设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 显示模式
        mode_group = QGroupBox(self.lang['display_mode'])
        mode_layout = QVBoxLayout()
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            self.lang['taskbar_mode'],
            self.lang['popup_mode'],
            self.lang['normal_mode']
        ])
        mode_layout.addWidget(QLabel(self.lang['display_mode_label']))
        mode_layout.addWidget(self.mode_combo)
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # 推进设置
        advance_group = QGroupBox(self.lang['advance_settings'])
        advance_layout = QVBoxLayout()
        
        self.advance_combo = QComboBox()
        self.advance_combo.addItems([
            self.lang['advance_char'],
            self.lang['advance_line']
        ])
        advance_layout.addWidget(QLabel(self.lang['advance_method']))
        advance_layout.addWidget(self.advance_combo)
        
        self.speed_spin = QSpinBox()
        self.speed_spin.setRange(100, 5000)
        self.speed_spin.setValue(1000)
        self.speed_spin.setSuffix(" ms")
        advance_layout.addWidget(QLabel(self.lang['auto_speed']))
        advance_layout.addWidget(self.speed_spin)
        
        advance_group.setLayout(advance_layout)
        layout.addWidget(advance_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_language_tab(self):
        """创建语言设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        lang_group = QGroupBox(self.lang['language_settings'])
        lang_layout = QVBoxLayout()
        
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "中文 (Chinese)",
            "English",
            "日本語 (Japanese)",
            "한국어 (Korean)"
        ])
        
        # 设置当前语言
        lang_index = {'zh': 0, 'en': 1, 'ja': 2, 'ko': 3}.get(self.current_lang, 0)
        self.language_combo.setCurrentIndex(lang_index)
        
        lang_layout.addWidget(QLabel(self.lang['select_language']))
        lang_layout.addWidget(self.language_combo)
        
        # 添加提示
        tip_label = QLabel("💡 " + {
            'zh': '更改语言后需要重启程序生效',
            'en': 'Restart required after changing language',
            'ja': '言語変更後は再起動が必要です',
            'ko': '언어 변경 후 재시작 필요'
        }.get(self.current_lang, ''))
        tip_label.setStyleSheet("color: #666; padding: 10px;")
        tip_label.setWordWrap(True)
        lang_layout.addWidget(tip_label)
        
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_hotkey_tab(self):
        """创建热键设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        hotkey_group = QGroupBox(self.lang['hotkey_settings'])
        hotkey_layout = QVBoxLayout()
        
        # 下一步热键
        hotkey_layout.addWidget(QLabel(self.lang['hotkey_next']))
        self.hotkey_next = QKeySequenceEdit()
        self.hotkey_next.setKeySequence(QKeySequence(Qt.Key.Key_Right))
        hotkey_layout.addWidget(self.hotkey_next)
        
        # 上一步热键
        hotkey_layout.addWidget(QLabel(self.lang['hotkey_prev']))
        self.hotkey_prev = QKeySequenceEdit()
        self.hotkey_prev.setKeySequence(QKeySequence(Qt.Key.Key_Left))
        hotkey_layout.addWidget(self.hotkey_prev)
        
        # 下一行热键
        hotkey_layout.addWidget(QLabel(self.lang['hotkey_line']))
        self.hotkey_line = QKeySequenceEdit()
        self.hotkey_line.setKeySequence(QKeySequence(Qt.Key.Key_Down))
        hotkey_layout.addWidget(self.hotkey_line)
        
        # 开始/暂停热键
        hotkey_layout.addWidget(QLabel(self.lang['hotkey_toggle']))
        self.hotkey_toggle = QKeySequenceEdit()
        self.hotkey_toggle.setKeySequence(QKeySequence(Qt.Key.Key_Space))
        hotkey_layout.addWidget(self.hotkey_toggle)
        
        hotkey_group.setLayout(hotkey_layout)
        layout.addWidget(hotkey_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def get_settings(self):
        """获取设置"""
        # 获取语言代码
        lang_codes = ['zh', 'en', 'ja', 'ko']
        selected_lang = lang_codes[self.language_combo.currentIndex()]
        
        return {
            'mode': self.mode_combo.currentText(),
            'advance': self.advance_combo.currentText(),
            'speed': self.speed_spin.value(),
            'language': selected_lang,
            'hotkeys': {
                'next': self.hotkey_next.keySequence().toString(),
                'prev': self.hotkey_prev.keySequence().toString(),
                'line': self.hotkey_line.keySequence().toString(),
                'toggle': self.hotkey_toggle.keySequence().toString(),
            }
        }
    
    def set_settings(self, settings):
        """设置值"""
        self.mode_combo.setCurrentText(settings.get('mode', self.lang['normal_mode']))
        self.advance_combo.setCurrentText(settings.get('advance', self.lang['advance_char']))
        self.speed_spin.setValue(settings.get('speed', 1000))
        
        # 设置热键
        hotkeys = settings.get('hotkeys', {})
        if 'next' in hotkeys:
            self.hotkey_next.setKeySequence(QKeySequence(hotkeys['next']))
        if 'prev' in hotkeys:
            self.hotkey_prev.setKeySequence(QKeySequence(hotkeys['prev']))
        if 'line' in hotkeys:
            self.hotkey_line.setKeySequence(QKeySequence(hotkeys['line']))
        if 'toggle' in hotkeys:
            self.hotkey_toggle.setKeySequence(QKeySequence(hotkeys['toggle']))


class StealthNovelSimple(QMainWindow):
    """StealthNovel 简化版主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 加载设置
        self.load_settings()
        
        # 当前语言
        self.current_lang = self.settings.get('language', 'zh')
        self.lang = LANGUAGES[self.current_lang]
        
        # 数据
        self.text_lines = []
        self.current_line = 0
        self.current_char = 0
        self.is_reading = False
        
        # 定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_advance)
        
        # 小窗口（用于任务栏/弹窗模式）
        self.small_window = None
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle(self.lang['title'])
        self.setMinimumSize(800, 600)
        
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout()
        
        # 标题
        self.title_label = QLabel(self.lang['main_title'])
        self.title_label.setFont(QFont("Microsoft YaHei", 20, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # 上传小说按钮
        self.upload_btn = QPushButton(self.lang['upload_btn'])
        self.upload_btn.setMinimumHeight(50)
        self.upload_btn.clicked.connect(self.upload_novel)
        button_layout.addWidget(self.upload_btn)
        
        # 设置按钮
        self.settings_btn = QPushButton(self.lang['settings_btn'])
        self.settings_btn.setMinimumHeight(50)
        self.settings_btn.clicked.connect(self.open_settings)
        button_layout.addWidget(self.settings_btn)
        
        layout.addLayout(button_layout)
        
        # 文件信息
        self.file_label = QLabel(self.lang['file_not_loaded'])
        self.file_label.setStyleSheet("color: gray; padding: 10px;")
        layout.addWidget(self.file_label)
        
        # 阅读区域
        reading_group = QGroupBox(self.lang['reading_area'])
        reading_layout = QVBoxLayout()
        
        # 进度信息
        self.progress_label = QLabel(f"{self.lang['progress']}: 0 / 0")
        reading_layout.addWidget(self.progress_label)
        
        # 文本显示
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Microsoft YaHei", 14))
        self.text_display.setMinimumHeight(300)
        reading_layout.addWidget(self.text_display)
        
        reading_group.setLayout(reading_layout)
        layout.addWidget(reading_group)
        
        # 控制按钮
        control_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton(self.lang['prev_btn'])
        self.prev_btn.clicked.connect(self.prev_step)
        self.prev_btn.setEnabled(False)
        control_layout.addWidget(self.prev_btn)
        
        self.start_btn = QPushButton(self.lang['start_btn'])
        self.start_btn.clicked.connect(self.toggle_reading)
        self.start_btn.setEnabled(False)
        control_layout.addWidget(self.start_btn)
        
        self.next_btn = QPushButton(self.lang['next_btn'])
        self.next_btn.clicked.connect(self.next_step)
        self.next_btn.setEnabled(False)
        control_layout.addWidget(self.next_btn)
        
        self.reset_btn = QPushButton(self.lang['reset_btn'])
        self.reset_btn.clicked.connect(self.reset_progress)
        self.reset_btn.setEnabled(False)
        control_layout.addWidget(self.reset_btn)
        
        layout.addLayout(control_layout)
        
        # 说明
        self.help_text = QLabel(self.lang['help_text'])
        self.help_text.setWordWrap(True)
        self.help_text.setStyleSheet("color: #666; padding: 10px; background: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.help_text)
        
        central_widget.setLayout(layout)
        
        # 应用样式
        self.setStyleSheet("""
            QPushButton {
                background-color: #E6F4EA;
                border: 2px solid #000;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d4e8dc;
            }
            QPushButton:pressed {
                background-color: #c2dcc8;
            }
            QPushButton:disabled {
                background-color: #f0f0f0;
                color: #999;
                border-color: #ccc;
            }
            QGroupBox {
                border: 2px solid #E6F4EA;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
    
    def upload_novel(self):
        """上传小说"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.lang['select_file'],
            "",
            self.lang['text_files']
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析文本
                self.text_lines = [line.strip() for line in content.split('\n')]
                self.current_line = 0
                self.current_char = 0
                
                # 更新界面
                file_name = Path(file_path).name
                self.file_label.setText(
                    f"{self.lang['loaded_file']}: {file_name} ({len(self.text_lines)} {self.lang['lines']})"
                )
                self.file_label.setStyleSheet("color: green; padding: 10px;")
                
                # 启用按钮
                self.start_btn.setEnabled(True)
                self.prev_btn.setEnabled(True)
                self.next_btn.setEnabled(True)
                self.reset_btn.setEnabled(True)
                
                # 显示第一行
                self.update_display()
                
                QMessageBox.information(self, self.lang['success'], self.lang['load_success'])
                
            except Exception as e:
                QMessageBox.critical(self, self.lang['error'], f"{self.lang['load_failed']}: {str(e)}")
    
    def open_settings(self):
        """打开设置"""
        dialog = SettingsDialog(self, self.current_lang)
        dialog.set_settings(self.settings)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            old_lang = self.current_lang
            self.settings = dialog.get_settings()
            self.current_lang = self.settings.get('language', 'zh')
            self.save_settings()
            
            # 如果语言改变，提示重启
            if old_lang != self.current_lang:
                msg = {
                    'zh': '语言已更改为 {}。请重启程序以应用新语言。',
                    'en': 'Language changed to {}. Please restart the application.',
                    'ja': '言語が {} に変更されました。アプリケーションを再起動してください。',
                    'ko': '언어가 {}로 변경되었습니다. 응용 프로그램을 다시 시작하십시오.'
                }
                lang_names = {
                    'zh': '中文', 'en': 'English', 'ja': '日本語', 'ko': '한국어'
                }
                QMessageBox.information(
                    self, 
                    self.lang['success'], 
                    msg.get(old_lang, msg['en']).format(lang_names.get(self.current_lang, ''))
                )
            else:
                QMessageBox.information(self, self.lang['success'], self.lang['settings_saved'])
    
    def toggle_reading(self):
        """开始/停止阅读"""
        if not self.is_reading:
            # 开始阅读
            self.is_reading = True
            self.start_btn.setText(self.lang['pause_btn'])
            
            # 根据模式切换显示
            mode = self.settings['mode']
            if mode == self.lang['taskbar_mode']:
                self.start_taskbar_mode()
            elif mode == self.lang['popup_mode']:
                self.start_popup_mode()
            else:
                # 正常窗口模式，启动自动推进
                self.timer.start(self.settings['speed'])
        else:
            # 停止阅读
            self.is_reading = False
            self.start_btn.setText(self.lang['start_btn'])
            self.timer.stop()
            
            # 关闭小窗口
            if self.small_window:
                self.small_window.close()
                self.small_window = None
    
    def start_taskbar_mode(self):
        """启动任务栏标题模式"""
        if not self.small_window:
            self.small_window = QWidget()
            self.small_window.setWindowTitle("StealthNovel")
            self.small_window.setFixedSize(1, 1)
            self.small_window.move(0, 0)
        
        self.small_window.show()
        self.timer.start(self.settings['speed'])
        self.update_taskbar_title()
    
    def start_popup_mode(self):
        """启动右下角弹窗模式"""
        if not self.small_window:
            self.small_window = QWidget()
            self.small_window.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.WindowStaysOnTopHint
            )
            self.small_window.setStyleSheet("""
                QWidget {
                    background-color: #E6F4EA;
                    border: 2px solid #000;
                    border-radius: 10px;
                    padding: 15px;
                }
            """)
            
            layout = QVBoxLayout()
            self.popup_label = QLabel()
            self.popup_label.setFont(QFont("Microsoft YaHei", 12))
            self.popup_label.setWordWrap(True)
            layout.addWidget(self.popup_label)
            self.small_window.setLayout(layout)
            
            # 定位到右下角
            screen = QApplication.primaryScreen().geometry()
            self.small_window.setFixedSize(350, 120)
            x = screen.width() - 350 - 20
            y = screen.height() - 120 - 50
            self.small_window.move(x, y)
        
        self.small_window.show()
        self.timer.start(self.settings['speed'])
        self.update_popup_text()
    
    def auto_advance(self):
        """自动推进"""
        self.next_step()
    
    def next_step(self):
        """下一步"""
        if not self.text_lines:
            return
        
        if self.settings['advance'] == self.lang['advance_char']:
            # 逐字推进
            if self.current_line < len(self.text_lines):
                current_text = self.text_lines[self.current_line]
                if self.current_char + 1 < len(current_text):
                    self.current_char += 1
                else:
                    # 移到下一行
                    if self.current_line + 1 < len(self.text_lines):
                        self.current_line += 1
                        self.current_char = 0
        else:
            # 逐行推进
            if self.current_line + 1 < len(self.text_lines):
                self.current_line += 1
                self.current_char = 0
        
        self.update_display()
    
    def prev_step(self):
        """上一步"""
        if not self.text_lines:
            return
        
        if self.settings['advance'] == self.lang['advance_char']:
            # 逐字后退
            if self.current_char > 0:
                self.current_char -= 1
            else:
                # 移到上一行末尾
                if self.current_line > 0:
                    self.current_line -= 1
                    self.current_char = max(0, len(self.text_lines[self.current_line]) - 1)
        else:
            # 逐行后退
            if self.current_line > 0:
                self.current_line -= 1
                self.current_char = 0
        
        self.update_display()
    
    def reset_progress(self):
        """重置进度"""
        self.current_line = 0
        self.current_char = 0
        self.update_display()
        QMessageBox.information(self, self.lang['success'], self.lang['progress_reset'])
    
    def update_display(self):
        """更新显示"""
        if not self.text_lines or self.current_line >= len(self.text_lines):
            return
        
        # 获取当前文本
        current_text = self.text_lines[self.current_line][self.current_char:]
        
        # 更新主窗口
        self.text_display.setPlainText(current_text)
        self.progress_label.setText(
            f"{self.lang['progress']}: {self.current_line + 1} / {len(self.text_lines)}, "
            f"字符 {self.current_char}"
        )
        
        # 更新任务栏/弹窗
        if self.is_reading:
            if self.settings['mode'] == self.lang['taskbar_mode']:
                self.update_taskbar_title()
            elif self.settings['mode'] == self.lang['popup_mode']:
                self.update_popup_text()
    
    def update_taskbar_title(self):
        """更新任务栏标题"""
        if self.small_window and self.text_lines:
            current_text = self.text_lines[self.current_line][self.current_char:]
            # 限制长度
            display_text = current_text[:40] if len(current_text) > 40 else current_text
            self.small_window.setWindowTitle(display_text)
    
    def update_popup_text(self):
        """更新弹窗文本"""
        if self.small_window and hasattr(self, 'popup_label') and self.text_lines:
            current_text = self.text_lines[self.current_line][self.current_char:]
            # 限制长度
            display_text = current_text[:100] if len(current_text) > 100 else current_text
            self.popup_label.setText(display_text)
    
    def load_settings(self):
        """加载设置"""
        settings_file = Path("stealth_settings.json")
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            except:
                self.settings = self.get_default_settings()
        else:
            self.settings = self.get_default_settings()
    
    def get_default_settings(self):
        """获取默认设置"""
        return {
            'mode': '正常窗口',
            'advance': '逐字',
            'speed': 1000,
            'language': 'zh',
            'hotkeys': {
                'next': 'Right',
                'prev': 'Left',
                'line': 'Down',
                'toggle': 'Space'
            }
        }
    
    def save_settings(self):
        """保存设置"""
        try:
            with open("stealth_settings.json", 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def keyPressEvent(self, event):
        """键盘事件"""
        # 获取自定义热键
        hotkeys = self.settings.get('hotkeys', {})
        key_seq = QKeySequence(event.key()).toString()
        
        if key_seq == hotkeys.get('next', 'Right') or event.key() == Qt.Key.Key_Right:
            self.next_step()
        elif key_seq == hotkeys.get('prev', 'Left') or event.key() == Qt.Key.Key_Left:
            self.prev_step()
        elif key_seq == hotkeys.get('line', 'Down') or event.key() == Qt.Key.Key_Down:
            # 强制逐行推进
            old_advance = self.settings['advance']
            self.settings['advance'] = self.lang['advance_line']
            self.next_step()
            self.settings['advance'] = old_advance
        elif key_seq == hotkeys.get('toggle', 'Space') or event.key() == Qt.Key.Key_Space:
            if self.start_btn.isEnabled():
                self.toggle_reading()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用 Fusion 风格
    
    window = StealthNovelSimple()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
