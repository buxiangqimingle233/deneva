sudo apt-get -y update
sudo apt-get -y install cmake git python3-pip

root=$(pwd)

# setup nanomsg
mkdir utils/
git clone https://github.com/nanomsg/nanomsg.git
cd utils/nanomsg
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
make 
sudo make install

cd $root
touch ifconfig.txt
