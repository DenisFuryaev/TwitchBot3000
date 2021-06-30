import irc.bot
import threading


class TwitchBot3000(irc.bot.SingleServerIRCBot):
    """
        This is Twitch Bot that can print messages from twitch chat to console
        and has some commands that you can see by typing [help] to console
    """

    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.bot_nickname = "DFdens"
        self.users_dict = {}
        self.message_count = 0
        self.show_msg = False
        self.statistics = False

        server = 'irc.chat.twitch.tv'
        port = 6667
        token = "thdpzkdobrqqqaihfo23p7x5gaaw1j"
        username = "notbot"
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    def on_welcome(self, c, event):
        print("Welcome to ChatBot3000")
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel_name)

    def on_pubmsg(self, c, event):
        self.message_count += 1
        chat_message = event.arguments[0]
        user_nickname = event.source.nick

        if self.show_msg:
            print(user_nickname + " [said] " + chat_message)

        if self.bot_nickname in chat_message:
            self.connection.privmsg(self.channel_name, "Привет @" + user_nickname)

        if user_nickname in self.users_dict:
            self.users_dict[user_nickname] += 1
        else:
            self.users_dict[user_nickname] = 1

        return

    def write_statistics(self, threshold):
        if self.message_count % threshold == 0:
            self.users_dict = dict(sorted(self.users_dict.items(), key=lambda item: item[1], reverse=True))
            with open("ChatUsersStatistics.txt", "w") as file:
                file.write(str(self.users_dict))

    def __del__(self):
        self.users_dict = dict(sorted(self.users_dict.items(), key=lambda item: item[1], reverse=True))
        with open("ChatUsersStatistics.txt", "w") as file:
            file.write(str(self.users_dict))


def user_input(bot):
    print("User input is listened")
    while True:
        cmd = input().strip()
        if cmd == "quit":
            del bot
            break
        if "show msg" in cmd:
            bot.show_msg = True
        if "hide msg" in cmd:
            bot.show_msg = False
        if "help" in cmd:
            print("User Commands:")
            print("[show msg] - to start printing messages from chat to terminal")
            print("[hide msg] - to pause printing messages from chat to terminal")
            print("[quit] - to quit the app")


def main():
    channel_name = "zloyn"
    bot = TwitchBot3000(f"#{channel_name}")

    try:
        x = threading.Thread(target=user_input, args=[bot])
        y = threading.Thread(target=bot.start, args=[])
        y.start()
        x.start()
        x.join()
        y.join()
    except:
        print("Error: unable to start thread")


if __name__ == "__main__":
    main()




# type: #pubmsg,
# source: lil_chacha123!lil_chacha123@lil_chacha123.tmi.twitch.tv,
# target: #vatarls,
# arguments: ['агрессатура пошла Jebaited'],
# tags: [{'key': 'badge-info', 'value': None},
# {'key': 'badges', 'value': None},
# {'key': 'color', 'value': None},
# {'key': 'display-name', 'value': 'lil_chacha123'},
# {'key': 'emotes', 'value': '114836:18-25'},
# {'key': 'first-msg', 'value': '0'},
# {'key': 'flags', 'value': None},
# {'key': 'id', 'value': '39a28298-d34f-467c-ad04-bb47a639bed8'},
# {'key': 'mod', 'value': '0'},
# {'key': 'room-id', 'value': '452952336'},
# {'key': 'subscriber', 'value': '0'},
# {'key': 'tmi-sent-ts', 'value': '1624982863880'},
# {'key': 'turbo', 'value': '0'},
# {'key': 'user-id', 'value': '210918387'},
# {'key': 'user-type', 'value': None}]