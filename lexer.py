class Token:
    def __init__(self, type, lexeme, line, value=None):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.value = value

class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.current_char = self.source[0] if len(self.source) > 0 else None
        
        # Reserved words
        self.keywords = {
            'begin': 'BEGIN', 'boolean': 'BOOLEAN', 'div': 'DIV',
            'do': 'DO', 'else': 'ELSE', 'end': 'END', 'false': 'FALSE',
            'if': 'IF', 'integer': 'INTEGER', 'mod': 'MOD', 'program': 'PROGRAM',
            'read': 'READ', 'then': 'THEN', 'true': 'TRUE', 'not': 'NOT',
            'var': 'VAR', 'while': 'WHILE', 'write': 'WRITE'
        }

    def advance(self):
        self.position += 1
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]

    def peek(self):
        peek_pos = self.position + 1
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
            self.advance()

    def skip_comment(self):
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char and self.current_char != '\n':
                self.advance()
            if self.current_char == '\n':
                self.line += 1
                self.advance()
        elif self.current_char == '(' and self.peek() == '*':
            self.advance()  # Skip (
            self.advance()  # Skip *
            while self.current_char:
                if self.current_char == '*' and self.peek() == ')':
                    self.advance()  # Skip *
                    self.advance()  # Skip )
                    break
                if self.current_char == '\n':
                    self.line += 1
                self.advance()
        elif self.current_char == '{':
            while self.current_char and self.current_char != '}':
                if self.current_char == '\n':
                    self.line += 1
                self.advance()
            self.advance()  # Skip }

    def get_identifier(self):
        lexeme = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            lexeme += self.current_char
            self.advance()

        if len(lexeme) > 20:
            raise Exception(f"Error: Identifier '{lexeme}' exceeds maximum length of 20 characters at line {self.line}")

        token_type = self.keywords.get(lexeme.lower(), 'IDENTIF')
        return Token(token_type, lexeme, self.line)

    def get_number(self):
        number = ''
        while self.current_char and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return Token('NUM', number, self.line, int(number))

    def get_next_token(self):
        while self.current_char:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Skip comments
            if (self.current_char == '/' and self.peek() == '/') or \
               (self.current_char == '(' and self.peek() == '*') or \
               self.current_char == '{':
                self.skip_comment()
                continue

            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.get_identifier()

            # Numbers
            if self.current_char.isdigit():
                return self.get_number()

            # Two-character operators
            if self.current_char == ':' and self.peek() == '=':
                token = Token('ATRIB', ':=', self.line)
                self.advance()
                self.advance()
                return token

            if self.current_char == '<' and self.peek() == '=':
                token = Token('LE', '<=', self.line)
                self.advance()
                self.advance()
                return token

            if self.current_char == '>' and self.peek() == '=':
                token = Token('GE', '>=', self.line)
                self.advance()
                self.advance()
                return token

            if self.current_char == '<' and self.peek() == '>':
                token = Token('NE', '<>', self.line)
                self.advance()
                self.advance()
                return token

            # Single-character operators and delimiters
            simple_tokens = {
                '+': 'PLUS',
                '-': 'MINUS',
                '*': 'MULT',
                '/': 'DIV',
                '=': 'EQ',
                '<': 'LT',
                '>': 'GT',
                '(': 'ABRE_PAR',
                ')': 'FECHA_PAR',
                ';': 'PONTO_VIRG',
                '.': 'PONTO',
                ',': 'VIRGULA',
                ':': 'DOIS_PONTOS'
            }

            if self.current_char in simple_tokens:
                token = Token(simple_tokens[self.current_char], self.current_char, self.line)
                self.advance()
                return token

            raise Exception(f"Error: Invalid character '{self.current_char}' at line {self.line}")

        return Token('EOF', '', self.line)