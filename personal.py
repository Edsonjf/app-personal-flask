from flask import Flask, render_template, request, redirect, session, flash, url_for
import pandas as pd

class Aluno:
    def __init__(self, nome, nascimento, altura, peso):
        self.nome = nome
        self.nascimento = nascimento
        self.altura = altura
        self.peso = peso

aluno1 = Aluno('João', '01/01/2000', '1.8', '80')
aluno2 = Aluno('José', '02/02/2002', '1.75', '90')
aluno3 = Aluno('Marcos', '03/03/2003', '1.70', '70')
aluno4 = Aluno('Carlos', '04/04/2004', '1.65', '50')

alunos = {
    aluno1.nome: aluno1,
    aluno2.nome: aluno2,
    aluno3.nome: aluno3,
    aluno4.nome: aluno4,
}

lista = [aluno1, aluno2, aluno3, aluno4]

class Exercicio:
    def __init__(self, exercicio, series, repeticoes, carga):
        self.exercicio = exercicio
        self.series = series
        self.repeticoes = repeticoes
        self.carga = carga

exercicio1 = Exercicio('Agachamento', 5, 12, 70)
exercicio2 = Exercicio('Supino', 3, 10, 50)
exercicio3 = Exercicio('Pulley Frente', 4, 15, 60)

exercicios = [exercicio1, exercicio2, exercicio3]

Treinos = {
    'João':{
            'A':
                {'1': {'Desenvolvimento', '3', '12', '30'},
                 '2':'Supino Reto',
                 '3':'Supino Inclinado',
                 '4':'Supino Declinado',
                 '5':'Pulley Frente ',
                 '6':'Remada Curvada'
                },
            'B': {'1':'Agachamento',
                  '2':'Terra',
                  '3':'Stiff',
                  '4':'Abdução de quadril',
                  '5':'Adução de quadril',
                  '6':'Afundo'
                  }
        }
}

# Treinos = {
#     'João':
#         {
#             'A':
#                  [ exercicio1],
#
#             'B': {'1':'Agachamento',
#                   '2':'Terra',
#                   '3':'Stiff',
#                   '4':'Abdução de quadril',
#                   '5':'Adução de quadril',
#                   '6':'Afundo'
#                   },
#         },
#     'José':
#         {
#             'A':
#                 {'1': {'Desenvolvimento', '3', '12', '30'},
#                  '2':'Supino Reto',
#                  '3':'Supino Inclinado',
#                  '4':'Supino Declinado',
#                  '5':'Pulley Frente ',
#                  '6':'Remada Curvada'
#                 },
#             'B': {'1':'Agachamento',
#                   '2':'Terra',
#                   '3':'Stiff',
#                   '4':'Abdução de quadril',
#                   '5':'Adução de quadril',
#                   '6':'Afundo'
#                   }
#         }
# }

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('João', '@joao', '123')
usuario2 = Usuario('José', '@jose', '456')

usuarios = {usuario1.nome: usuario1,
            usuario2.nome: usuario2}

class Treino:
    def __init__(self, aluno, treino,
                 ex1, serie1, rep1, carga1,
                 ex2, serie2, rep2, carga2,
                 ):
        self.aluno = aluno
        self.treino = treino
        self.ex1 = ex1
        self.serie1 = serie1
        self.rep1 = rep1
        self.carga1 = carga1
        self.ex2 = ex2
        self.serie2 = serie2
        self.rep2 = rep2
        self.carga2 = carga2


treino_a = Treino('João', 'A',
                  'Supino Reto', '3', '10', '20',
                  'Desenvolvimento', '3', '12', '10'
                  )
treino_b = Treino('João', 'B',
                  'Agachamento',  '3', '10', '20',
                  'Terra', '3', '12', '10'
                  )

treinos = [treino_a]

app = Flask(__name__)

app.secret_key = 'treinopersonal'

@app.route('/')
def index():
    # se não houver nenhuma chave logada na sessão ou a chave definida como "None"
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Necessário login para continuar!')
        return redirect('/login')

    if session['usuario_logado'] in usuarios:
       usuario = usuarios[session['usuario_logado']]
       dados = alunos[session['usuario_logado']]

    #dados pessoais


    return render_template('lista.html', titulo='Aluno', alunos=lista, usuario=usuario, dados=dados)

@app.route('/registro-treino')
def sessao():
    return render_template('sessao_treino_executada.html', titulo='Sessão')

@app.route('/meus-treinos')
def meus_treinos():
    usuario = session['usuario_logado']
    flash(usuario)
    if usuario in Treinos.values():
        flash('Usuário tem treinos disponíveis')


    treino = exercicios
    return render_template('/meus_treinos.html', treino=treino)


@app.route('/dados-treino', methods=['POST',])
def treino():
    # nome = request.form['nome']
    exercicio = request.form['exercicio']
    series = request.form['series']
    repeticoes = request.form['repeticoes']
    carga = request.form['carga']

    treino = Exercicio(exercicio, series, repeticoes, carga)
    exercicios.append(treino)

    #return render_template('sessao_treino_realizado.html', titulo='Treino Realizado', treino=exercicios)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    #proxima = request.args.get('proxima')
    #return render_template('login.html', proxima=proxima)
    return render_template('login.html', titulo='Login')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nome
            flash(session['usuario_logado'] + ' logado com sucesso!')
            return redirect('/')
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)