
# we can serach for packages to install like this:
#   aptitude search netcdf

# update ubuntu
sudo apt-get update
sudo apt-get upgrade

# easy auto installs
sudo apt-get install libudunits2-dev libhdf5-serial-dev libnetcdf-dev python2.7-dev python2.7-scipy python-pip make unzip python-setuptools
pip install nose cython pyshp shapely pil pep8 mock pyke netCDF4


################################
######### manual builds ########
################################

## dependencies for matplotlib (1.1, but we'll install 1.2)
sudo apt-get build-dep matplotlib

# matplotlib - because ubuntu doesn't have the version we need (1.2)
wget https://github.com/downloads/matplotlib/matplotlib/matplotlib-1.2.0.tar.gz
tar -xvf matplotlib-1.2.0.tar.gz
cd matplotlib-1.2.0
python setup.py build
sudo python setup.py install
cd ..
rm matplotlib-1.2.0.tar.gz
rm -rf matplotlib-1.2.0

## geos - because ubuntu doesn't have the version we need (3.3.4)
wget http://download.osgeo.org/geos/geos-3.3.6.tar.bz2
tar -xvf geos-3.3.6.tar.bz2
cd geos-3.3.6
./configure
make
sudo make install
cd ..
rm geos-3.3.6.tar.bz2
rm -rf geos-3.3.6


###############
### gribapi ###
###############
export CFLAGS="-fPIC -m64"
export CPPFLAGS="-fPIC -m64"
export YFLAGS="-fPIC -m64"
export FFLAGS="-fPIC -m64"
export FCFLAGS="-fPIC -m64"
export LDFLAGS="-fPIC -m64"

# jasper
#wget http://www.ece.uvic.ca/~frodo/jasper/software/jasper-1.900.1.zip
#unzip -r jasper-1.900.1.zip
#cd jasper-1.900.1/
#./configure
#make
#sudo make install
#cd ..
#rm jasper-1.900.1.zip
#rm -rf jasper-1.900.1/
sudo apt-get install libjasper-dev
	
# gribapi
sudo apt-get build-dep libgrib-api-1.9.9 libgrib-api-dev libgrib-api-tools

# ubuntu 11
#sudo apt-get install libgrib-api-0d-1 libgrib-api-dev libgrib-api-tools

# ubuntu 12 - this doesn't seem to isntall the python stuff

#sudo apt-get install libgrib-api-1.9.9 libgrib-api-dev libgrib-api-tools

wget https://software.ecmwf.int/wiki/download/attachments/3473437/grib_api-1.9.18.tar.gz --no-check-certificate
tar -xvf grib_api-1.9.18.tar.gz
cd grib_api-1.9.18
./configure --with-jasper=/usr/local/lib --disable-fortran --enable-python
make
sudo make install
cd ..
rm grib_api-1.9.18.tar.gz
rm -rf grib_api-1.9.18
mkdir ~/.local
mkdir ~/.local/lib
mkdir ~/.local/lib/python2.7
mkdir ~/.local/lib/python2.7/site-packages
ln -s /usr/local/lib/python2.7/dist-packages/grib_api ~/.local/lib/python2.7/site-packages/gribapi



###########
# cartopy #
###########

wget http://python-distribute.org/distribute_setup.py
sudo python distribute_setup.py
rm distribute_setup.py

# geos - this gives 3.3.3, we need 3.3.4, hence the manual install above
#sudo apt-add-repository ppa:sharpie/for-science
#sudo apt-get update
#sudo apt-get install libgeos-dev

# proj4
wget http://download.osgeo.org/proj/proj-4.8.0.tar.gz
tar -xvf proj-4.8.0.tar.gz
cd proj-4.8.0
./configure
make
sudo make install
cd ..
rm proj-4.8.0.tar.gz
rm -rf proj-4.8.0

# cartopy
git clone git://github.com/SciTools/cartopy.git
cd cartopy
python setup.py build
sudo python setup.py install
cd ..
rm -rf cartopy


############
### iris ###
############

git clone git://github.com/SciTools/iris.git
cd iris
python setup.py build
sudo python setup.py install
cd ..
rm -rd iris


#
# Also...
#   pp packing
#   graphviz (for dot)
#

