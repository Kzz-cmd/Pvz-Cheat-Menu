#Importação de bibliotecas
import pymem
import pymem.process,pymem.pattern
from re import escape
from sys import exit

#Inicializando variáveis globais
PROCESS_NAME = "popcapgame1.exe"
PATCH_ADDRS = None

#Checando se o jogo está aberto
try:
    pm = pymem.Pymem(PROCESS_NAME)
except pymem.exception.ProcessNotFound:
        print(f"[-] Erro: O processo '{PROCESS_NAME}' não foi encontrado. O jogo está aberto?")
        exit()

def encontrar_endereco_dinamico(endereco_base,offset_estatico,offset_nivel_1,offset_nivel_2):
    '''Função que calcula o endereço dinâmico atual através de offsets e o endereço base do jogo'''
    endereco_raiz = endereco_base + offset_estatico
    valor_nivel_3 = pm.read_int(endereco_raiz) 
        
    endereco_nivel_2 = valor_nivel_3 + offset_nivel_2
    valor_nivel_2 = pm.read_int(endereco_nivel_2)

    return valor_nivel_2 + offset_nivel_1

def menu():
    print('===' * 3)
    print(' ' * 2,'menu',' ' * 3)
    print('===' * 3)
    print('1.Mudar Sóis')
    print('2.Mudar Dinheiro')
    print('3.Tirar Cooldowns de plantas')
    print('4.Sair')
    print('Faça sua escolha:')

def hack_sois(novo_valor):
    '''Função que altera a quantia atual dos sóis'''
    #Adquirindo endereço base
    module = pymem.process.module_from_name(pm.process_handle, PROCESS_NAME)
    endereco_base = module.lpBaseOfDll

    #Offsets adquiridos através do cheat engine        
    offset_estatico = 0x331D08
    offset_nivel_2 = 0x868
    offset_nivel_1 = 0x5578

    endereco_dinamico_sol = encontrar_endereco_dinamico(endereco_base,offset_estatico,offset_nivel_1,offset_nivel_2)

    #Alterando o valor atual dos sóis    
    pm.write_int(endereco_dinamico_sol, novo_valor)
        
    print(f"[+] Sucesso! Seus sóis foram alterados para {novo_valor}.")

def hack_cooldowns(estado):
    global PATCH_ADDRS
    
    # Bytes para anular a instrução do jogo
    nop = b"\x90\x90\x90\x90"
    # Bytes originais que o jogo usa para iniciar a contagem da recarga
    original = b"\xC6\x45\x48\x00"
    
    # Assinatura de busca do jogo em seu estado normal/intocado
    AOB_ORIGINAL = escape((b"\x33\xC0" b"\xC6\x45\x48\x00" b"\x89\x45\x24" b"\x89\x45\x28"))

    # Assinatura de busca para o caso do hack já ter sido injetado antes
    AOB_HACKEADO = escape((b"\x33\xC0" b"\x90\x90\x90\x90" b"\x89\x45\x24" b"\x89\x45\x28"))

    # Só faz o scan pesado na memória se os endereços ainda não foram descobertos
    if PATCH_ADDRS is None:
        # Tenta achar o código original
        matches = pymem.pattern.pattern_scan_all(pm.process_handle, AOB_ORIGINAL)

        # Se não achar o original, verifica se já hackeamos a memória antes
        if not matches:
            matches = pymem.pattern.pattern_scan_all(pm.process_handle, AOB_HACKEADO)
            
            if not matches:
                # Se não achou nenhum dos dois, o padrão mudou
                print("Padrão não encontrado na memória.")
                return
            else:
                print("[!] O jogo já estava com os cooldowns alterados da sessão anterior. Endereço recuperado!")

        # O pymem pode retornar um 'int' se achar só um, isso converte para lista
        if isinstance(matches, int):
            matches = [matches]

        # Salva o endereço final pulando os 2 primeiros bytes (\x33\xC0) para escrever no lugar exato
        PATCH_ADDRS = [match + 2 for match in matches]

    # Percorre os endereços e injeta os bytes dependendo do estado do menu
    for addr in PATCH_ADDRS:
        if estado == 0:
            pm.write_bytes(addr, nop, 4) # Apaga a regra da recarga
        else:
            pm.write_bytes(addr, original, 4) # Restaura a regra original
            
    print("Cooldowns: OFF (Sem recarga)" if estado == 0 else "Cooldowns: ON (Normal)")

def hack_dinheiro(quantia):
    '''Função que altera a quantia atual do dinheiro'''
    #Adquirindo endereço base
    module = pymem.process.module_from_name(pm.process_handle,PROCESS_NAME)
    endereco_base = module.lpBaseOfDll

    #Offsets adquiridos através do cheat engine 
    offset_nivel_1 = 0x54
    offset_nivel_2 = 0x94C
    offset_estatico = 0x331D08

    endereco_dinheiro = encontrar_endereco_dinamico(endereco_base,offset_estatico,offset_nivel_1,offset_nivel_2)

    #Alterando o valor atual do dinheiro
    pm.write_int(endereco_dinheiro,quantia)

if __name__ == "__main__":
    #Assumindo que o estado atual dos cooldowns é ligado
    estado = 1

    #Iniciando loop principal do programa
    while True:
        #ECU básico
        menu()
        escolha = int(input())
        
        match escolha:
            case 1:
                try:
                    hack_sois(int(input('Digite a nova quantia de sóis atual:\n')))
                except pymem.exception.MemoryWriteError:
                    print('Erro detectado, pelo menos entre em uma fase')
            case 2:
                hack_dinheiro(int(input('Digite a nova quantia de dinheiro atual:\n'))//10)         
            case 3:
                estado = 1 - estado
                try:
                    hack_cooldowns(estado)
                except AttributeError:
                    print('Erro detectado, pelo menos entre em uma fase')
            case 4:
                break
            case _:
                print('Não existe essa opção')