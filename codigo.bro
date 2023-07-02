/* Esse é um programa em BroLang */
nulo principal() {
    inteiro a, b;
    real c;
    char d;

    a = 1;
    b = 3;
    ler(c);

    enquanto (a < b) {
        a = a + 1;
        se (a > b) {
            escrever("a maior que b");
        } senao {
            escrever("a menor que b");
        }
    }
}