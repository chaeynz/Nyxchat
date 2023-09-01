// EventHandler.hpp

#pragma once

#include <map>
#include <vector>
#include <functional>
#include <memory>

#include "include/engine/ErrorHandler.hpp"

template <typename... Args>
class EventHandler {
public:
	using Event = std::function<void()>; 
	using Callback = std::function<void(Args...)>;

	using UserNotFoundHandler = EventHandler<std::string>;

	static std::map <Event, std::vector<Callback>> eventSubscribers;
	            //  <onNetworkInputRecv>,    notify  <correspondingReceiver>;

	static void registerCallback(const Event&, const Callback&);
	static void unregisterCallback(const Event&, const Callback&);
	static void notify(const Event&);

	static void onNetworkInputReceived();
	static void onUserNotFoundLocally();
	
};
template <typename... Args>
std::map<typename EventHandler<Args...>::Event, std::vector<typename EventHandler<Args...>::Callback>> EventHandler<Args...>::eventSubscribers;
