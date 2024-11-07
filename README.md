Trabalho 2 - Descrição
O trabalho consiste em desenvolver um probe RMON. O probe deve receber como parâmetro de execução o nome das interfaces que serão utilizadas para monitorar a rede. O probe deve ser capaz de receber requisições SNMP (versão 2c) para criação de relatórios e coleta de dados, conforme especificado nos grupos do RMON.

Exemplo de execução do probe (para monitorar as interfaces lo, eth0 e eth1)

$ probe lo eth0 eth1
O probe deverá suportar obrigatoriamente os seguintes grupos: statistics e history. Além destes grupos, o probe RMON deverá implementar outros 2 grupos quaisquer da MIB do RMON1 ou RMON2.

Sugestão de ferramentas a serem utilizadas

net-snmp (http://www.net-snmp.org/)

Scapy (https://scapy.net/)

Links úteis

https://mibs.observium.org/mib/RMON-MIB/

https://datatracker.ietf.org/doc/rfc2819/

https://mibs.observium.org/mib/RMON2-MIB/

https://datatracker.ietf.org/doc/rfc4502

Detalhes para construção do probe:

o probe deve ser executado a partir de um terminal por linha de comando de acordo com o exemplo apresentado - não deve ser necessário utilizar uma IDE para executar o probe!!!

o probe pode ser implementado em qualquer linguagem (é sugerido o uso de Python, mas podem ser usadas outras linguagens)

Itens a serem entregues:

código fonte

relatório (em pdf) contendo:

(i) detalhes de implementação (linguagem, classes, principais métodos);

(ii) descrição de como configurar e executar o probe;

(iii) apresentação de um exemplo de utilização para cada grupo implementado;

(iv) limitações da implementação e dificuldades.

OBSERVAÇÕES

O trabalho deve ser realizado em grupos de no máximo 3 alunos.

Não serão aceitos trabalhos atrasados e/ou enviados por e-mail.

Trabalhos que não executam não serão avaliados.

Todos os trabalhos serão analisados e comparados. Caso seja identificada cópia de trabalhos, todos os trabalhos envolvidos receberão nota ZERO!



Ambiente Virtual 
python3 -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
