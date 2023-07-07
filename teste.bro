nulo principal () {
    inteiro a, b, c;
    inteiro teste;
    char teste1;
    real nota;

    a = -3 + -5 * ( 3 + 2 );
    b = 3 + 5 * ( 3 + 2 );
    teste = a + b;
    teste1 = "a er we wer ewr";
    nota = 10.5 / 2.5;
    c = 4 > 2;
    escrever(a);
    escrever(b);
    escrever("teste");
    escrever(20);
    escrever(20.5);
    escrever(5 * 5 / 2 + 3 - 1);

    ler(a);
    escrever(a);
    escrever(!0);

    se ( a > b ) {
        escrever(a);
    } senao {
        escrever(b);
    }

    /* teste de comentario */

    enquanto ( a > 0 ) {
        escrever(a);
        a = a - 1;

        se ( a == 2 ) {
            escrever("a eh igual a 2");
        }
    }
}