1 - Este código tem o objetivo de raspar dados nas lojas mobile Google Play e App Store, fazendo análise de sentimentos e tópicos de avaliações para aplicativos da Google Play Store e da Apple App Store.

2 - Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina. Os scripts utilizam bibliotecas como pandas, matplotlib, nltk e sklearn. Você pode instalar todas as dependências necessárias utilizando o comando:

    2.1 - pip install pandas matplotlib nltk scikit-learn

    2.2 - Execute os arquivos scraper_android.py e scraper_ios.py com os comandos:

        2.2.1 - python scraper_android.py
        2.2.2 -  pyton scraper_ios.py
    
    2.3 - Execute os scripts de análise de sentimento

        2.3.1 - python analysis_vivo_easy_appsstore.py
        2.3.2 - python analysis_vivo_easy_googleplay.py

3 - Rodando localmente servidor Flask para exibir todos gráficos

4 - Pré-requisitos

Certifique-se de ter o Flask instalado. Você pode instalar usando o pip:

    4.1 - pip install flask

5 - Garanta de que o arquivo CSV gerado pelo código scraper esteja no mesmo diretório que o app.py.

6 - Execute o servidor Flask usando o comando:
    6.1 - python app.py
    6.2 - Acesse através da rota exibida no termial - http://127.0.0.1:5000
