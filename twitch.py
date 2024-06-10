import threading


def create_channel_point_reward(channel_id, title, is_user_input_required):
    channel_reward = {
        "id": channel_id,
        "title": title,
        "is_user_input_required": is_user_input_required,
    }
    return channel_reward


def create_waiting_redemption(reward_id, message, original_content):
    waiting_redemption = {
        "reward_id": reward_id,
        "message": message,
        "original_content": original_content,
    }
    return waiting_redemption


def create_twitch_account(user_name):
    user = {"user_name": user_name}
    return user


def create_twitch_channel(name, user_name):
    twitch_channel = {
        "name": name,
        "user_name": user_name,
        "channel_point_rewards": [],
        "waiting_redemptions": [],
        "rewards_count": 0,
        "redemptions_count": 0,
        "lock": threading.Lock(),
    }
    return twitch_channel


def get_twitch_url():
    twitch_url = "http://twitch.tv/server"
    return twitch_url


def append_channel_point_reward_message(reward):
    reward_message = f"Reward {reward['title']} appended."
    return reward_message


def add_message(message):
    print(message)


def assert_in_gui_thread(main_thread_id):
    current_thread_id = threading.current_thread().ident
    if current_thread_id != main_thread_id:
        error = "Function must be called from the GUI thread"
        raise AssertionError(error)


def get_name(channel):
    channel_name = channel["name"]
    return channel_name


def add_waiting_redemption(channel, redemption):
    with channel["lock"]:
        channel["waiting_redemptions"].append(redemption)
        return channel["waiting_redemptions"]


def process_message(msg, server):
    process_message = f"Processing message for redemption {msg['reward_id']} on Twitch server: {server}"
    print(process_message)


def retain_waiting_redemptions(channel, reward_id, server):
    with channel["lock"]:
        new_waiting_redemptions = []
        for redemption in channel["waiting_redemptions"]:
            if redemption["reward_id"] != reward_id:
                new_waiting_redemptions.append(redemption)
            else:
                process_message(redemption, server)
        channel["waiting_redemptions"] = new_waiting_redemptions
        return new_waiting_redemptions


def add_channel_point_reward(channel, reward, main_thread_id):
    assert_in_gui_thread(main_thread_id)
    if reward["is_user_input_required"] == 0:
        builder = append_channel_point_reward_message(reward)
        add_message(builder)
        return channel

    channel["channel_point_rewards"].append(reward)
    channel_name = get_name(channel)
    reward_id = reward["id"]
    reward_title = reward["title"]
    reward_required = reward["is_user_input_required"]
    channel_point_message = f"[TwitchChannel {channel_name}] Channel point reward added: {reward_id}, {reward_title}, {reward_required}"
    print(channel_point_message)

    server = get_twitch_url()
    retain_waiting_redemptions(channel, reward_id, server)

    return channel


def main_func(
    user_name,
    channel_name,
    reward_id,
    reward_title,
    is_user_input_required,
    main_thread_id,
):
    twitch_account = create_twitch_account(user_name)
    twitch_channel = create_twitch_channel(channel_name, twitch_account["user_name"])

    reward = create_channel_point_reward(
        reward_id, reward_title, is_user_input_required
    )
    channel = add_channel_point_reward(twitch_channel, reward, main_thread_id)

    return channel


def main():
    user_name = "broadcaster_name"
    channel_name = "channel_name"
    reward_id = "reward1"
    reward_title = "Reward 1"
    is_user_input_required = 0

    main_thread_id = threading.current_thread().ident

    channel = main_func(
        user_name,
        channel_name,
        reward_id,
        reward_title,
        is_user_input_required,
        main_thread_id,
    )
    print(f"Final channel state: {channel}")


if __name__ == "__main__":
    main()
