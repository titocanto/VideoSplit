import os
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def home(request):
    return render(request, 'home.html')


def split(request):
    if request.method == 'POST':
        # Obtém o arquivo e o tamanho da parte enviados pelo formulário
        uploaded_file = request.FILES['file']
        chunk_size = int(request.POST['chunk_size'])
        # Salva o arquivo enviado em uma pasta temporária
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        # Divide o arquivo em partes do tamanho especificado
        # Cria uma pasta para armazenar as partes do arquivo
        output_dir = os.path.splitext(file_path)[0] + "_split"
        os.makedirs(output_dir, exist_ok=True)
        # Abre o arquivo original em modo binário de leitura
        with open(file_path, "rb") as f:
            # Obtém o tamanho do arquivo em bytes
            file_size = os.path.getsize(file_path)
            # Converte o tamanho da parte para bytes
            chunk_size = chunk_size * 1024 * 1024
            # Calcula o número de partes necessárias
            num_chunks = file_size // chunk_size + 1
            # Itera sobre as partes do arquivo
            parts = []
            for i in range(num_chunks):
                # Cria um novo arquivo para a parte atual
                part_path = os.path.join(output_dir, f"Video_{i}.mp4")
                with open(part_path, "wb") as part:
                    # Lê o número de bytes necessários para a parte atual
                    data = f.read(chunk_size)
                    # Escreve os bytes lidos no novo arquivo
                    part.write(data)
                # Adiciona a parte atual à lista de partes
                parts.append(part_path)
            # Retorna uma página HTML que inclui links para cada parte do vídeo
            return render(request, 'download.html', {'parts': parts})
    else:
        return HttpResponse('Error: POST method required')


def download(request, filename):
    # Monta o caminho completo para o arquivo solicitado
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    # Retorna o arquivo para o usuário
    response = HttpResponse(open(path, 'rb'), content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(path)}'
    return response