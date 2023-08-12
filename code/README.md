# Uso
Utilize o arquivo requirements.txt para instalar as dependências necessárias.
>> pip install -r ../requirements.txt

Utilizando o uvicorn, inicialize a aplicação com o seguinte comando:
>> uvicorn main:app --reload

A aplicação utiliza o banco de dados existente no local:
>> .code/db.sqlite3

# Opcional
O arquivo db.sqlite3 é gerado automaticamente pela aplicação durante a primeira execução.

Como alternativa, temos na pasta ../sqlite_exemplo um arquivo db.sqlite3 pré populado com alguns valores para teste.
