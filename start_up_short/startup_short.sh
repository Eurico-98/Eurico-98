#!/bin/bash

# Github gh
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

sudo apt update
sudo apt -y install \
csh \
cmake \
ghostscript \
subversion \
build-essential \
autoconf \
libpcre3-dev \
libfftw3-dev \
libnetcdf-dev \
libtiff5-dev \
libhdf5-dev \
libgdal-dev gdal-bin \
wget \
liblapack-dev \
gfortran \
g++ \
libgmt-dev \
gmt-dcw gmt-gshhg gmt \
make \
python3-pip \
parallel \
unzip \
gh \
iotop

pip3 install asf_search

###################
# Mount SSD Array #
###################
sudo apt update && sudo apt -y install mdadm --no-install-recommends
# List
lsblk
# Combine
sudo mdadm --create /dev/md0 --level=0 --raid-devices=8 \
/dev/nvme0n1 /dev/nvme0n2 /dev/nvme0n3 /dev/nvme0n4 \
/dev/nvme0n5 /dev/nvme0n6 /dev/nvme0n7 /dev/nvme0n8

sudo mkfs.ext4 -F /dev/md0
# Make mount directory
mkdir ssdarray
sudo mount /dev/md0 ./ssdarray
sudo chown -R $USER ~/ssdarray

############
# Software #
############

mkdir software
cd software


##################
# Install GMTSAR #
##################

#gh repo clone gmtsar/gmtsar
git clone https://github.com/gmtsar/gmtsar.git
sudo chown -R $USER gmtsar
cd gmtsar

autoconf
autoupdate
./configure
# Edit config.mk with -z muldefs in CFLAGS and LDFLAGS
cflags=$(grep "^CFLAGS" ./config.mk)
ldflags=$(grep "^LDFLAGS" ./config.mk)
sed -i "s/^CFLAGS.*/$cflags -z muldefs/g" config.mk
sed -i "s/^LDFLAGS.*/$ldflags -z muldefs/g" config.mk
make
make install
# Edit ~/.bashrc add GMTSAR="gmtsarfolder" and GMTSAR_BIN="gmtsarfolder/bin"
echo 'export GMTSAR="~/software/gmtsar"' >> ~/.bashrc
echo 'export GMTSAR_BIN="$GMTSAR/bin"' >> ~/.bashrc
echo 'export PATH="$GMTSAR:$GMTSAR_BIN:$PATH"' >> ~/.bashrc
source ~/.bashrc
#############################
# Download Spotlite Scripts #
#############################

cd ~/software
#gh repo clone SteffanDavies/GMTSAR_SBAS_AUTOMATION
# clone private repo using only PAT 
git clone https://"$1"@github.com/SteffanDavies/GMTSAR_SBAS_AUTOMATION.git

# meu PAT do git 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

###########
# Python3 #
###########

#import asf_search as asf
#import os
#session = asf.ASFSession().auth_with_creds('ej_98', 'atadHtrae_@_192837')
#wkt=''
#results = asf.geo_search(platform=[asf.PLATFORM.SENTINEL1], intersectsWith=wkt, processingLevel='SLC', start='2020-06-01', end='2022-07-01', relativeOrbit='', asfFrame='')
#results.download(path=os.getcwd(), session=session, processes=70)

