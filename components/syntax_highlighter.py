from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import QRegularExpression

class JsonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        # Keys
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#9cdcfe"))
        self.rules.append(
            (QRegularExpression(r'"[^"]*"(?=\s*:)'), key_format)
        )

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#ce9178"))
        self.rules.append(
            (QRegularExpression(r'"([^"\\]|\\.)*"'), string_format)
        )

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#b5cea8"))
        self.rules.append(
            (QRegularExpression(r'\b-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?\b'),
             number_format)
        )

        # Booleans
        bool_format = QTextCharFormat()
        bool_format.setForeground(QColor("#569cd6"))
        self.rules.append(
            (QRegularExpression(r'\b(true|false|null)\b'), bool_format)
        )

        # Braces / brackets
        brace_format = QTextCharFormat()
        brace_format.setForeground(QColor("#ffd700"))
        self.rules.append(
            (QRegularExpression(r'[{}\[\]]'), brace_format)
        )

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    fmt
                )