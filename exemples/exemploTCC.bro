nulo principal () {
    real x, media, qnt;
    inteiro cont;

    qnt = 5;

    cont = 0;
    media = 0;

    enquanto (cont < qnt) {
        escrever("Valor");
        escrever(cont);
        ler(x);
        media = media + x;
        cont = cont + 1;
    }

    escrever("\n");
    escrever("Soma total:");
    escrever(media);
    escrever("Resultado da media:");
    escrever(media / qnt);
}