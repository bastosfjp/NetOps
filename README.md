# 🛠️ NetOps — Canivete Suíço de Redes
 
Ferramenta CLI para diagnóstico e análise de redes, desenvolvida em Python.
Reúne as principais ferramentas de troubleshooting em um único lugar, com interface interativa no terminal.
 
> ⚠️ **Versão inicial** — projeto em desenvolvimento para fins de estudo e testes. Novas funcionalidades sendo implementadas progressivamente.
 
---
 
## ✨ Funcionalidades implementadas
 
### 🖥️ Interface e sistema
 
- Banner ASCII na inicialização com identidade visual do projeto
- Painel de informações do sistema exibido ao iniciar: versão, data/hora, hostname, IP local, IP público, localidade e provedor/ASN
- Menu principal dividido por categorias com submenus independentes
- Navegação hierárquica — cada área tem seu próprio menu com opção de voltar
 
### 🔹 Conectividade
 
**Ping**
- Teste de conectividade ICMP com host ou IP
- Suporte a IPv4 e IPv6 (seleção manual pelo usuário)
- Quantidade de pacotes configurável
- Validação de entrada
- Compatível com Windows e Linux/Mac
 
**Traceroute**
- Mapeamento de rota até o destino hop a hop
- Output em tempo real — cada hop aparece conforme é descoberto
- Compatível com Windows (`tracert`) e Linux/Mac (`traceroute`)
 
### 🔹 Diagnóstico
 
**Port Scanner**
- Varredura de portas TCP nas principais portas de serviços conhecidos
- Resolução automática de hostname para IP
- Resultado exibido em tabela formatada com status de cada porta
- Identificação de serviços (SSH, HTTP, FTP, MySQL, etc.)
 
### 🔹 Serviços Web
 
**DNS Lookup**
- Consulta de registros A, AAAA, MX, NS e TXT
- Resultado exibido em tabela com tipo, valor e TTL
- Via `dnspython`
 
**HTTP Check**
- Verificação de status HTTP e tempo de resposta
- Exibição de headers relevantes (Content-Type, Server)
- Suporte a redirecionamentos automáticos
- Via `requests`
 
---
 
## 🚀 Como usar
 
### Pré-requisitos
 
- Python 3.10+
- pip
 
### Instalação
 
```bash
git clone https://github.com/seu-usuario/netops.git
cd netops
python -m venv venv
 
# Windows
venv\Scripts\activate
 
# Linux/Mac
source venv/bin/activate
 
pip install -r requirements.txt
```
 
### Rodando
 
```bash
python main.py
```
 
O terminal exibe o banner, as informações do sistema e o menu principal. Navegue pelas categorias digitando o número correspondente.
 
---
 
## 📁 Estrutura do projeto
 
```
netops/
├── main.py              # ponto de entrada e banner
├── cli.py               # menus e navegação
├── requirements.txt     # dependências
├── tools/
│   ├── __init__.py
│   ├── ping.py          # ferramenta de ping
│   ├── tracert.py       # ferramenta de traceroute
│   ├── portscan.py      # scanner de portas
│   ├── dns.py           # consulta DNS
│   └── http_check.py    # verificação HTTP
└── utils/
    ├── __init__.py
    └── sysinfo.py       # informações do sistema e IP público
```
 
---
 
## 📦 Dependências
 
| Biblioteca | Uso |
|---|---|
| `rich` | Interface colorida no terminal, tabelas e painéis |
| `subprocess` | Execução de comandos do sistema (ping, tracert) |
| `socket` | Comunicação de rede de baixo nível (port scan, IP local) |
| `sys` | Detecção do sistema operacional |
| `requests` | Verificação HTTP e consulta de IP público |
| `dnspython` | Consultas DNS |
| `datetime` | Data e hora na inicialização |
 
---
 
## 🗺️ Roadmap
 
### Em desenvolvimento
 
- [ ] **SSL Check** — validade, emissor e dados do certificado HTTPS
 
### Próximas features
 
- [ ] **Exportação de relatórios** — salvar resultados em JSON ou TXT com timestamp
- [ ] **Histórico de execuções** — log local das últimas verificações realizadas
- [ ] **Banner Grabbing** — identificação de versão de serviços em portas abertas
- [ ] **Monitor de host** — ping contínuo com alerta quando host cai ou volta
- [ ] **Whois** — consulta de informações de registro de domínios e IPs
- [ ] **Scan de range de IPs** — varredura de múltiplos hosts em uma sub-rede
- [ ] **Teste de velocidade** — medição de latência e throughput da conexão
- [ ] **Suporte a argumentos diretos via CLI** — `python main.py ping 8.8.8.8` sem menu interativo (`argparse`)
 
### Melhorias técnicas
 
- [ ] Testes automatizados com `pytest`
- [ ] Suporte a arquivo de configuração (hosts favoritos, portas customizadas)
- [ ] Empacotamento como executável standalone com `PyInstaller`
 
---
 
## 🤝 Contribuindo
 
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
 
---

## 👤 Autor

Desenvolvido por **João Pedro Bastos Fernandes**

Estudante de Sistemas de Informação, entusiasta de redes, automação, Linux e tecnologia em geral.


[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/bastosfjp/)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/bastosfjp)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://instagram.com/bastosfjp)

---

