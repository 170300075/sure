#!/bin/bash

# Actualizar repositorio y paquetes
sudo apt-get update -y
sudo apt-get upgrade -y

# Instalar los repositorios actualizados de CRAN
# para obtener la versión mas actualizada de R
# install two helper packages we need
sudo apt install --no-install-recommends software-properties-common dirmngr
# add the signing key (by Michael Rutter) for these repos
# To verify key, run gpg --show-keys /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc 
# Fingerprint: E298A3A825C0D65DFD57CBB651716619E084DAB9
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
# add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"

# Instalar R
sudo apt install --no-install-recommends r-base -y

# Instalar Shiny en R
sudo su - \
-c "R -e \"install.packages('shiny', repos='https://cran.rstudio.com/')\""

# Instalar algunos paquetes que se necesitan
# antes de instalar shiny-server
sudo apt-get install gdebi-core -y
# Descargar el instalador de shiny-server
wget https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.18.987-amd64.deb
# Instalar shiny-server usando gdebi
sudo gdebi shiny-server-1.5.18.987-amd64.deb

# Instalar Python 3.10
sudo apt-get install python3.10 -y

# Instalar git
sudo apt-get install git -y

# Instalar java jre
sudo apt-get install default-jre default-jdk -y

# Instalar dependencias necesarias por las bibliotecas
sudo apt-get install libcurl4-openssl-dev libssl-dev libmariadb-dev libxml2-dev libssl-dev libsasl2-dev -y
# Instalar bibliotecas necesarias para R
Rscript dependencies.R

# Instalar PIP
sudo apt-get install python3-pip -y

# Instalar bibliotecas necesarias para Python
pip install -r requirements.txt

# Dirigirse a la carpeta del servidor shiny
cd srv/shiny-server

# Clonar el repositorio con el codigo fuente
sudo git clone https://github.com/170300075/PT-SURE

# Mas dependencias
sudo apt-get install libpng-dev libudunits2-dev libprotobuf-dev libjq-dev gfortran-9 gfortran libfontconfig1-dev -y
sudo apt-get install libblas-dev liblapack-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev -y

#install Xvfb
sudo apt-get install xvfb

#set display number to :99
Xvfb :99 -ac &
export DISPLAY=:99    

#you are now having an X display by Xvfb