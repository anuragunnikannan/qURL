import json
from pydoc import text
from pydoc import text
import xml.etree.ElementTree as ET
from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat
from pygments.lexer import Lexer
from pygments.lexers import (
    HtmlLexer,
    JsonLexer,
    TextLexer,
    XmlLexer,
    guess_lexer,
)
from pygments.styles import get_style_by_name
from pygments.token import Token
from pygments.util import ClassNotFound


class DynamicHighlighter(QSyntaxHighlighter):

	def __init__(self, document, style_name="monokai"):
		super().__init__(document)
		self.lexer = JsonLexer()
		self.detected_mime = "application/json"
		self.detected_name = "json"
		self.styles = self._build_style_map(style_name)

	def _build_style_map(self, style_name):
		style = get_style_by_name(style_name)
		mapping = {}
		for token, opts in style:
			fmt = QTextCharFormat()
			if opts["color"]:
				fmt.setForeground(QColor(f"#{opts['color']}"))
			if opts["bold"]:
				fmt.setFontWeight(QFont.Weight.Bold)
			if opts["italic"]:
				fmt.setFontItalic(True)
			mapping[token] = fmt
		return mapping

	def detect_and_update(self, text: str) -> tuple[str, str]:
		"""Detects format from text and re-highlights the document."""
		stripped = text.strip()
		if not stripped:
			self.lexer = TextLexer()
			self.detected_mime = "text/plain"
			self.detected_name = "raw"
			self.rehighlight()
			return self.detected_name, self.detected_mime

		# 1. Fast JSON heuristic
		if (stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[") and stripped.endswith("]")):
			try:
				json.loads(stripped)
				self.lexer = JsonLexer()
				self.detected_mime = "application/json"
				self.detected_name = "JSON"
				self.rehighlight()
				return self.detected_name, self.detected_mime
			except Exception:
				pass

		# 2. Fast XML/HTML heuristic
		if stripped.startswith("<") and stripped.endswith(">"):
			try:
				ET.fromstring(stripped)
				self.lexer = XmlLexer()
				self.detected_mime = "application/xml"
				self.detected_name = "XML"
				self.rehighlight()
				return self.detected_name, self.detected_mime
			except Exception:
				self.lexer = HtmlLexer()
				self.detected_mime = "text/html"
				self.detected_name = "HTML"
				self.rehighlight()
				return self.detected_name, self.detected_mime

		# 3. Fallback to Pygments automatic guessing
		try:
			self.lexer = guess_lexer(stripped)
			self.detected_name = self.lexer.name
			# Map common lexer aliases to MIME types
			self.detected_mime = (
				getattr(self.lexer, "mimetypes", ["text/plain"])[0]
				if self.lexer.mimetypes
				else "text/plain"
			)
		except ClassNotFound:
			self.lexer = TextLexer()
			self.detected_mime = "text/plain"
			self.detected_name = "raw"

		self.rehighlight()
		return self.detected_name, self.detected_mime

	def highlightBlock(self, text: str):
		if not text or not self.lexer:
			return

		# Process tokens for this line
		try:
			tokens = self.lexer.get_tokens_unprocessed(text)
		except Exception:
			tokens = []

		for index, token_type, value in tokens:
			# Resolve token style by climbing up token hierarchy if not explicitly defined
			fmt = self.styles.get(token_type)
			curr = token_type
			while fmt is None and curr.parent:
				curr = curr.parent
				fmt = self.styles.get(curr)

			if fmt:
				self.setFormat(index, len(value), fmt)

	def set_language(self, language:str):
		lang = language.lower()
		if "json" in lang:
			self.lexer = JsonLexer()
		elif "html" in lang:
			self.lexer = HtmlLexer()
		elif "xml" in lang:
			self.lexer = XmlLexer()
		else:
			self.lexer = TextLexer()

		self.rehighlight()
