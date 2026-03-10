import streamlit as st

         
def media(notas): #calc avg for each std
    media_aluno = {}
    for aluno, nota in notas.items():
        total = sum(nota)
        qntd_notas = len(nota)
        calculo = round((total / qntd_notas),1)
        media_aluno[aluno] = calculo #indented in the loop, so it's for each std
    return media_aluno #outta the loop, so collects the last result (if it were in the loop, would store only the last run)

def analisar_medias(resultado_media): #gets highest and lowest avg
    maior_nota = max(resultado_media.values())
    menor_nota = min(resultado_media.values())
    for aluno, media in resultado_media.items(): #goes through dict to get the match
        if maior_nota == media:
            aluno_maior = aluno
        elif menor_nota == media:
            aluno_menor = aluno
    return aluno_maior, aluno_menor

def remover_aluno(nome, turma):
    if nome in turma: 
        turma.pop(nome)
        return True
    return False
        


## COLLECT DATA ##

if 'notas_turma' not in st.session_state:
    st.session_state.notas_turma = {}

match st.session_state.notas_turma:
    case {}:
        tipo_processo = 'adicionar'
    case _:
        tipo_processo = st.text_input('Você deseja remover ou adicionar alunos? Preencha com "remover" ou "adicionar"')
    
match tipo_processo:
            case 'adicionar': 
                qnt_alunos = int(st.number_input('Quantos alunos?', min_value=1, step=1))

                for i in range(qnt_alunos):
                    aluno = st.text_input('Digite o nome do aluno', key=f'aluno_{i}')
                    
                    if st.button('Adicionar aluno', key=f'btn_{i}'):
                        if aluno in st.session_state.notas_turma:
                            st.warning('Nome já existe')
                        else:
                            qnt_notas = int(st.number_input('Quantas notas?', min_value=1, max_value=10, step=1, key=f'nota_{i}')) #quantas notas para aquele aluno
                            
                            notas_aluno = [] #crio lista vazia para aquele aluno

                            for x in range (qnt_notas): #runs once for each grade
                                
                                nota = float(st.number_input(f'Digite a {x+1} nota:', min_value=0, max_value=10, step=1, key=f'nota_{i}_{x}'))
                                notas_aluno.append(nota) #add grade to each  students list
                            st.session_state.notas_turma[aluno] = notas_aluno #cria {aluno:lista de notas}
            case 'remover': 
                aluno_removido = st.text_input('Qual o nome do aluno? Preencha nome completo')
                status_remover = st.selectbox(f'Confirma remover o aluno {aluno_removido} da lista?',  ['sim', 'nao'])
                if status_remover == 'sim':
                    remover_aluno(aluno_removido,st.session_state.notas_turma)
                    st.write(f'{aluno_removido} foi removido com sucesso')
            case _:
                st.write('Entrada inválida, tente novamente')

        
## PROCESS AND DATA OUTPUT##

resultado_media = media(st.session_state.notas_turma) 
for aluno, nota in resultado_media.items():
    st.warning(f'Aluno {aluno}, nota: {nota}')
if len(resultado_media) > 1:
    aluno_maior, aluno_menor = (analisar_medias(resultado_media))
    st.warning(f'A maior média é {(resultado_media[aluno_maior])} do aluno {aluno_maior}')
    st.warning(f'A menor média é {(resultado_media[aluno_menor])} do aluno {aluno_menor}')


