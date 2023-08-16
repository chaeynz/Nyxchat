// Serializer.hpp

#pragma once

#include <boost/asio.hpp>

#include "include/components/Message.hpp"

#define serializeMessage(a); boost::asio::buffer(a);

class Serializer
{
public:
	static boost::asio::const_buffer serializeMessageContent(std::string messageContent);
};



