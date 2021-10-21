
message_event_name = "Write event name."
message_title = "Write title."
message_description = "Write description."
message_media = "Sent media"
message_for_change_bot = "Вы создали событие👆👆👆.\n" \
           "Для того, чтобы получать уведомления о сообщениях перейдите в  @teetetettete_bot и напишите старт"


def get_full_user_name(message):
    return f"{message.from_user.first_name} " \
           f"{message.from_user.last_name}"


def mess_about_create_event(data):
    return f"Event name: {data['event_name']}\n" \
           f"Event title: {data['title']}\n" \
           f"Event description: {data['description']}\n" \
           f"End time: {data['end_time']}\n" \
           f"Media: {data['media']}\n"
