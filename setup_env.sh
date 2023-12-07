sudo apt-get -y update
sudo apt-get -y install cmake git python3-pip

root=~/deneva

cd $root

# setup nanomsg
mkdir utils/
cd utils/

git clone https://github.com/nanomsg/nanomsg.git
cd nanomsg
mkdir build
cd build
cmake ..
cmake --build .
sudo cmake --build . --target install
sudo ldconfig

cd $root/utils
git clone https://github.com/jemalloc/jemalloc.git
cd jemalloc
./autogen.sh
make -j
sudo make install

cd $root
make deps
make -j
touch ifconfig.txt