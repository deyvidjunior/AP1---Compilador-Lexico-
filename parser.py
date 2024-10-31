from lexer import Lexer, Token

class Parser:
    def __init__(self, source):
        self.lexer = Lexer(source)
        self.current_token = self.lexer.get_next_token()

    def error(self, expected):
        raise Exception(f"Erro sintático: Esperado [{expected}] encontrado [{self.current_token.type}] na linha {self.current_token.line}")

    def consume(self, token_type):
        if self.current_token.type == token_type:
            print(f"Linha: {self.current_token.line} - atomo: {self.current_token.type} lexema: {self.current_token.lexeme}")
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def programa(self):
        self.consume('PROGRAM')
        self.consume('IDENTIF')
        if self.current_token.type == 'ABRE_PAR':
            self.consume('ABRE_PAR')
            self.lista_identificadores()
            self.consume('FECHA_PAR')
        self.consume('PONTO_VIRG')
        self.bloco()
        self.consume('PONTO')

    def bloco(self):
        if self.current_token.type == 'VAR':
            self.declaracoes_variaveis()
        self.comando_composto()

    def declaracoes_variaveis(self):
        self.consume('VAR')
        self.declaracao()
        while self.current_token.type == 'PONTO_VIRG':
            self.consume('PONTO_VIRG')
            if self.current_token.type == 'IDENTIF':
                self.declaracao()
        self.consume('PONTO_VIRG')

    def declaracao(self):
        self.lista_identificadores()
        self.consume('DOIS_PONTOS')
        self.tipo()

    def lista_identificadores(self):
        self.consume('IDENTIF')
        while self.current_token.type == 'VIRGULA':
            self.consume('VIRGULA')
            self.consume('IDENTIF')

    def tipo(self):
        if self.current_token.type in ['INTEGER', 'BOOLEAN']:
            self.consume(self.current_token.type)
        else:
            self.error('tipo')

    def comando_composto(self):
        self.consume('BEGIN')
        self.comando()
        while self.current_token.type == 'PONTO_VIRG':
            self.consume('PONTO_VIRG')
            if self.current_token.type != 'END':
                self.comando()
        self.consume('END')

    def comando(self):
        if self.current_token.type == 'IDENTIF':
            self.atribuicao()
        elif self.current_token.type == 'READ':
            self.comando_entrada()
        elif self.current_token.type == 'WRITE':
            self.comando_saida()
        elif self.current_token.type == 'IF':
            self.comando_if()
        elif self.current_token.type == 'WHILE':
            self.comando_while()
        elif self.current_token.type == 'BEGIN':
            self.comando_composto()
        else:
            self.error('comando')

    def atribuicao(self):
        self.consume('IDENTIF')
        self.consume('ATRIB')
        self.expressao()

    def comando_if(self):
        self.consume('IF')
        self.expressao()
        self.consume('THEN')
        self.comando()
        if self.current_token.type == 'ELSE':
            self.consume('ELSE')
            self.comando()

    def comando_while(self):
        self.consume('WHILE')
        self.expressao()
        self.consume('DO')
        self.comando()

    def comando_entrada(self):
        self.consume('READ')
        self.consume('ABRE_PAR')
        self.lista_identificadores()
        self.consume('FECHA_PAR')

    def comando_saida(self):
        self.consume('WRITE')
        self.consume('ABRE_PAR')
        self.expressao()
        while self.current_token.type == 'VIRGULA':
            self.consume('VIRGULA')
            self.expressao()
        self.consume('FECHA_PAR')

    def expressao(self):
        self.expressao_simples()
        if self.current_token.type in ['LT', 'LE', 'EQ', 'NE', 'GT', 'GE']:
            self.operador_relacional()
            self.expressao_simples()

    def operador_relacional(self):
        if self.current_token.type in ['LT', 'LE', 'EQ', 'NE', 'GT', 'GE']:
            self.consume(self.current_token.type)
        else:
            self.error('operador relacional')

    def expressao_simples(self):
        if self.current_token.type in ['PLUS', 'MINUS']:
            self.consume(self.current_token.type)
        self.termo()
        while self.current_token.type in ['PLUS', 'MINUS', 'OR']:
            self.consume(self.current_token.type)
            self.termo()

    def termo(self):
        self.fator()
        while self.current_token.type in ['MULT', 'DIV', 'MOD', 'AND']:
            self.consume(self.current_token.type)
            self.fator()

    def fator(self):
        if self.current_token.type == 'IDENTIF':
            self.consume('IDENTIF')
        elif self.current_token.type == 'NUM':
            self.consume('NUM')
        elif self.current_token.type == 'ABRE_PAR':
            self.consume('ABRE_PAR')
            self.expressao()
            self.consume('FECHA_PAR')
        elif self.current_token.type in ['TRUE', 'FALSE']:
            self.consume(self.current_token.type)
        elif self.current_token.type == 'NOT':
            self.consume('NOT')
            self.fator()
        else:
            self.error('fator')