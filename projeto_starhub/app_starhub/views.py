from django.shortcuts import render
from .models import Usuario
from django.shortcuts import render, redirect
from .models import Curriculo, Empresa, Vaga
from django.shortcuts import get_object_or_404

# Verificar o usuario logado ou nao
def get_usuario_logado(request):
    usuario_id = request.session.get('usuario_id')
    tipo = request.session.get('tipo_usuario')  # <-- pega o tipo salvo na sessão

    if not usuario_id or not tipo:
        return None

    if tipo == 'usuario':
        try:
            return Usuario.objects.get(id_usuario=usuario_id)
        except Usuario.DoesNotExist:
            return None
    elif tipo == 'empresa':
        from .models import Empresa
        try:
            return Empresa.objects.get(id_empresa=usuario_id)
        except Empresa.DoesNotExist:
            return None

    
    
# LOGICA DE LOGIN
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Tenta login como Usuario normal
        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            request.session['usuario_id'] = usuario.id_usuario
            request.session['tipo_usuario'] = 'usuario'  # opcional, para diferenciar depois
            return redirect('inicio')
        except Usuario.DoesNotExist:
            # Tenta login como Empresa
            try:
                empresa = Empresa.objects.get(email_empresa=email, senha_empresa=senha)
                request.session['usuario_id'] = empresa.id_empresa
                request.session['tipo_usuario'] = 'empresa'
                return redirect('inicio_empresa')
            except Empresa.DoesNotExist:
                # Nenhum usuário ou empresa com essas credenciais
                return render(request, 'usuarios/login.html', {'erro': 'Email ou senha inválidos.'})

    return render(request, 'usuarios/login.html')

# Cadastro
def cadastro(request):
    return render(request, 'usuarios/cadastro.html', {'erro': None})

def cadastro_empresa(request):
    if request.method == 'POST':
        nome_empresa = request.POST.get('nome_empresa')
        email_empresa = request.POST.get('email_empresa')
        local = request.POST.get('local')
        cpf = request.POST.get('cpf')
        pais = request.POST.get('pais')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        endereco = request.POST.get('endereco')
        senha_empresa = request.POST.get('senha_empresa')

        # Verificar se o email já existe
        if Empresa.objects.filter(email_empresa=email_empresa).exists():
            return render(request, 'jobs/cadastro_empresa.html', {'erro': 'Este e-mail já está em uso.'})

        # Criar nova empresa
        nova_empresa = Empresa(
            nome_empresa=nome_empresa,
            email_empresa=email_empresa,
            local=local,
            cpf=cpf,
            pais=pais,
            estado=estado,
            cidade=cidade,
            endereco=endereco,
            senha_empresa=senha_empresa
        )
        nova_empresa.save()

        # Redirecionar ou exibir sucesso
        return redirect('inicio_empresa')  # ou 'inicio_empresa', dependendo do fluxo

    # Se for GET, apenas renderiza o formulário
    return render(request, 'jobs/cadastro_empresa.html', {'erro': None})

# Dentro do site (USUÁRIO)

# Dentro do site (EMPRESA)
def inicio_empresa(request):
    usuario = get_usuario_logado(request)
    tipo = request.session.get('tipo_usuario')

    if not usuario:
        return redirect('login')

    if tipo != 'empresa':
        return redirect('inicio')

    return render(request, 'jobs/inicio_empresa.html', {'usuario': usuario})

def postar_vagas(request):
    if request.method == 'POST':
        empresa = get_usuario_logado(request)  # Pega a empresa logada

        if not empresa:
            return redirect('login')

        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        bolsa = request.POST.get('bolsa')
        local = request.POST.get('local')
        descricao = request.POST.get('descricao')

        Vaga.objects.create(
            empresa=empresa,
            titulo=titulo,
            horario=horario,
            bolsa=bolsa,
            local=local,
            descricao=descricao
        )

        return redirect('inicio_empresa')  # ou para onde quiser depois de postar

    return render(request, 'jobs/postar_vagas.html')

def detalhes_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    return render(request, 'main/detalhes_vaga.html', {'vaga': vaga})

def index(request):
    return render(request, 'usuarios/index.html')

def vagas(request):
    vagas = Vaga.objects.all()
    return render(request, 'main/vagas.html', {'vagas': vagas})

def interesse(request):
    return render(request, 'main/interesse.html')

def curriculo(request):
    usuario = get_usuario_logado(request)
    if not usuario:
        return redirect('login')

    sucesso = False

    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        Curriculo.objects.create(usuario=usuario, arquivo=arquivo)
        sucesso = True

    return render(request, 'curriculo.html', {'usuario': usuario, 'sucesso': sucesso})

def inicio(request):
    usuario = get_usuario_logado(request)
    if not usuario:
        return redirect('login')

    return render(request, 'main/inicio.html', {'usuario': usuario})

def perfil(request):
    usuario = get_usuario_logado(request)
    if not usuario:
        return redirect('login')
    return render(request, 'usuarios/perfil.html', {'usuario': usuario})

def usuarios(request):
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    # Verificar se o e-mail já está cadastrado
    if Usuario.objects.filter(email=email).exists():
        return render(request, 'usuarios/cadastro.html', {'erro': 'Este e-mail já está em uso.'})

    novo_usuario = Usuario()
    novo_usuario.nome = nome
    novo_usuario.sobrenome = sobrenome
    novo_usuario.email = email
    novo_usuario.senha = senha
    novo_usuario.save()

    usuarios = {
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'main/inicio.html', usuarios)

def upload_curriculo(request):
    usuario = get_usuario_logado(request)
    sucesso = False
    ultimo_curriculo = None

    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo')
        if arquivo:
            ultimo_curriculo = Curriculo.objects.create(usuario=usuario, arquivo=arquivo)
            sucesso = True
    else:
        # Se não for POST, busca o último currículo enviado (se existir)
        ultimo_curriculo = Curriculo.objects.filter(usuario=usuario).order_by('-data_envio').first()

    return render(request, 'usuarios/curriculo.html', {
        'curriculo': ultimo_curriculo,
        'sucesso': sucesso,
    })


def perfil(request):
    usuario = get_usuario_logado(request)
    if not usuario:
        return redirect('login')

    if request.method == 'POST':
        contato = request.POST.get('contato')
        cargo = request.POST.get('cargo')
        descricao = request.POST.get('descricao')
        imagem = request.FILES.get('imagem')

        usuario.contato = contato
        usuario.descricao = descricao
        usuario.cargo = cargo

        if imagem:
            usuario.imagem = imagem  

        print(f"ANTES DO SAVE: telefone={usuario.contato}, sobre={usuario.descricao}")
        usuario.save()
        print(f"DEPOIS DO SAVE: telefone={usuario.contato}, sobre={usuario.descricao}")
        return redirect('perfil')

    return render(request, 'usuarios/perfil.html', {'usuario': usuario})



