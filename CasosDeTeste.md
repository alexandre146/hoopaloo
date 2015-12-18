## Testes Automáticos ##

Os testes automáticos estão em duas categorias: testes com unittest.

### Testes com unittest ###

  * Cadastro de tutores
  * Cadastro de alunos
  * Cadastro de exercícios
  * Criação de submissão
  * Atualização de atributos de alunos
  * Verificação de atributos de alunos (número de submissões, exercícios pendentes, exercícios entregues e não entregies, etc.) após cadastro de exercícios e diversas submissões.
  * Consultas diversas sobre os modelos do BD

### Testes On-Line ###

Os testes "on-line" são os testes realizados no próprio sistema, simulando situações de uso.

#### Cenário 1 ####
  * Ator: qualquer usuário
  * Página: login

  * Ação: Digitar o login incorretamente
  * esultado esperado: página de login do hoopaloo com mensagem de erro ("Invalid Acess")
  * esultado obtido: página de login do hoopaloo com mensagem de erro ("Invalid Acess")

  * Ação: Digitar a senha incorretamente
  * Resultado esperado: página de login do hoopaloo com mensagem de erro ("Invalid Acess")
  * Resultado obtido: página de login do hoopaloo com mensagem de erro ("Invalid Acess")

  * Ação: Digitar login e senha corretamente
  * Resultado esperado: página inicial do usuário
  * Resultado obtido: página inicial do usuário

  * Ação: Usuário esqueceu a senha e clica em "Forgot your password?"
  * Resultado esperado: página que pede o email
  * Resultado obtido: página que pede o email

#### Cenário 2 ####
  * Ator: qualquer usuário
  * Página: forgot password

  * <font color='red'>Ação: Usuário informa email<br>
<ul><li>Resultado esperado: mensagem ("Please check your email. If you did not receive any message, check your spam folder.") e que chegue um email em sua caixa de emails<br>
</li><li>Resultado obtido: mensagem ("Please check your email. If you did not receive any message, check your spam folder.") e <a href='https://code.google.com/p/hoopaloo/issues/detail?id='>https://code.google.com/p/hoopaloo/issues/detail?id=</a>: o email não é enviado. CORRIGIDO!!!!!!</font></li></ul>

#### Cenário 3 ####
  * Ator: professor (superusuário)
  * Página: página inicial de professor (tabela com todos os alunos da turma daquele professor)

  * Ação: clicar no link "Register Students" no menu Users
  * Resultado esperado: redirecionamento par

  * Ação: clicar no link "Register Assistants" no menu Users
  * Resultado esperado: redirecionamento para a página de cadastro de tutores
  * resultado obtido: redirecionamento para a página de cadastro de tutores

  * Ação: clicar no link "Assign Students to Assistants" no menu Users
  * Resultado esperado: redirecionamento para a página de atribuição de alunos a tutores
  * Resultado obtido: redirecionamento para a página de atribuição de alunos a tutores

  * Ação: clicar no link "Assign Students to Assistants" no menu Users
  * Resultado esperado: redirecionamento para a página de atribuição de alunos a tutores
  * Resultado obtido: redirecionamento para a página de atribuição de alunos a tutores

  * Ação: clicar no link "User Details" no menu Users
  * Resultado esperado: redirecionamento para a página de visualização de  informações dos usuários (email ultima vez que logou, username, data de cadastro)
  * Resultado obtido: redirecionamento para a página de visualização de  informações dos usuários (email ultima vez que logou, username, data de cadastro)

  * Ação: clicar no link "Actions Log of System" no menu Users
  * Resultado esperado: redirecionamento para a página que contém as últimas 100 ações dos usuários no hoopaloo
  * Resultado obtido: redirecionamento para a página que contém as últimas 100 ações dos usuários no hoopaloo

  * Ação: clicar no link "New Exercise" no menu Exercise
  * Resultado esperado: redirecionamento para a página de cadastro de exercício
  * Resultado obtido: redirecionamento para a página de cadastro de exercício

  * Ação: clicar no link "List Exercises" no menu Exercise
  * Resultado esperado: redirecionamento para a página que lista todos os exercícios
  * Resultado obtido: redirecionamento para a página que lista todos os exercícios

  * Ação: clicar no link "List Tests" no menu Exercise
  * Resultado esperado: redirecionamento parlista todos os alunos cadastradosa a página que lista todos os testes referentes aos exercícios cadastrados
  * Resultado obtido: redirecionamento para a página que lista todos os testes referentes aos exercícios cadastrados

  * Ação: clicar no link "All Students" no menu Views
  * Resultado esperado: redirecionamento para a página que lista todos os alunos cadastrados
  * Resultado obtido: redirecionamento para a página que lista todos os alunos cadastrados

  * Ação: clicar no link "Assistants - Students" no menu Views
  * Resultado esperado: redirecionamento para a página que lista as associações entre tutores e alunos
  * Resultado obtido: redirecionamento para a página que lista as associações entre tutores e alunos

  * Ação: clicar no link "Change Password" no menu principal
  * Resultado esperado: redirecionamento para a página de mudança de senha
  * Resultado obtido: redirecionamento para a página de mudança de senha

  * Ação: clicar no link "Logout" no menu principal
  * Resultado esperado: redirecionamento para a página de login com a mensagem de logout ("You are unlogged")
  * Resultado obtido: redirecionamento para a página de login com a mensagem de logout ("You are unlogged")

