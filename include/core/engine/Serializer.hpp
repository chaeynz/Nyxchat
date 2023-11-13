// Serializer.hpp

#pragma once

#include <string>
#include <regex>
#include <boost/asio.hpp>
#include <components/Message.hpp>

#define serializeMessage(a); boost::asio::buffer(a);

class Serializer
{
public:
	static boost::asio::const_buffer serializeMessageContent(std::string);
	static boost::asio::const_buffer serializeRequestUser(std::string);

	static std::string buffer_to_string(boost::asio::const_buffer);

	static std::string deserializeNetworkStream(boost::asio::const_buffer received);

	static Message deserializeMessage(std::string received);

};



