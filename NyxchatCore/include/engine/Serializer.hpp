// Serializer.hpp
#include <iostream>
#include <vector>

#include "include/components/Message.hpp"

class Serializer
{
  std::vector<char> serializeMessage(unsigned long long messageId, std::string messageContent, User* messageAuthor);
};



