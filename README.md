## C++ Word Printer Application

This is a simple C++ application that takes a word as a command-line argument and prints it to the console a number of times equal to the length of the word.

### Dependencies

To build and run this application, you need the following installed on your system:

*   **C++ Compiler:** A C++11 compatible compiler (e.g., GCC, Clang).
*   **CMake:** Version 3.10 or higher.

### Building the Application

Follow these steps to build the application:

1.  **Create a build directory:**
    ```bash
    mkdir build
    cd build
    ```

2.  **Configure the project with CMake:**
    ```bash
    cmake ..
    ```

3.  **Build the application:**
    ```bash
    make
    ```

### Static Linking

By default, the application is built with dynamic linking. If you wish to build the `word_printer` executable with static linking (meaning the `word_printer_lib` will be embedded directly into the executable), you can configure CMake with the `BUILD_SHARED_LIBS` option:

1.  **Clean the build directory (optional but recommended):**
    ```bash
    rm -rf build
    cd build
    ```
2.  **Configure for static linking:**
    ```bash
    cmake -DBUILD_SHARED_LIBS=OFF ..
    ```
3.  **Build the application:**
    ```bash
    make
    ```

This will link `word_printer_lib` statically. To attempt a *fully* static executable (including system libraries), you can pass a linker flag:

```bash
# In your build directory
cmake -DCMAKE_EXE_LINKER_FLAGS="-static" ..
make
```

Note that fully static executables are generally larger and might have compatibility issues with some system libraries.

### Running the Application

After building, you can run the `word_printer` executable. Provide a word as a command-line argument:

```bash
./src/word_printer <your_word>
```

**Example:**

```bash
./src/word_printer hello
```

**Expected Output:**

```
hello hello hello hello hello
```

### Running Tests

To run the unit tests for the application:

1.  **Navigate to the build directory (if not already there):**
    ```bash
    cd build
    ```

2.  **Execute tests with CTest:**
    ```bash
    ctest --verbose
    ```
