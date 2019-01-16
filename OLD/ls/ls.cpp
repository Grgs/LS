#include <algorithm>
#include <array>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

std::string exec(const char *cmd) {
  std::array<char, 128> buffer;
  std::string result;
  std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
  if (!pipe) {
    throw std::runtime_error("popen() failed!");
  }
  while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
    result += buffer.data();
  }
  return result;
}

std::string exec(const std::string command) { return exec(command.c_str()); }

int main(int argc, char **argv) {
  std::string sysCommand("ls -gGAhS --color=always ");
  if (argc > 1) {
    for (int i = 1; i < argc; ++i) {
      sysCommand.append(argv[i]);
      sysCommand.append(" ");
    }
  }
  std::string text = exec(sysCommand);
  /* std::string otext(text.length()); */
  /* std::transform(text.begin(), text.end(), otext.begin(), std::toupper); */
  /* for (std::string::iterator i = text.begin(); i != text.end(); ++i) { */
  /*   std::cout << *i; */
  /* } */
  // std::transform(text.begin(), text.end(), text.begin(), ::toupper);
  std::cout << text << "\n";
  return 0;
}