#### Cenário 4 ####
  * Ator: professor (superusuário)
  * Página: página de mudança de senha

  * Ação: inserir uma nova senha
  * Resultado esperado: redirecionamento para a pagina de login informando que a senha foi alterada
  * Resultado obtido: redirecionamento para a pagina de login informando que a senha foi alterada

  * Página: login página inicial do usuário
  * Ação: inserir a senha antiga
  * Resultado esperado: página de login do hoopaloo com mensagem de erro ("Invalid Acess")
  * Resultado obtido: página de login do hoopaloo com mensagem de erro ("Invalid Acess")

  * Página: login
  * Ação: inserir a senha nova
  * Resultado esperado: página inicial do usuário
  * Resultado obtido: página inicial do usuário

#### Cenário 5 ####
  * Ator: professor (superusuário)
  * Página: cadastro de alunos

  * Ação: submeter o cadastro com o campo vazio
  * Resultado esperado: mensagem de erro ("This field is required.")
  * Resultado obtido: mensagem de erro ("This field is required.")

  * Ação: submeter o cadastro com apenas um aluno
  * Resultado esperado: cadastro efetuado com sucesso e mensagem ("The students were added successfully."), email enviado para o usuário cadastrado
  * Resultado obtido:  cadastro efetuado com sucesso e mensagem ("The students were added successfully."), email enviado para o usuário cadastrado

  * Ação: submeter o cadastro com varios alunos, todos corretos
  * Resultado esperado: cadastro efetuado com sucesso e mensagem ("The students were added successfully."), email enviado para os usuários cadastrados
  * Resultado obtido:  cadastro efetuado com sucesso e mensagem ("The students were added successfully."), email enviado para os usuários cadastrados

  * Ação: submeter o cadastro com varios alunos, alguns incorretos
  * Resultado esperado: cadastro efetuado com sucesso e mensagem ("The students bellow are not registered. Review usernames, studentID and emails for them."), email enviado para os usuários cadastrados e permanece no campo os alunos que não foram registrados
  * Resultado obtido:  cadastro efetuado com sucesso, mas mensagem ("The students bellow are not registered. Review usernames, studentID and emails for them."), email enviado para os usuários cadastrados e permanece no campo os alunos que não foram registrados

  * Ação: submeter o cadastro com o campo vazio
  * Resultado esperado: mensagem de erro ("This field is required.")
  * Resultado obtido: mensagem de erro ("This field is required.")

#### Cenário 6 ####
  * Ator: professor (superusuário)
  * Página: cadastro de tutores

  * Ação: submeter o cadastro com o campo vazio
  * Resultado esperado: mensagem de erro ("This field is required.")
  * Resultado obtido: mensagem de erro ("This field is required.")

  * Ação: submeter o cadastro com apenas um tutor
  * Resultado esperado: cadastro efetuado com sucesso e mensagem ("The assistants were added successfully."), email enviado para o usuário cadastrado
  * Resultado obtido:  cadastro efetuado com sucesso e mensagem ("The assistants were added successfully."), email enviado para o usuário cadastrado

  * Ação: submeter o cadastro com varios tutores, todos corretos
  * Resultado esperado: cadastro efetuado com sucesso e mensagem ("The assistants were added successfully."), email enviado para os usuários cadastrados
  * Resultado obtido:  cadastro efetuado com sucesso e mensagem ("The assistants were added successfully."), email enviado para os usuários cadastrados

  * Ação: submeter o cadastro com varios tutores, alguns incorretos
  * Resultado esperado: cadastro efetuado com sucesso e mensagem ("The assistants bellow are not registered. Review usernames, studentID and emails for them."), email enviado para os usuários cadastrados e permanece no campo os tutores que não foram registrados
  * Resultado obtido:  cadastro efetuado com sucesso, mas mensagem ("The assistants bellow are not registered. Review usernames, studentID and emails for them."), email enviado para os usuários cadastrados e permanece no campo os tutores que não foram registrados

