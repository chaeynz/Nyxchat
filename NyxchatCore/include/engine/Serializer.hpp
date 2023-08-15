// Serializer.hpp
#include <iostream>
#include "include/components/Message.hpp"
#include <boost/asio.hpp>

class Serializer
{
  boost::asio::buffer serializeMessage(unsigned long long messageId, std::string messageContent, User* messageAuthor);
};



