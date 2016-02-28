clang --version | grep -q 3.0
if [[ $? != 0 ]]; then echo "Check clang setup. Version should be 3.0"; exit; fi

which sparc-elf-gcc 1> /dev/null
if [[ $? != 0 ]]; then echo "Sparc-ELF cross-compiler not in PATH"; exit; fi


