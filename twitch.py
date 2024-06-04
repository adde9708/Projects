import threading


def create_channel_point_reward(id, title, is_user_input_required):
    channel_point_reward = {
        "id": id,
        "title": title,
        "is_user_input_required": is_user_input_required,
    }
    return channel_point_reward


def create_waiting_redemption(reward_id, message, original_content):
    waiting_redemption = {
        "reward_id": reward_id,
        "message": message,
        "original_content": original_content,
    }
    return waiting_redemption


def create_twitch_account(user_name):
    user_name = {"user_name": user_name}
    return user_name


def create_accounts(twitch_account):
    twitch_account = {"twitch_account": twitch_account}
    return twitch_account


def create_app(accounts):
    accounts = {"accounts": accounts}
    return accounts


def create_twitch_channel(name, app):
    twitch_channel = {
        "name": name,
        "app": app,
        "channel_point_rewards": [],
        "waiting_redemptions": [],
        "rewards_count": 0,
        "redemptions_count": 0,
        "lock": threading.Lock(),
    }
    return twitch_channel


def concrete_get_twitch(server):
    twitch_url = "http://twitch.tv/server"
    return twitch_url


def create_concrete_server():
    server = {}
    server["get_twitch"] = concrete_get_twitch
    return server


# Function implementations
def append_channel_point_reward_message(reward):
    reward_message = f"Reward {reward['title']} appended."
    return reward_message


def add_message(message):
    print(message)


def assert_in_gui_thread(thread_id):

    # Store the main thread ID
    main_thread_id = threading.current_thread()
    if main_thread_id != thread_id:
        error = "Function must be called from the GUI thread"
        raise AssertionError(error)


def get_name(channel):
    channel = channel["name"]
    return channel


def get_twitch(server):
    server = server["get_twitch"]()
    return server


def add_waiting_redemption(channel, redemption):
    with channel["lock"]:
        channel["waiting_redemptions"].append(redemption)


def process_message(msg, server):
    base_server = server
    processing_message = f"Processing message for redemption {msg['reward_id']} on Twitch server: {base_server['get_twitch']()}"
    print(processing_message)


def retain_waiting_redemptions(channel, reward_id, server):

    redemption = {}
    with channel["lock"]:
        for redemption in channel["waiting_redemptions"][:]:
            if redemption and redemption["reward_id"] == reward_id:
                process_message(redemption, server)
                channel["waiting_redemptions"].remove(redemption)


def add_channel_point_reward(channel, reward, main_thread_id):
    assert_in_gui_thread(main_thread_id)

    if reward["is_user_input_required"] == 0:
        builder = append_channel_point_reward_message(reward)
        add_message(builder)
        return 0

    channel["channel_point_rewards"].append(reward)
    channel_name = get_name(channel)
    channel_reward_message = f"[TwitchChannel {channel_name}] Channel point reward added: {reward['id']}, {reward['title']}, {reward['is_user_input_required']}"
    print(channel_reward_message)

    server = create_concrete_server()
    retain_waiting_redemptions(channel, reward["id"], get_twitch(server))

    return 0


def main_func():
    account = create_twitch_account("broadcaster_name")
    accounts = create_accounts(account)
    app = create_app(accounts)
    channel = create_twitch_channel("channel_name", app)

    reward = create_channel_point_reward("reward1", "Reward 1", 0)
    add_channel_point_reward(channel, reward, threading.current_thread())


def main():

    main_func()


if __name__ == "__main__":
    main()
