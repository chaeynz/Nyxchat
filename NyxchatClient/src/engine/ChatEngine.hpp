// ChatEngine.hpp


#include "../NyxchatCore/include/engine/NetworkEngine.hpp"
#include "../NyxchatCore/include/components/Message.hpp"
#include "../NyxchatCore/include/components/User.hpp"

class ChatEngine {
	static void chatOutMessage(std::string message);
	static void chatOutMessage(Message* sendMessage, User* receiverUser);
	static void chatInMessage();
};