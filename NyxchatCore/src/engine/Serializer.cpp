// Serializer.cpp

#include "include/engine/Serializer.hpp"

boost::asio::const_buffer Serializer::serializeMessageContent(std::string messageContent)
{
	return boost::asio::buffer(messageContent);
}