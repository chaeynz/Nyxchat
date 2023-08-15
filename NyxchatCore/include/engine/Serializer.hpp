// Serializer.hpp
#include <iostream>

#include "include/components/Message.hpp"
class Serializer
{
  int serializeMessage(unsigned long long messageId, std::string messageContent, User* messageAuthor);
};



