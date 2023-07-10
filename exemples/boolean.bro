nulo principal () {
    inteiro a;
    real b;

    a = 1;
    b = 0;

    se (a) {
        escrever("variável a é verdadeira, seu valor:");
        escrever(a);
    } senao {
        escrever("variável a é falsa, seu valor:");
        escrever(a);
    }

    se (b) {
        escrever("variável b é verdadeira, seu valor:");
        escrever(b);
    } senao {
        escrever("variável b é falsa, seu valor:");
        escrever(b);
    }

    se (a && b) {
        escrever("a && b é verdadeira, seu valor:");
        escrever(a && b);
    } senao {
        escrever("a && b é falsa, seu valor:");
        escrever(a && b);
    }

    se (a || b) {
        escrever("a || b é verdadeira, seu valor:");
        escrever(a || b);
    } senao {
        escrever("a || b é falsa, seu valor:");
        escrever(a || b);
    }

    escrever("a + b:");
    escrever(a+b);
}
