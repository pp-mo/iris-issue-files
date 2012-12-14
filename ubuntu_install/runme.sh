
# we can serach for packages to install like this:
#   aptitude search netcdf

# update ubuntu
sudo apt-get update
sudo apt-get upgrade

####### easy auto installs ########

## bits and bobs
#sudo apt-get install libudunits2-dev
#sudo apt-get install libhdf5-serial-dev
#sudo apt-get install libnetcdf-dev
#
## python headers
#sudo apt-get install python2.7-dev
#
## scipy and numpy
#sudo apt-get install python2.7-scipy
#
## pip installer for python packages
#sudo apt-get install python-pip

sudo apt-get install libudunits2-dev libhdf5-serial-dev libnetcdf-dev python2.7-dev python2.7-scipy python-pip make

# python packages
pip install nose cython pyshp shapely pil pep8 mock pyke netCDF4


################################
######### manual builds ########
################################

# dependencies for matplotlib (1.1, but we'll manually intall 1.2)
sudo apt-get build-dep matplotlib

# matplotlib
wget https://github.com/downloads/matplotlib/matplotlib/matplotlib-1.2.0.tar.gz
tar -xfv matplotlib-1.2.0.tar.gz
cd matplotlib-1.2.0
sudo python setup.py install
cd ..
rm -rf matplotlib-1.2.0

# geos
wget http://download.osgeo.org/geos/geos-3.3.6.tar.bz2
tar -xfv geos-3.3.6.tar.bz2
cd geos-3.3.6
./configure
make
sudo make install
cd ..
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
wget http://www.ece.uvic.ca/~frodo/jasper/software/jasper-1.900.1.zip
cd jasper-1.900.1/
./configure
make
sudo make install
cd ..
rm -rf jasper-1.900.1/
	
# gribapi
wget https://software.ecmwf.int/wiki/download/attachments/3473437/grib_api-1.9.18.tar.gz
tar -xfv grib_api-1.9.18.tar.gz
cd grib_api-1.9.18
./configure --with-jasper=/usr/local/lib --disable-fortran --enable-python
sudo make install
cd ..
rm -rf grib_api-1.9.18



############
### iris ###
############

sudo apt-get install python-setuptools

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


###########
# cartopy #
###########

# proj4
wget http://download.osgeo.org/proj/proj-4.8.0.tar.gz
tar -xfv proj-4.8.0.tar.gz
cd proj-4.8.0
./configure
make
sudo make install
cd ..
rm -rf proj-4.8.0

# cartopy
git clone git://github.com/SciTools/cartopy.git
cd cartopy
python setup.py build
sudo python setup.py install
cd ..
rm -rf cartopy

