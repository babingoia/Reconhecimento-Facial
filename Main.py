# Bibliotecas
import cv2
import face_recognition as fc
import os
import Classes

# Contadores
conhecidos = 0
desconhecidos = 0

# Listas
Pessoas = []

# Pega todas as pessoas que estiverem na pasta de Conhecidas e armzena na lista Pessoas
def atualizar_lista_conhecidos():
    global Pessoas
    i = 0
    for file in os.listdir('Conhecidas/'):
        Pessoas.append(Classes.Conhecida('', '', '', '', ))
        Pessoas[i].nome = f'{file}'
        Pessoas[i].imagem = fc.load_image_file(f'Conhecidas/{file}')
        i += 1


# Bloco que transforma todas as imagens de pessoas conhecidas em um codigo que o 'face recognition' lê
def encodar_conhecidos():
    global Pessoas
    i = 0
    atualizar_lista_conhecidos()

    try:
        print('Encodando imagens...')

        for pessoa in Pessoas:
            Pessoas[i].imagem_encodada = fc.face_encodings(pessoa.imagem)
            i += 1
        print("Imagens encodadas.")
    except:
        print('Imagem não encodada')
        quit()


# Funcao de capturar o video
def cap_video(video):
    # Pega a camera
    print('Carregando Video...')
    cap = cv2.VideoCapture(video, cv2.CAP_DSHOW)
    print('Video Carregado')

    while True:
        # Pega o frame da camera
        check, frame = cap.read()

        # Detecta um rosto pela funcao 'reconhecerImagem()' e desenha um retangulo envolta dele
        frame = reconhecer_imagem(frame)
        contar_tempo()

        # Mostra a imagem da camera com o retangulo
        cv2.imshow('Teste', frame)

        # Desliga tudo se apertar q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fecha tudo
    cap.release()
    cv2.destroyAllWindows()


# funcao que reconhece as faces e desenha um retangulo envolta, além de ativar os contadores.
def reconhecer_imagem(frame):
    image = []
    # Diminui o tamanho do frame para agilizar o processamento
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


# Função que vai diminuindo os contadores das pessoas detectadas. Ela é calculada em frames/segundo
def contar_tempo():
    for conhecido in Pessoas:
        conhecido.contador -= 1


# Função que conta quantas pessoas conhecidas e desconhecidas passaram nas cameras
def contar_pessoas(frame):
    # Puxa as variaveis de fora da função
    global Pessoas, conhecidos
    i = 0
    frame_encodado = []

    # Codigo que encoda o frame do video
    try:
        frame_encodado = fc.face_encodings(frame)
        print('Frame encodado')
    except:
        print('Frame não encodado')

    # Compara a pessoa do frame com o banco de imagem
    for pessoa in frame_encodado:
        # Compara cada pessoa do banco com as do frame
        for conhecido in Pessoas:

            resultado = fc.compare_faces(conhecido.imagem_encodada, pessoa)

            # Vê se alguma pessoa do banco bateu com a imagem da camera e adiciona um timer no contador de conhecidos.
            for b in range(0, len(resultado)):
                if resultado[b]:
                    if conhecido.contador <= 0:
                        conhecidos += 1
                        Pessoas[i].contador = 9000  # Equivale a 5 minutos
                        print('Achei mais uma pessoa conhecida!')
                    else:
                        Pessoas[i].contador = 9000
                else:
                    contar_pessoas_desconhecidas(frame)


def contar_pessoas_desconhecidas(frame):
    global desconhecidos
    # guardar_desconhecido(frame)
    print('Achei uma pessoa desconhecida!')
    desconhecidos += 1


# Função para armazenar uma pessoa desconhecida no banco de dados.
def guardar_desconhecido(frame):
    global desconhecidos
    # cv2.imwrite(f'{desconhecidos}.jpg', frame)


# Roda tudo
encodar_conhecidos()
cap_video(0)
print(f'Eu reconheci {conhecidos + desconhecidos} pessoas!, {conhecidos} eram conhecidas e {desconhecidos} eram '
      f'desconhecidas.')

# OBS: O programa ainda está super lento por conta da quantidade de codigo sendo executado entre os frames.

# OBS 2: O contador de desconhecidos ainda não funciona.

# OBS 3: Se a função de atualizar pessoas precisar ser executada de novo ela vai recolocar/excluir as pessoas que já
# existem.
