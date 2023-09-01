// Serializer.cpp

#include "include/engine/Serializer.hpp"

boost::asio::const_buffer Serializer::serializeMessageContent(std::string messageContent)
{
	return boost::asio::buffer(messageContent);
}

boost::asio::const_buffer Serializer::serializeRequestUser(std::string userID) {
    return boost::asio::buffer(userID);
}

std::string Serializer::buffer_to_string(boost::asio::const_buffer received) {
	const char* data = boost::asio::buffer_cast<const char*>(received);
	std::size_t size = boost::asio::buffer_size(received);

	std::string result(data, size);
	return result;
}



std::string Serializer::deserializeNetworkStream(boost::asio::const_buffer received) {
	std::string data = buffer_to_string(received);


}

Message Serializer::deserializeMessage(std::string received) {
    std::regex pattern("NYXC 1\\.0\\\\TRANSMIT\\(\"([^\"]*)\"\\);SENDER\\[\"([^\"]*)\"\\];RECEIVER\\[\"([^\"]*)\"\\];TIME\\[\"([^\"]*)\"\\];CONTENT\\[\"([^\"]*)\"\\]\\\\N\\d+");

    std::smatch matches;
    if (std::regex_match(received, matches, pattern)) {
        Message msg(matches[2], matches[3], matches[4], matches[5]);
        // Sender, Receiver, Timestamp, Content
    }
    else {
        throw std::runtime_error("Invalid NYXC format");
    }

    return msg;
}