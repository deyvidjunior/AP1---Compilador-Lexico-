def main():
    # Test program
    source = """program exemplo1;
var num: integer;
begin
    num := 10;
    write(num)
end."""

    try:
        parser = Parser(source)
        parser.programa()
        print(f"\n{parser.lexer.line} linhas analisadas, programa sintaticamente correto.")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()