#### Cenário 7 ####
  * Ator: professor (superusuário)
  * Página: atribuição de alunos a tutores

  * <font color='red'>Ação: submeter o cadastro com o campo vazio<br>
<ul><li>Resultado esperado: mensagem de erro ("This field is required.")<br>
</li><li>Resultado obtido: <a href='https://code.google.com/p/hoopaloo/issues/detail?id='>https://code.google.com/p/hoopaloo/issues/detail?id=</a>: página de erro (Server Error (500)) CORRIGIDO!!!! </font></li></ul>

  * Ação: submeter o cadastro com apenas uma atribuiçãouso.

  * Resultado esperado: atribuição efetuada com sucesso e mensagem ("The assign students to assistant(s) was done sucessfully.")
  * Resultado obtido:  atribuição efetuada com sucesso e mensagem ("The assign students to assistant(s) was done sucessfully.")

  * Ação: submeter o cadastro com varias atribuições, todas corretas
  * Resultado esperado: atribuição efetuada com sucesso e mensagem ("The assign students to assistant(s) was done sucessfully.")
  * Resultado obtido:  atribuição efetuada com sucesso e mensagem ("The assign students to assistant(s) was done sucessfully.")

  * Ação: submeter o cadastro com varias atribuições, algumas incorretas
  * Resultado esperado: algumas atribuições efetuadas com sucesso,mas mensagem ("Review the assigns students to assistant(s) bellow. See usernames with attention.") e permanece no campo as atribuições que não foram registrados
  * Resultado obtido:  algumas atribuições com sucesso, mas mensagem ("Review the assigns students to assistant(s) bellow. See usernames with attention." e permanece no campo as atribuições que não foram registrados

#### Cenário 8 ####
  * Ator: professor (superusuário)
  * Página: página de visualização de  informações dos usuários

  * Ação: deletar algum usuário
  * Resultado esperado: redirecionamento para página com confirmação
  * Resultado obtido: redirecionamento para página com confirmação

#### Cenário 9 ####
  * Ator: professor (superusuário)
  * Página: página de cadastro de exercício

  * Ação: cadastrar um exercicio corretamente
  * Resultado esperado: mensagem "The exercise was added sucessfully. If you want edit the default test to this exercise click on link "Exercises > List Tests" and edit it."
  * Resultado obtido: mensagem "The exercise was added sucessfully. If you want edit the default test to this exercise click on link "Exercises > List Tests" and edit it."

  * Ação: cadastrar um exercicio faltando nome
  * Resultado esperado: mensagem de erro "Some error exists in your form."
  * Resultado obtido: mensagem de erro "Some error exists in your form."

  * Ação: cadastrar um exercicio faltando data
  * Resultado esperado: mensagem de erro "Review the date."
  * Resultado obtido: mensagem de erro "Review the date."

  * Ação: cadastrar um exercicio faltando descrição
  * Resultado esperado: mensagem "The exercise was added sucessfully. If you want edit the default test to this exercise click on link "Exercises > List Tests" and edit it."
  * Resultado obtido: mensagem "The exercise was added sucessfully. If you want edit the default test to this exercise click on link "Exercises > List Tests" and edit it."

  * Ação: cadastrar um exercicio indisponivel
  * Resultado esperado: mensagem "The exercise was added sucessfully. If you want edit the default test to this exercise click on link "Exercises > List Tests" and edit it."
  * Resultado obtido: mensagem "The exercise was added sucessfully. If you want edit the default test to this exercise click on link "Exercises > List Tests" and edit it."

  * Ação: cadastrar um exercicio com o nome de um exercicio que já existe
  * Resultado esperado: mensagem de erro 'An exercise with the same name already exists.'
  * Resultado obtido: mensagem de erro 'An exercise with the same name already exists.'

#### Cenário 10 ####
  * Ator: professor (superusuário)
  * Página: lista de exercícios

  * Ação: Clicar no nome de um exercício
  * Resultado esperado: redirecionamento para página com uma visão mais detalhada do exercício
  * Resultado obtido: redirecionamento para página com uma visão mais detalhada do exercício

  * Ação: Habilitar um exercicio que estava desabilitado clicando em uma checkbox na coluna "Unable/Enable Availability"
  * Resultado esperado: redirecionamento para página de confirmação
  * Resultado obtido: redirecionamento para página de confirmação

  * Ação: confirmar operação
  * Resultado esperado: mensagem "The exercise was updated sucessfully. Please, check the deadline to this exercise."
  * Resultado obtido: mensagem "The exercise was updated sucessfully. Please, check the deadline to this exercise."

  * Ação: clicar em "Back to list exercises"
  * Resultado esperado: redirecionamento para página que lista os exercícios e exercício modificado
  * Resultado obtido: redirecionamento para página que lista os exercícios e exercício modificado

  * Ação: Desabilitar um exercicio que estava habilitado clicando em uma checkbox na coluna "Unable/Enable Availability"
  * Resultado esperado: redirecionamento para página de confirmação
  * Resultado obtido: redirecionamento para página de confirmação

  * Ação: confirmar operação
  * Resultado esperado: mensagem "The exercise was updated sucessfully. Please, check the deadline to this exercise."
  * Resultado obtido: mensagem "The exercise was updated sucessfully. Please, check the deadline to this exercise."

  * Ação: clicar em "Back to list exercises"
  * Resultado esperado: redirecionamento para página que lista os exercícios e exercício modificado
  * Resultado obtido: redirecionamento para página que lista os exercícios e exercício modificado

  * Ação: Habilitar/desabilitar um exercicio que estava desabilitado/habilitado clicando em uma checkbox na coluna "Unable/Enable Availability"
  * Resultado esperado: redirecionamento para página de confirmação
  * Resultado obtido: redirecionamento para página de confirmação

  * Ação: clicar em "Back to list exercises"
  * Resultado esperado: redirecionamento para página que lista os exercícios e exercício não modificado
  * Resultado obtido: redirecionamento para página que lista os exercícios e exercício não modificado

  * Ação: clicar no botão "Delete" referente a um exercício na lista
  * Resultado esperado: redirecionamento para página de confirmação
  * Resultado obtido: redirecionamento para página de confirmação

  * Ação: confirmar operação
  * Resultado esperado: mensagem The exercise was deleted sucessfully.
  * Resultado obtido: mensagem The exercise was deleted sucessfully.

  * Ação: clicar em "Back to list exercises"
  * Resultado esperado: redirecionamento para página que lista os exercícios e exercício não mais presente na lista
  * Resultado obtido: redirecionamento para página que lista os exercícios e exercício não mais presente na lista

  * Ação: clicar no botão "Delete" referente a um exercício na lista
  * Resultado esperado: redirecionamento para página de confirmação
  * Resultado obtido: redirecionamento para página de confirmação

  * Ação: clicar em "Back to list exercises"
  * Resultado esperado: redirecionamento para página que lista os exercícios e exercício não deletado
  * Resultado obtido: redirecionamento para página que lista os exercícios e exercício não deletado

#### Cenário 11 ####
  * Ator: professor (superusuário)
  * Página: visão detalhada de um exercício

  * Ação: clicar no botão "Edit this exercise"
  * Resultado esperado: redirecionamento para a página de edição
  * Resultado obtido: redirecionamento para a página de edição

  * Ação: não alterar nada e clicar no botão "Change Exercise"
  * Resultado esperado: redirecionamento para a página com visão detalhada de um exercício sem nenhuma alteração
  * Resultado obtido: redirecionamento para a página com  visão detalhada de um exercício sem nenhuma alteração

  * Ação: editar o nome do exercício e clicar no botão "Change Exercise"
  * Resultado esperado: redirecionamento para a página com visão detalhada de um exercício com nome modificado
  * Resultado obtido: redirecionamento para a página com  visão detalhada de um exercício com nome modificado

  * Ação: editar a descrição do exercício e clicar no botão "Change Exercise"
  * Resultado esperado: redirecionamento para a página com visão detalhada de um exercício com descrição modificada
  * Resultado obtido: redirecionamento para a página com  visão detalhada de um exercício com descrição modificada

  * Ação: editar a disponibilidade do exercício e clicar no botão "Change Exercise"
  * Resultado esperado: redirecionamento para a página com visão detalhada de um exercício com disponibilidade modificada
  * Resultado obtido: redirecionamento para a página com  visão detalhada de um exercício com disponibilidade modificada

  * Ação: editar a data do exercício e clicar no botão "Change Exercise"
  * Resultado esperado: redirecionamento para a página com visão detalhada de um exercício com data modificada
  * Resultado obtido: redirecionamento para a página com  visão detalhada de um exercício com data modificada

  * Ação: alterar todos os dados e clicar no botão "Change Exercise"
  * Resultado esperado: redirecionamento para a página com visão detalhada de um exercício com todas as alterações
  * Resultado obtido: redirecionamento para a página com  visão detalhada de um exercício com todas as alterações

#### Cenário 12 ####
  * Ator: aluno
  * Página: login

  * Ação: realizar primeiro login (1º acesso ao Hoopaloo)
  * Resultado esperado: redirecionamento para a página de mudança de senha
  * Resultado obtido: redirecionamento para a página de mudança de senha

  * Ação: mudar a senha
  * Resultado esperado: redirecionamento para a página de login com a mensagem "Your password was changed."
  * Resultado obtido: redirecionamento para a página de login com a mensagem "Your password was changed."

  * Ação: fazer login
  * Resultado esperado: redirecionamento para a página inicial de aluno (lista as submissões já realizadas pelo aluno), nesse caso a lista está vazia
  * Resultado obtido: redirecionamento para a página inicial de aluno (lista as submissões já realizadas pelo aluno), nesse caso a lista está vazia

#### Cenário 13 ####
  * Ator: aluno
  * Página: página inciial de aluno

  * Ação: clicar em "Change Password" no menu principal
  * Resultado esperado: redirecionamento para página de mudança de senha
  * Resultado obtido:  redirecionamento para página de mudança de senha

  * Ação: alterar a senha
  * Resultado esperado: redirecionamento para página de login com a mensagem "Your password was changed."
  * Resultado obtido:  redirecionamento para página de login com a mensagem "Your password was changed."

  * Ação: fazer login com a nova senha
  * Resultado esperado: redirecionamento para a página inicial de aluno (lista as submissões já realizadas pelo aluno)
  * Resultado obtido: redirecionamento para a página inicial de aluno (lista as submissões já realizadas pelo aluno)

  * Ação: clicar em "Delivered Exercises" no menu Exercises
  * Resultado esperado: redirecionar para a página que mostra os exercícios já entregues pelo aluno
  * Resultado obtido:

  * Ação: clicar em "Undelivered Exercises" no menu Exercises
  * Resultado esperado: redirecionar para a página que mostra os exercícios não entregues pelo aluno
  * Resultado obtido: redirecionar para a página que mostra os exercícios não entregues pelo aluno

  * Ação: clicar em "Available Exercises" no menu Exercises
  * Resultado esperado: redirecionar para a página que mostra os exercícios disponíveis para entrega
  * Resultado obtido: redirecionar para a página que mostra os exercícios disponíveis para entrega

  * Ação: clicar em "Submit" no menu Submissions
  * Resultado esperado: redirecionar para a página de submissões, que possui o campo para fazer upload e uma lista das submissões já realizadas
  * Resultado obtido: redirecionar para a página de submissões, que possui o campo para fazer upload e uma lista das submissões já realizadas

  * Ação: clicar em "See Submisisons" no menu Submissions
  * Resultado esperado: redirecionar para a página que mostra a lista das submissões já realizadas
  * Resultado obtido: redirecionar para a página que mostra a lista das submissões já realizadas

  * Ação: clicar no link "Logout" no menu principal
  * Resultado esperado: redirecionamento para a página de login com a mensagem de logout ("You are unlogged")
  * Resultado obtido: redirecionamento para a página de login com a mensagem de logout ("You are unlogged")

#### Cenário 14 ####
  * Ator: aluno
  * Página: página de submissões

  * Ação: Fazer upload corretamente de um arquivo para um exercício
  * Resultado esperado: mensagem de sucesso "Your program was updated sucessfully. Check your code submission in table bellow.", mensagem de sucesso nos testes (nenhum teste registrado ainda para o exercício) "Your program passed in all tests (0 tests)." e apresentação do arquivo submetido na lista de submissões já realizadas
  * Resultado obtido: mensagem de sucesso "Your program was updated sucessfully. Check your code submission in table bellow.", mensagem de sucesso nos testes (nenhum teste registrado ainda para o exercício) "Your program passed in all tests (0 tests)." e apresentação do arquivo submetido na lista de submissões já realizadas

  * Ação: clicar em "See Submisisons" no menu Submissions
  * Resultado esperado: redirecionar para a página que mostra a lista das submissões já realizadas, incluindo a realizada agora
  * Resultado obtido: redirecionar para a página que mostra a lista das submissões já realizadas, incluindo a realizada agora

  * Ação: clicar no link "Logout" no menu principal
  * Resultado esperado: redirecionamento para a página de login com a mensagem de logout ("You are unlogged")
  * Resultado obtido: redirecionamento para a página de login com a mensagem de logout ("You are unlogged")

  * Ator: professor ou tutor
  * Página: login

  * Ação: fazer login
  * Resultado esperado: página inicial de professor ou tutor
  * Resultado obtido: página inicial de professor ou tutor

  * Ação: ver a tabela de informações sobre os alunos na página inicial
  * Resultado esperado: visualização do número 1 no número de submissões do aluno que estava logado anteriormente
  * Resultado obtido: visualização do número 1 no número de submissões do aluno que estava logado anteriormente

  * <font color='red'>Ação: clicar no nome no aluno<br>
<ul><li>Resultado esperado: ver uma lista das submissões dos alunos (assim como eles vêem)<br>
</li><li>Resultado obtido: <a href='https://code.google.com/p/hoopaloo/issues/detail?id='>https://code.google.com/p/hoopaloo/issues/detail?id=</a>: página de erro (Page not found) CORRIGIDO!!!</font></li></ul>

  * Ação: clicar no link "Exercises of <Nome do aluno>"
  * Resultado esperado: redirecionamento para uma página contendo uma tabela com resultado sumárizados sobre as submissões do aluno
  * Resultado obtido:  redirecionamento para uma página contendo uma tabela com resultado sumárizados sobre as submissões do aluno

  * Página: Exercises of <Nome do aluno> (página obtida no passo anterior)
  * Ação: clicar no nome do exercício
  * Resultado esperado: visualização dados sobre a questão e sobre a submissão do aluno (nome do aluno, enunciado da questão, número de testes, número de erros, mensagens de erro, código do aluno)
  * Resultado obtido: visualização dados sobre a questão e sobre a submissão do aluno (nome do aluno, enunciado da questão, número de testes, número de erros, mensagens de erro, código do aluno)

  * Ação: clicar no link "See Code of the Test" logo abaixo do código do aluno
  * Resultado esperado: abrir uma nova página com uma visão do teste para aquela questão, incluindo o código
  * Resultado obtido: abrir uma nova página com uma visão do teste para aquela questão, incluindo o código

  * Página: Exercises of <Nome do aluno> (voltar para a página anterior)
  * Ação: clicar no link "Code"
  * Resultado esperado: baixar o arquivo do aluno
  * Resultado obtido: baixar o arquivo do aluno <font color='green'> WARNING#1: Dar um jeito de nomear o arquivo porque ele salva com um nome dado pelo browser</font>

#### Cenário 15 ####
  * Ator: professor ou tutor
  * Página: página que lista todos os testes (List Test no menu Exercise)

  * Ação: clicar no nome de um teste
  * Resultado esperado: abrir uma nova página com uma visão do teste para aquela questão, incluindo o código
  * Resultado obtido: abrir uma nova página com uma visão do teste para aquela questão, incluindo o código

  * Página: lista de todos os testes (voltar para página anterior)
  * Ação: clicar no link "Edit it" para algum teste
  * Resultado esperado: redirecionamento para página de edição do teste
  * Resultado obtido: redirecionamento para página de edição do teste

  * Ação: não editar nada e voltar para a página anterior
  * Resultado esperado: nenhuma alteração na lista de teste (teste ainda unlocked)
  * Resultado obtido: nenhuma alteração na lista de teste (teste ainda unlocked)

  * Ação: clicar no link "Edit it" para algum teste
  * Resultado esperado: redirecionamento para página de edição do teste
  * Resultado obtido: redirecionamento para página de edição do teste

  * Ação: não editar nada, mas clicar no botão "Save Test As Under Test"
  * Resultado esperado: redirecionamento para uma página com todas as submissões para a questão relativa ao teste editado, mensagem "The test under test was added sucessfullty. Choose the student submissions to execute."
  * Resultado obtido: redirecionamento para uma página com todas as submissões para a questão relativa ao teste editado, mensagem "The test under test was added sucessfullty. Choose the student submissions to execute."

  * Ação: voltar 2 páginas
  * Resultado esperado: alteração na lista de teste (teste editado agora está locked - Locked by "fulano"), uma nova tabela "Under Tests", que possui o teste que acabou de ser supostamente editado
  * Resultado obtido: alteração na lista de teste (teste editado agora está locked - Locked by "fulano"), uma nova tabela "Under Tests", que possui o teste que acabou de ser supostamente editado

  * Ação: clicar em "Edit it" para um teste qualquer cujo exercício já possua submissões
  * Resultado esperado: redirecionamento para página de edição do teste
  * Resultado obtido: redirecionamento para página de edição do teste

  * Ação: realmente editar o código do teste (lembrar de fazer o import do módulo de solução) e clicar o botão "Save As Under Test"
  * Resultado esperado: redirecionamento para uma página com todas as submissões para a questão relativa ao teste editado, mensagem "The test under test was added sucessfullty. Choose the student submissions to execute."
  * Resultado obtido: redirecionamento para uma página com todas as submissões para a questão relativa ao teste editado, mensagem "The test under test was added sucessfullty. Choose the student submissions to execute."

  * Ação: escolher/marcar uma (ou mais) submissão (submissões) e clicar no botão "Run Test"
  * Resultado esperado: redirecionamento para página com os resultados da exercução do teste editado sobre a submissão (ou submissões) escolhida(s)
  * Resultado obtido: redirecionamento para página com os resultados da exercução do teste editado sobre a submissão (ou submissões) escolhida(s)

  * Página: página com resultados temporários (obtida no passo anterior)
  * Ação: clicar no botão "Back to Edit"
  * Resultado esperado: redirecionamento para a página de edição do teste
  * Resultado obtido: redirecionamento para a página de edição do teste

  * Ação: não alterar nada (apenas por simplicidade, para voltar à págian de resultados temporários) e clicar em "Save Test Under Test"
  * Resultado esperado: redirecionamento para uma página com todas as submissões para a questão relativa ao teste editado, mensagem "The test under test was added sucessfullty. Choose the student submissions to execute."
  * Resultado obtido: redirecionamento para uma página com todas as submissões para a questão relativa ao teste editado, mensagem "The test under test was added sucessfullty. Choose the student submissions to execute."

  * Ação: escolher/marcar uma (ou mais) submissão (submissões) e clicar no botão "Run Test"
  * Resultado esperado: redirecionamento para página com os resultados da exercução do teste editado sobre a submissão (ou submissões) escolhida(s)
  * Resultado obtido: redirecionamento para página com os resultados da exercução do teste editado sobre a submissão (ou submissões) escolhida(s)

  * Ação: clicar no botão "Cancel"
  * Resultado esperado: redirecionamento para a página de visão do teste
  * Resultado obtido:  redirecionamento para a página de visão do teste

  * <font color='red'>Ação: clicar em qualquer link do menu a partir dessa página<br>
<ul><li>Resultado esperado: redirecionamento para a página indicada pelo link<br>
</li><li>Resultado obtido: <a href='https://code.google.com/p/hoopaloo/issues/detail?id='>https://code.google.com/p/hoopaloo/issues/detail?id=</a>: Page not found (links quebrados) CORRIGIDO!!! </font></li></ul>

  * Ação: chegar até a página de resultados temporários novamente e clicar no botão "Consolidate Test"
  * Resultado esperado: redirecionamento para a página de visão de teste já com o código alterado
  * Resultado obtido:  redirecionamento para a página de visão de teste já com o código alterado

  * <font color='red'>Ação: clicar em qualquer link do menu a partir dessa página<br>
<ul><li>Resultado esperado: redirecionamento para a página indicada pelo link<br>
</li><li>Resultado obtido: <a href='https://code.google.com/p/hoopaloo/issues/detail?id='>https://code.google.com/p/hoopaloo/issues/detail?id=</a>: Page not found (links quebrados) CORRIGIDO!!!</font></li></ul>

#### Cenário 16 ####
  * Ator: professor ou tutor
  * Página: lista de exercicios

  * Ação: clicar no nome do exercício
  * Resultado esperado: redirecionamento para página com uma visão mais detalhada do exercício, dessa vez com uma tabela de resultados e dois links que vão dar uma visão do percentual de testes acertados eplos alunos e das notas obtidas
  * Resultado obtido: redirecionamento para página com uma visão mais detalhada do exercício, dessa vez com uma tabela de resultados e dois links que vão dar uma visão do percentual de testes acertados eplos alunos e das notas obtidas

  * Página: página inicial ou visão dos alunos
  * Ação: clicar no link "Exercises of <Nome do aluno>"
  * Resultado esperado: redirecionamento para uma página contendo uma tabela com resultado sumarizados sobre as submissões do aluno
  * Resultado obtido:  redirecionamento para uma página contendo uma tabela com resultado sumarizados sobre as submissões do aluno

  * Ação: clicar no nome de algum exercício
  * Resultado esperado: visualização dados sobre a questão e sobre a submissão do aluno (nome do aluno, enunciado da questão, número de testes, número de erros, mensagens de erro, código do aluno)
  * Resultado obtido: visualização dados sobre a questão e sobre a submissão do aluno (nome do aluno, enunciado da questão, número de testes, número de erros, mensagens de erro, código do aluno)

  * <font color='red'>Ação: inserir comentário e/ou nota para aquela submissão<br>
<ul><li>Resultado esperado: mensagem "Comments/score are addedd sucessfully."<br>
</li><li>Resultado obtido: <a href='https://code.google.com/p/hoopaloo/issues/detail?id='>https://code.google.com/p/hoopaloo/issues/detail?id=</a>: Server Error (500) CORRIGIDO!!!!!!!!!!! </font></li></ul>

  * Ação: clicar no link "Logout" no menu principal
  * Resultado esperado: redirecionamento para a página de login com a mensagem de logout ("You are unlogged")
  * Resultado obtido: redirecionamento para a página de login com a mensagem de logout ("You are unlogged")

  * Ator: aluno
  * Página: página de login

  * Ação: realizar login
  * Resultado esperado: redirecionamento para a página inicial de aluno (lista as submissões já realizadas pelo aluno)
  * Resultado obtido: redirecionamento para a página inicial de aluno (lista as submissões já realizadas pelo aluno)

  * Ação: clicar no link "Views Code"
  * Resultado esperado: opção de salvar o código
  * Resultado obtido: opção de salvar o código <font color='green'>WARNING#2: Colocar um nome no arquivo que vai se salvo </font>

  * Ação: clicar no nome da questão
  * Resultado esperado: redirecionamento para a página de vsão da submissão (enunciado da questão, número de testes, núemro de erros, mensagens de erro, comnetários e nota, além do código)
  * resiltado obtido: redirecionamento para a página de vsão da submissão (enunciado da questão, número de testes, núemro de erros, mensagens de erro, comnetários e nota, além do código)

#### Cenário 17 ####
  * Ator: professor ou tutor
  * Página: atribuição de alunos a tutores

  * <font color='red'>Ação: tentar fazer atribuição entre tutores e alunos inexistentes no sistema<br>
<ul><li>Resultado esperado: mensagem de erro informando que a operação não foi realizada com sucesso e apresentação das linhas incorretas.<br>
</li><li>Resultado obtido: <a href='https://code.google.com/p/hoopaloo/issues/detail?id='>https://code.google.com/p/hoopaloo/issues/detail?id=</a>: mensagem de erro informando que a operação não foi realizada com sucesso e apresentação das linhas incorretas, mas ocorreu a repetição das linhas incorretas. Por exemplo, se houvesse 3 nomes de alunos não existentes, haveria 3 repetições da linha incorreta. CORRIGIDO!!!</font></li></ul>

#### Cenário 18 ####
  * Ator: professor ou tutor
  * Página: edição de testes

  * <font color='red'>Ação: editar um teste, salvar como undertest e depois não escolher nenhuma submissão para executar e mesmo assim clicar em "Run Test"<br>
<ul><li>Resultado esperado: mensagem de erro avisando que ao menos uma submissão deve ser escolhida para que o testes seja executado<br>
</li><li>Resultado obtido: <a href='https://code.google.com/p/hoopaloo/issues/detail?id='>https://code.google.com/p/hoopaloo/issues/detail?id=</a>:  nenhuma mensagem. CORRIGIDO!!!</font></li></ul>


### Testes On-Line com Andrea (12-06) ###

Resoluções:

#### Problemas ####

Depois de consolidar um undertest ir para a pagina que lista os testes para evitar que a ação de voltar a pagina anterior dê problemas. Além disso, arrumar uma pagina que nao seja aquele erro 500 para as situações que em o cara voltar no browser e quiser clicar em um daqueles botoes (consolidate, cancel ou back to edit). Colocar um link na página de visualização dos testes para que o usuário possa voltar à pagina de listagem, isso evita quer ele use mto o back do browser.

<font color='red'>De alguma forma o undertest não está sendo destruido do bd e isso causa um problema na hora de executar a segunda edição. (Acho quer foi apenas na hora do teste.) CORRIGIDO </font>

<font color='red'>Quando o professor não colocar mensagem de erro alternativa, não apresentar o resultado da asserção para o usuário.</font>

<font color='red'>Visualizar exercicio para aluno que nao tem tutor dah erro!!! Ver isso no arquivo util.py CORRIGIDO </font>

#### Coisas a ajeitar (menos graves) ####

Under test colocar uma coluna de edição.
Substituir os templates que estão lá em casa pelo html do site (A partir de test view mexer no menu dá erro de página)
Reorganizar a página que o professor vê a submissão do aluno para que ele possa imprimir como Dalton quer.

Colocar um botão na página de edição do teste apenas para ele cancelar a ação de editar e voltar a pagina que lista.
Quando faz um comentario dah erro se clicar no menu, ajeitar os links.

### Relatos dos monitores ###
#### Francisco Thiago ####
  * "Quando estou logado como tutor, quando peço para ver os estudantes, vejo o seguinte erro: Server Error (500)" CORRIGIDO
  * "erro ocorre quando tento registrar uma questão, funcionou na segunda tentativa
;( Na realidade observei que quando uso determinados caracteres no "Título do exercício" aparece esse erro" CORRIGIDO