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
    channel_point_rewards = []
    twitch_channel = {
        "name": name,
        "user_name": user_name,
        "channel_point_rewards": channel_point_rewards,
        "channel_point_rewards_len": len(channel_point_rewards),
        "channel_point_rewards_capacity": len(channel_point_rewards),
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


def assert_in_gui_thread(current_thread_id):
    main_thread_id = threading.main_thread().ident
    if current_thread_id != main_thread_id:
        error = "Function must be called from the GUI thread"
        raise AssertionError(error)


def get_name(channel):
    channel_name = channel["name"]
    return channel_name


def add_waiting_redemption(channel, redemption):
    channel_lock = channel["lock"]
    with channel_lock:
        waiting_redemptions_len = channel["waiting_redemptions_len"]
        waiting_redemptions_capacity = channel["waiting_redemptions_capacity"]

        if waiting_redemptions_len == waiting_redemptions_capacity:

            initial_capacity = 4

            new_capacity = (
                initial_capacity
                if waiting_redemptions_capacity == 0
                else waiting_redemptions_capacity * 2
            )

            waiting_redemptions = channel["waiting_redemptions"]
            waiting_redemptions += [None] * (
                new_capacity - waiting_redemptions_capacity
            )

            waiting_redemptions_capacity = new_capacity

        waiting_redemptions[waiting_redemptions_len] = redemption
        waiting_redemptions_len += 1

    return waiting_redemptions


def process_message(msg, server):
    processing_message = f"Processing message for redemption {msg['reward_id']} on Twitch server: {server}"
    print(processing_message)


def retain_waiting_redemptions(channel, reward_id, server):
    channel_lock = channel["lock"]

    with channel_lock:
        waiting_redemptions = channel["waiting_redemptions"]
        new_waiting_redemptions = []

        for redemption in waiting_redemptions:
            if redemption["reward_id"] == reward_id:
                process_message(redemption, server)
            else:
                new_waiting_redemptions.append(redemption)

        waiting_redemptions = new_waiting_redemptions

    return new_waiting_redemptions


def add_channel_point_reward(channel, reward, current_thread_id):
    assert_in_gui_thread(current_thread_id)
    if reward["is_user_input_required"] == 0:
        builder = append_channel_point_reward_message(reward)
        add_message(builder)

    channel_point_reward_message = (
        f"Channel point reward added: {reward['id']}, {reward['title']}"
    )
    print(channel_point_reward_message)
    reward_id = reward["id"]
    server = get_twitch_url()
    retain_waiting_redemptions(channel, reward_id, server)
    return channel


def main_func(
    user_name,
    channel_name,
    reward_id,
    reward_title,
    is_user_input_required,
    current_thread_id,
):

    twitch_account = create_twitch_account(user_name)
    twitch_channel = create_twitch_channel(channel_name, twitch_account["user_name"])

    reward = create_channel_point_reward(
        reward_id, reward_title, is_user_input_required
    )
    channel = add_channel_point_reward(twitch_channel, reward, main_thread_id)

    return channel_point_reward


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
        current_thread_id,
    )

    print(f"Final channel state: Channel created successfully: {channel}")


if __name__ == "__main__":
    main()
