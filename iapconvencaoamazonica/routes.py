from flask import render_template, redirect, url_for, request, flash, abort
from iapconvencaoamazonica import app, database, bcrypt
from iapconvencaoamazonica.forms import FormLogin, FormCriarConta, FormPerfil, FormCriarPost
from iapconvencaoamazonica.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route("/contato")
def contato():
    return render_template('contato.html')


@app.route('/convencao')
def convencao():
    return render_template('convencao.html')


@app.route('/denominacao')
def denominacao():
    return render_template('denominacao.html')


@app.route('/missao-e-visao')
def missao_e_visao():
    return render_template('missaoevisao.html')


@app.route('/pontos-de-fe')
def pontos_de_fe():
    return render_template('pontos_de_fe.html')


@app.route('/diretoria-regional')
def diretoria_regional():
    return render_template('diretoria_regional.html')


@app.route('/ministerio-de-ensino')
def ministerio_de_ensino():
    return render_template('ministerio_de_ensino.html')


@app.route('/ministerio-de-mulheres')
def ministerio_de_mulheres():
    return render_template('ministerio_de_mulheres.html')


@app.route('/ministerio-de-jovens')
def ministerio_de_jovens():
    return render_template('ministerio_de_jovens.html')


@app.route('/ministerio-de-adolescentes')
def ministerio_de_adolescentes():
    return render_template('ministerio_de_adolescentes.html')


@app.route('/ministerio-de-celebracao')
def ministerio_de_celebracao():
    return render_template('ministerio_de_celebracao.html')


@app.route('/missoes-e-evengelismo')
def ministerio_de_me():
    return render_template('ministerio_de_me.html')


@app.route('/assistencia-social')
def ministerio_de_assistencia():
    return render_template('ministerio_de_assistencia.html')


@app.route('/vidapastoral')
def ministerio_de_vida_pastoral():
    return render_template('ministerio_de_vida_pastoral.html')


@app.route('/capelania')
def secretaria_capelania():
    return render_template('secretaria_capelania.html')


@app.route('/inclusao')
def secretaria_inclusao():
    return render_template('secretaria_inclusao.html')


@app.route('/regionais')
def noticias_regionais():
    return render_template('noticias_regionais.html')


@app.route('/nacionais')
def noticias_nacionais():
    return render_template('noticias_nacionais.html')


@app.route('/missionais')
def noticias_missionais():
    return render_template('noticias_missionais.html')


@app.route('/licoes/download')
def licoes():
    return render_template('licoes.html')


@app.route('/pequenos-grupos/download')
def pequenos_grupos():
    return render_template('pequenos_grupos.html')


@app.route('/ebooks/download')
def ebooks():
    return render_template('ebooks.html')


@app.route('/igrejas')
def igrejas():
    return render_template('igrejas.html')


@app.route('/converse-com-a-gente')
def converse_com_a_gente():
    return render_template('converse_com_a_gente.html')


@app.route('/acesso-restrito', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash('Login feito com sucesso!', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect('/')
        else:
            flash('Falha no Login, e-mail ou senha incorretos.', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash('Conta criada com sucesso!', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Faça o Login para continuar', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    profile_pictures = url_for('static', filename='profile_pictures/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', profile_pictures=profile_pictures)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post feito com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/profile_pictures', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    profile_pictures = url_for('static', filename='profile_pictures/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', profile_pictures=profile_pictures, form=form)


def transforma_titulo_para_url(titulo):
    # Substitui espaços por hifens e converte para minúsculas
    return titulo.replace(' ', '-').lower()


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
