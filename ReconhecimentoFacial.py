# Bibliotecas
import cv2
import face_recognition as fc
import os

# Lista de pessoas conhecidas com uma pasta de mesmo nome
Pessoas = []

# Pega todas as pessoas que estiverem na pasta de Conhecidas
for file in os.listdir('Conhecidas/'):
    Pessoas.append(fc.load_image_file(f'Conhecidas/{file}'))

# Contador de quantas vezes uma pessoa conhecida apareceu na camera
conhecidos = 0

# Bloco que transforma todas as imagens de pessoas conhecidas em um codigo que o face recognition lê
try:
    print('Encodando imagens...')
    PessoasCodificadas = []

    for imagem in Pessoas:
        PessoasCodificadas.append(fc.face_encodings(imagem)[0])
    print("Imagens encodadas.")

except:
    print('Imagem não encodada')
    quit()


# Funcao de capturar o video
def cap_video(video):
    # Pega a camera
    print('Carregando Video...')
    cap = cv2.VideoCapture(video)
    print('Video Carregado')

    while True:
        # Pega o frame da camera
        check, frame = cap.read()

        # Detecta um rosto pela funcao 'reconhecerImagem()' e desenha um retangulo envolta dele
        frame = reconhecer_imagem(frame)

        # Mostra a imagem da camera com o retangulo
        cv2.imshow('Teste', frame)

        # Desliga tudo se apertar q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fecha tudo
    cap.release()
    cv2.destroyAllWindows()


# funcao que reconhece as faces e desenha um retangulo envolta
def reconhecer_imagem(frame):
    # Diminui o tamanho do frame pra agilizar o processamento
    # framezinho = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Transforma o codigo de cores do frame pra RGB>
    imagem_rgb = frame[:, :, ::-1]

    # Detecta a posição dos rostos
    coordernadas = fc.face_locations(imagem_rgb)

    # Checa se existe algum valor de posição nas coordenadas
    if len(coordernadas) >= 1:

        # Aplica a função de contar pessoas
        contar_pessoas(frame)

        # Passa por todas as pessoas que aparecerem
        for (x, r, y, l) in coordernadas:
            # Pega as coordenadas do canto superior esquerdo, e volta elas ao tamanho normal
            top = l, x

            # Pega as coordenadas do canto inferior direito, e volta elas ao tamanho normal
            bottom = r, y

            # Desenha o retangulo
            image = cv2.rectangle(frame, top, bottom, (255, 0, 0), 5)

        # Retorna a imagem com o retangulo
        return image

    else:

        # Retorna o frame normal
        return frame


# Função que conta quantas pessoas conhecidas e desconhecidas passaram nas cameras
def contar_pessoas(frame):
    # Puxa as variaveis de fora da função
    global PessoasCodificadas
    global conhecidos

    # Codigo que encoda o frame do video
    try:
        frame = fc.face_encodings(frame)
        print('Frame encodado')
    except:
        print('Frame não encodado')

    # Compara a pessoa do frame com o banco de imagem
    for pessoa in frame:
        resultado = fc.compare_faces(PessoasCodificadas, pessoa)

        # Vê se alguma pessoa do banco bateu com a imagem da camera e adiciona 1 no contador de conhecidos.
        for i in range(0, len(resultado)):
            if resultado[i]:
                conhecidos += 1
                print('Achei mais uma pessoa conhecida!')


# Roda tudo
cap_video(0)
print(f'Eu reconheci {conhecidos} pessoas!q')

# OBS: O unico problema que eu achei é uma queda brutal de fps que tende a aumentar, eu achei um jeito de aumentar
# isso, mas a precisão cai muito. Essa solução está comentada no inicio da funcao reconhecerImagem()

# OBS 2: Ele conta a mesma pessoa diversas vezes em alguns segundos, vou colocar um delay individual de cada pessoa
# de pelo menos 1 minuto.

# OBS 3: A parte de contar desconhecidos vai ver se a pessoa existe no banco de dados e se não existir vai tirar uma
# print dela e adicionar um ponto no contador de desconhecidos.Depois vai colocar um delay individual igual o outro.
