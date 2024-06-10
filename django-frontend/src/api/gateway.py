import mock.chats


# TODO: Remove after implementing real chat messages
def get_mock_global_chat_messages() -> list[dict]:
    mock_global_chat_messages: list[dict] = mock.chats.get_mock_global_chat_messages()
    return mock_global_chat_messages
