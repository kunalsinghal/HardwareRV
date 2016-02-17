#/bin/bash

echo "Enter path to sparc-elf (omit trailing slash)"
read SPARC_ELF_PATH


echo "Path is I$SPARC_ELF_PATH"

export CLANGPP_SPARC='clang++ -v -ccc-host-triple sparc-elf -ccc-gcc-name sparc-elf-gcc -I$SPARC_ELF_PATH/include/c++/3.4.4 -I$SPARC_ELF_PATH/sparc-elf/include -I$SPARC_ELF_PATH/include/c++/3.4.4/sparc-elf'

export CLANG_SPARC='clang -v -ccc-host-triple sparc-elf  -ccc-gcc-name sparc-elf-gcc -I$SPARC_ELF_PATH/sparc-elf/include'

