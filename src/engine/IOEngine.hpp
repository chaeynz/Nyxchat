// IOEngine.hpp

#pragma once

#include <iostream>

#include "../../lib/boost/asio.hpp"
#include "../../lib/boost/asio/ts/buffer.hpp"

using boost::asio::ip::tcp;

class IOEngine
{
private:
	tcp::socket* p_socket;
	boost::asio::io_context ioContext;

public:
	IOEngine();
	~IOEngine();

	void listenForMessages(uint16_t listenPort);

	void sendMessage(std::string& message, std::string& targetIp, uint16_t targetPort);
};

