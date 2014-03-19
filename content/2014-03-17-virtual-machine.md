Title: Virtual Machine
date:  2014-03-17 10:42
comments: true
slug: vmachine


<span style="color:red">Warming!  This post is in Portuguese!!</span>

Todos os [notebooks](http://nbviewer.ipython.org/github/ocefpaf/python4oceanographers/tree/master/content/downloads/notebooks/)
mostrados nesse site e utilizados em aula exigem uma série de módulos Python
que podem ser complicados de instalar.  Para facilitar as aulas onde utilizo
esses notebooks criei uma Máquina Virtual (VM) em `OVF` (Open Virtualization
Format), que pode ser importada tanto pelo
[VMWare Player](https://www.vmware.com/) ou
[VirtualBox](https://www.virtualbox.org/wiki/Downloads).

Essa VM foi criada utilizando a distribuição Linux OpenSUSE, com o
[SUSE Studio](https://susestudio.com/) e contendo um
[repositório](https://build.opensuse.org/project/monitor/home:ocefpaf)
particular com todos os módulos, pacotes e bibliotecas necessárias para rodar
os notebooks.

A máquina já abre um browser (chormium) diretamente na pasta contendo os
notebooks de aula.  Mas, por ser uma distribuição Linux completa, é possível
utiliza-lá normalmente como qualquer outra instalação de Linux.  Só não é
recomendado utilizar essa VM como sua principal estação de trabalho devido à
natureza instável dos pacotes nos repositórios.  (Todos são atualizados
semanalmente diretamente do seu repositório oficial.)

Bom, por enquanto é só,
[baixe a máquina](https://susestudio.com/a/YfJVDT/python4oceanographers--2)
e um ambiente virtualizador de sua preferência, otimize as configuração da
máquina para o seu ambiente (Memória RAM, forma de conectar à internet e etc)
e boas aulas.

ps: O download é pesado ~1,6 gigas!
