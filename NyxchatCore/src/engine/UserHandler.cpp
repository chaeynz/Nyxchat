// UserHandler.cpp

#include "include/engine/UserHandler.hpp"


std::shared_ptr<User> UserHandler::queryUser(std::string userID) {
    bool userLocated = false;
    std::shared_ptr<User> matchingUser = findUser(userID);

    if (matchingUser != nullptr) {
        return matchingUser;
    }
    else {
        EventHandler::onUserNotFoundLocally();
        if () {

        }
        else {
            //ErrorHandler::handleUserDoesNotExistError();
        }
    }

}

std::shared_ptr<User> UserHandler::findUser(std::string userID) {
    for (const auto& userPtr : users) {
        if (userPtr->getUserId() == userID) {
            return userPtr;
        }
    }
    return nullptr;
}

