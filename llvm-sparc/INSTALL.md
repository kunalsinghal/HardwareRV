Installing LLVM 3.0
====================

1. Download LLVM source code from http://llvm.org/releases/3.0/llvm-3.0.tar.gz
2. Download Clang source code from http://llvm.org/releases/3.0/clang-3.0.tar.gz
3. Untar LLVM source code using `tar xvzf llvm-3.0.tar.gz`
4. Untar Clang source code using `tar xvzf clang-3.0.tar.gz` and move the extracted files to tools/ inside the llvm directory (Remember to rename the extracted clang-3.0 directory to clang)
5. Follow [this guide](https://cmake.org/pipermail/cmake/2012-January/048419.html) and install CMake + Ninja build system.
6. Create a build directory.
`mkdir build-llvm`
`cd build-llvm`
7. Execute this command in the shell replacing path/to/llvm/source/root with the path to the root of your LLVM source tree:

`cmake -G Ninja path/to/llvm/source/root` 
8. Start the build using `cmake --build .`
9. Install it to the build target.
`cmake --build . --target install`


Installing Sparc-ELF cross-compiler
=============================

1. Download the binaries from [here](http://www.gaisler.com/anonftp/bcc/bin/linux/sparc-elf-3.4.4-1.0.45.tar.bz2).
2. Untar the file using `tar xvjf sparc-elf-3.4.4-1.0.45.tar.bz2`.
3. Rename the extracted directory to `sparc-elf`.
4. Add the executables from sparc-elf to your path,
`export PATH=/path/to/sparc-elf/bin:$PATH`
5. If using a 64 bit Ubuntu, download the necessary packages for running 32 bit applications,
`apt-get install libc6-i386`
`apt-get install lib32z1`
6. Check that the sparc compiler is installed by invoking `sparc-elf-gcc` from the command line.
