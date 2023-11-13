// UserHandler.hpp

#pragma once

#include <string>
#include <vector>
#include <memory>

#include <components/User.hpp>
#include <engine/EventHandler.hpp>
#include <engine/ErrorHandler.hpp>

class UserHandler {
public:
	static std::vector<std::shared_ptr<User>> localAvailableUsers;

	static void addUser(User);
	static std::shared_ptr<User> queryUser(std::string);
	static std::shared_ptr<User> findUser(std::string);

	static void downloadNewUser(std::string);
};