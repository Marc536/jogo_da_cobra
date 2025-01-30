import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

LIMIT_X = 250
LIMIT_Y = 250
RAIO_CABECA_COBRA = 5
DIR_X_CABECA_COBRA = 5
DIR_Y_CABECA_COBRA = 5
TAMANHO_DA_COBRA = 3

RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'

# última posição da cobra
LAST_POS = None

# inicio do movimento da cobra
START_MOVE = 0

# Criando um fundo branco
FIG, AX = plt.subplots(figsize=(10, 10))

# desenhando a cobra
COBRA = []

# Passo de movimento da cabeça da cobra
STEP = RAIO_CABECA_COBRA * 2

# Sentido de movimento da cabeça no eixo X
SENT_X = 0

# Sentido de movimento da cabeça no eixo Y
SENT_Y = 0

# desenhando fruta
FRUTA = None

def gerar_numeros():
	x = random.choice(range(5, 250, 10))
	y = random.choice(range(5, 250, 10))
	for i in COBRA:
		pos = i.center
		if pos[0] == x and pos[1] == y:
			x, y = gerar_numeros()
			return x, y
	return x, y

def update(frame = 0):
	"""Atualiza a posição da cabeça da cobra continuamente"""

	global FRUTA
	global DIR_X_CABECA_COBRA
	global DIR_Y_CABECA_COBRA
	global TAMANHO_DA_COBRA
	DIR_X = DIR_X_CABECA_COBRA + STEP * SENT_X
	DIR_Y = DIR_Y_CABECA_COBRA + STEP * SENT_Y

	# Verifica se a cobra se movimentou
	if not START_MOVE:
		return

	# Verifica se o movimento da cobra extrapolou os limites da tela
	if DIR_X < RAIO_CABECA_COBRA:
		return
	if DIR_X > LIMIT_X - RAIO_CABECA_COBRA:
		return
	if DIR_Y > LIMIT_Y - RAIO_CABECA_COBRA:
		return
	if DIR_Y < RAIO_CABECA_COBRA:
		return
	
	# Verifica se a cobra não bateu no seu corpo
	for i in range(len(COBRA)):
		if i < len(COBRA) -1:
			pos = COBRA[i].center
			if pos[0] == DIR_X_CABECA_COBRA and pos[1] == DIR_Y_CABECA_COBRA:
				return
	
	DIR_X_CABECA_COBRA = DIR_X
	DIR_Y_CABECA_COBRA = DIR_Y

	# Desenha repetidamente a cabeça da cobra no seu novo lugar
	COBRA.append(plt.Circle((DIR_X_CABECA_COBRA, DIR_Y_CABECA_COBRA), RAIO_CABECA_COBRA, color='red'))
	AX.add_patch(COBRA[-1])

	# limita o tamanho da cobra
	if len(COBRA) > TAMANHO_DA_COBRA:
		cauda = COBRA.pop(0)
		cauda.remove()
		del cauda

	# atualizando a cor do corpo da cobra no fundo branco
	for i in range(len(COBRA)):
		if i < len(COBRA) -1:
			COBRA[i].set_facecolor('blue')

	# fruta não existe
	if not FRUTA:
		# Desenhando um círculo (cabeça da cobra)
		DIR_X_FRUTA, DIR_Y_FRUTA = gerar_numeros()
		FRUTA = plt.Circle((DIR_X_FRUTA, DIR_Y_FRUTA), RAIO_CABECA_COBRA, color='yellow')

		# Adicionar a fruta ao fundo branco
		AX.add_patch(FRUTA)

	# fruta existe
	if FRUTA:
		pos_fruta = FRUTA.center
		if DIR_X_CABECA_COBRA == pos_fruta[0] and DIR_Y_CABECA_COBRA == pos_fruta[1]:
			FRUTA.remove()
			del FRUTA
			FRUTA = None
			TAMANHO_DA_COBRA += 1


def on_key(event):
	"""Movimenta a cabeça da cobra quando uma tecla é pressionada"""

	global SENT_X
	global SENT_Y
	global START_MOVE
	global LAST_POS

	if event.key == LEFT:
		if LAST_POS == RIGHT:
			return
		LAST_POS = LEFT
		SENT_X = 0
		SENT_Y = 0
		if DIR_X_CABECA_COBRA > RAIO_CABECA_COBRA:
			START_MOVE = 1
			SENT_X = -1
	elif event.key == RIGHT:
		if LAST_POS == LEFT:
			return
		LAST_POS = RIGHT
		SENT_X = 0
		SENT_Y = 0
		if DIR_X_CABECA_COBRA < LIMIT_X - RAIO_CABECA_COBRA:
			START_MOVE = 1
			SENT_X = 1
	elif event.key == UP:
		if LAST_POS == DOWN:
			return
		LAST_POS = UP
		SENT_X = 0
		SENT_Y = 0
		if DIR_Y_CABECA_COBRA < LIMIT_Y - RAIO_CABECA_COBRA:
			START_MOVE = 1
			SENT_Y = 1
	elif event.key == DOWN:
		if LAST_POS == UP:
			return
		LAST_POS = DOWN
		SENT_X = 0
		SENT_Y = 0
		if DIR_Y_CABECA_COBRA > RAIO_CABECA_COBRA:
			START_MOVE = 1
			SENT_Y = -1

	FIG.canvas.draw()

def main():
	# Desenhando um círculo (cabeça da cobra)
	circle = plt.Circle((DIR_X_CABECA_COBRA, DIR_Y_CABECA_COBRA), RAIO_CABECA_COBRA, color='red')

	# Adicionando a cabeça ao corpo da cobra
	COBRA.append(circle)

	# Adicionar a cabeça da cobra ao fundo branco
	AX.add_patch(circle)

	# Configurando limites
	AX.set_xlim(0, LIMIT_X)
	AX.set_ylim(0, LIMIT_Y)
	
	# Conectando o evento de teclado
	FIG.canvas.mpl_connect("key_press_event", on_key)

	# Criando a animação para atualizar a posição do círculo
	ani = animation.FuncAnimation(FIG, update, frames=500, interval=120, blit=False)

	plt.show()

if __name__ == "__main__":
	main()