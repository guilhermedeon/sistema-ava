# Desafio Final:

Para seguir com o desafio sera necessario ter implementado o exercicio do dia 4.
Então vamos lá:

1. Criar um atributo 'active' do tipo booleano no  modelo curso que ira indicar se o curso esta ativo ou não

2. criar um novo modelo chamado aluno com os seguintes atributos id, nome, sobrenome, email, idade, cpf e id_curso(obs. o aluno so poderá se associar a um único curso)

3. Implementar o CRUD para o modelo de aluno.

4. No metodo remover aluno, verificar se o curso que o aluno tem vinculo está ativo, se sim, não permitir remover o aluno a menos que o status do curso seja alterado pra false.
Caso aluno esteja vinculado a um curso ativo, retornar a seguinte mensagem: Nao foi possivel excluir o aluno, pois ele esta vinculado a um curso ativo. o status code pode ser um 400.
