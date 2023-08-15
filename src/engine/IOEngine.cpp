// IOEngine.cpp

#include "IOEngine.hpp"

IOEngine::IOEngine() {
	this->p_socket = new tcp::socket(this->ioContext);

}

IOEngine::~IOEngine() {

}

void IOEngine::listenForMessages(uint16_t listenPort)
{
	tcp::acceptor acceptor(this->ioContext, tcp::endpoint(tcp::v4(), listenPort));

	for(;;) {
		acceptor.accept(*this->p_socket);

		std::array<char, 128> buffer;
		boost::system::error_code error;
		size_t length = this->p_socket->read_some(boost::asio::buffer(buffer), error);

		if (error == boost::asio::error::eof) {
			break;
		}
		else if (error) {
			throw boost::system::system_error(error);
		}
		std::cout << "Received: ";
		std::cout.write(buffer.data(), length);
		std::cout << std::endl;
		break;
	}
}

void IOEngine::sendMessage(std::string& message, std::string& targetIp, uint16_t targetPort) {
	tcp::resolver resolver(this->ioContext);
	tcp::resolver::results_type endpoints = resolver.resolve(targetIp, std::to_string(targetPort));
	boost::asio::connect(*this->p_socket, endpoints);
	boost::asio::write(*this->p_socket, boost::asio::buffer(message));
}