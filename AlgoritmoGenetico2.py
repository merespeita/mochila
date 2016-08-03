from Cromossomo import Cromossomo
import random
from operator import attrgetter

class AlgoritmoGenetico:

		
	def __init__(self,nrGenes,tamanhoPopulacao):
		self.nrGenes = nrGenes
		self.tamanhoPopulacao = tamanhoPopulacao
		self.populacao = self.criaPopulacaoInicial(self.nrGenes)
		self.pesos=		[8, 41, 41, 37, 62, 41]
		self.valores=	[222, 23, 127, 72, 922, 204]
		self.pesoMaximo=1500
		self.probabilidadeCruzamento=90
		self.probabilidadeMutacao=10

	def cruzamentoUmPonto(self,cromo1,cromo2):
		numGenes = len(cromo1.genes)
		pontoCorte = random.randrange(numGenes)
		genes1 = cromo1.genes[0:pontoCorte] + cromo2.genes[pontoCorte:numGenes]
		genes2 = cromo2.genes[0:pontoCorte] + cromo1.genes[pontoCorte:numGenes]
		filho1 = Cromossomo(self.nrGenes)
		filho2 = Cromossomo(self.nrGenes)
		filho1.genes = genes1
		filho2.genes = genes2
		return filho1,filho2

	def cruzamentoDoisPontos(self,cromo1,cromo2):
		numGenes = len(cromo1.genes)
		pontoCorte1 = random.randrange(numGenes)
		pontoCorte2 = random.randrange(pontoCorte1, numGenes)
		# print str(pontoCorte1) + " " + str(pontoCorte2)
		genes1 = cromo1.genes[0:pontoCorte1] + cromo2.genes[pontoCorte1:pontoCorte2] + cromo1.genes[pontoCorte2:numGenes]
		genes2 = cromo2.genes[0:pontoCorte1] + cromo1.genes[pontoCorte1:pontoCorte2] + cromo2.genes[pontoCorte2:numGenes]
		genes3 = cromo1.genes[0:pontoCorte1] + cromo2.genes[pontoCorte1:numGenes] 
		genes4 = cromo2.genes[0:pontoCorte1] + cromo1.genes[pontoCorte1:numGenes] 
		genes5 = cromo1.genes[0:pontoCorte2] + cromo2.genes[pontoCorte2:numGenes] 
		genes6 = cromo2.genes[0:pontoCorte2] + cromo1.genes[pontoCorte2:numGenes]

		listaGenes = [genes1, genes2, genes3, genes4, genes5, genes6]
		cromossomosFilhos = [Cromossomo(genes) for genes in listaGenes]
		return cromossomosFilhos

		# filho1 = Cromossomo(self.nrGenes)
		# filho2 = Cromossomo(self.nrGenes)
		# filho3 = Cromossomo(self.nrGenes)
		# filho4 = Cromossomo(self.nrGenes)
		# filho5 = Cromossomo(self.nrGenes)
		# filho6 = Cromossomo(self.nrGenes)
		# filho1.genes = genes1
		# filho2.genes = genes2
		# filho3.genes = genes3
		# filho4.genes = genes4
		# filho5.genes = genes5
		# filho6.genes = genes6

	def mutacao(self,cromossomo):
		for i in range(0,len(cromossomo.genes)):
			prob = random.randrange(100)
			if(prob < self.probabilidadeMutacao):
				if cromossomo.genes[i]==1:
					cromossomo.genes[i]=0
				else:
					cromossomo.genes[i]=1


	def calculaFitness(self):
		for cromossomo in self.populacao:
			pesoTotal=0
			valorTotal=0
			if(cromossomo.getFitness == 0):
				continue
			for i in range(0,len(cromossomo.genes)):
				if(cromossomo.genes[i]==1):
					pesoTotal += self.pesos[i]
					valorTotal += self.valores[i]
			if(pesoTotal > self.pesoMaximo):
				cromossomo.setFitness(0)
			else:
				cromossomo.setFitness(1.0*valorTotal-0.0*pesoTotal)


	def criaPopulacaoInicial(self,nrGenes):
		populacao = []
		for i in range(0,self.tamanhoPopulacao*1):
			cromo = Cromossomo(nrGenes)
			populacao.append(cromo)
		return populacao


	def cruza(self):
		cromossomos=[]
		for cromossomo in self.populacao:
			prob = random.randrange(100)
			if(prob <= self.probabilidadeCruzamento): #verifica se o cromossomo ira para o cruzamento
				cromossomos.append(cromossomo)
		for x in range(0,len(cromossomos),1):
			if (x+1 >= len(cromossomos)):
				break
			cromossomosFilhos = self.cruzamentoDoisPontos(cromossomos[x],cromossomos[x+1])
			for cromossomo in cromossomosFilhos:
				self.populacao.append(cromossomo)

	def seleciona(self):
		self.calculaFitness()
		novaPopulacao=[]
		best = self.getMelhorIndividuo()					# 
		novaPopulacao.append(best)		
		while (len(novaPopulacao)<self.tamanhoPopulacao):					# elitismo
		# for i in range(self.tamanhoPopulacao):
			c1 = random.randrange(len(self.populacao))
			c2 = random.randrange(len(self.populacao))
			if(self.populacao[c1].getFitness() == 0 and self.populacao[c2].getFitness()==0):
				continue
			cromossomoVencedor = self.torneio(self.populacao[c1],self.populacao[c2])
			if cromossomoVencedor not in novaPopulacao:
				novaPopulacao.append(cromossomoVencedor)
		self.populacao = novaPopulacao


	def torneio(self,cromossomo1,cromossomo2):
		if(cromossomo1.getFitness > cromossomo2.getFitness):
			return cromossomo1
		else:
			return cromossomo2

	def roleta(self):
		

	def muta(self):
		best = self.getMelhorIndividuo()
		for cromossomo in self.populacao:
			if(best.id != cromossomo.id): #nao executa mutacao no melhor individuo
				self.mutacao(cromossomo)

	
	def imprimePopulacao(self):
		print len(self.populacao)
		for cromossomo in self.populacao:
			print cromossomo.toString() + " " + self.getConfiguracaoMochila(cromossomo)


	def getConfiguracaoMochila(self,cromossomo):
		pesoTotal = 0
		valorTotal = 0
		for i in range(0,len(cromossomo.genes)):
			if(cromossomo.genes[i]==1):
				pesoTotal += self.pesos[i]
				valorTotal += self.valores[i]
		return "peso: " + str(pesoTotal)+", valor: "+ str(valorTotal) + ", fitness: " + str(cromossomo.fitness)


	def getMelhorIndividuo(self):
		return max(self.populacao, key=attrgetter('fitness'))


	def simulaPesos(self,qtdeItens, maxPeso):
		self.pesos = []
		for i in range(0,qtdeItens):
			self.pesos.append(random.randrange(maxPeso)) 

	def simulaValores(self,qtdeItens,maxValor):
		self.valores=[]
		for i in range(0,qtdeItens):
			self.valores.append(random.randrange(maxValor)) 

	def get_n_melhorsIndividuos(self,n):
		listaOrdenada = sorted(self.populacao, key=lambda x: x.fitness,reverse = True)
		return listaOrdenada[0:n]

	def imprime_n_melhoresIndividuos(self,n):
		listaMelhoresIndividuos = self.get_n_melhorsIndividuos(n)
		for cromossomo in listaMelhoresIndividuos:
			print self.getConfiguracaoMochila(cromossomo)

