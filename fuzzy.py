import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
quantidade = ctrl.Antecedent(np.arange(0, 9, 2), 'quantidade')
tempo = ctrl.Antecedent(np.arange(0, 11, .5), 'tempo')

#Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 11, 2), 'peso')

# automf -> Atribuição de categorias automaticamente
quantidade['pouco'] =    fuzz.trapmf(quantidade.universe, [-5,0,2,4])
quantidade['razoavel'] = fuzz.trapmf(quantidade.universe, [2,4,6,8])
quantidade['bastante'] = fuzz.trapmf(quantidade.universe, [4,6,8,10])

tempo['pouco'] = fuzz.trapmf(tempo.universe, [-.5,0,.5,2])
tempo['medio'] = fuzz.trapmf(tempo.universe,[.5,2,3.5,5])
tempo['bom'] = fuzz.trapmf(tempo.universe,[3.5,5,7.5,10])

# atribuicao sem o automf
peso['leve'] = fuzz.trapmf(peso.universe, [-5,0,2,4])
peso['medio'] = fuzz.trapmf(peso.universe,[2,4,6,8])
peso['pesado'] = fuzz.trapmf(peso.universe,[6,8,10,11])


#Visualizando as variáveis
#quantidade.view()
#tempo.view()
#peso.view()



#Criando as regras
regra_1 = ctrl.Rule(quantidade['pouco'] & tempo['pouco'], peso['leve'])
regra_2 = ctrl.Rule(quantidade['razoavel'] & tempo['pouco'], peso['medio'])
regra_3 = ctrl.Rule(quantidade['razoavel']  & tempo['bom'], peso['leve'])
regra_4 = ctrl.Rule( quantidade['bastante'] & tempo['bom'], peso['medio'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3,regra_4])


#Simulando
Calculopeso = ctrl.ControlSystemSimulation(controlador)

notaquantidade = int(input('quantidade em Kcal: '))
notatempo = int(input('tempo de atividade fisica por semana: '))
Calculopeso.input['quantidade'] = notaquantidade  /1000
Calculopeso.input['tempo'] = notatempo/ 100
Calculopeso.compute()

valorpeso = Calculopeso.output['peso']

print("\nquantidade %dKCal\ntempo de exercício semanal %d minutos\npeso de %5.2fKg" %(
        notaquantidade, 
        notatempo,
        valorpeso*10))


quantidade.view(sim=Calculopeso)
tempo.view(sim=Calculopeso)
peso.view(sim=Calculopeso)

plt.show()