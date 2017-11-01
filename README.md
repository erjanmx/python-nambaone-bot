# Python NambaOne Bot

[![Build Status](https://travis-ci.org/erjanmx/python-nambaone-bot.svg?branch=master)](https://travis-ci.org/erjanmx/python-nambaone-bot)

[NambaOne BotAPI](https://namba1.co/bot_creation) wrapper

### Installing

You can install or upgrade python-nambaone-bot with:

```$ pip install nambaone --upgrade```

### Methods

#### Bot

- Contructor
```python
Bot(token,
    base_url=None,                  # api endpoint (https://api.namba1.co by default)
    error_handler=None,             # error handler function that should accept Update and Error objects
    
                                    # following handlers should accept Bot and Update objects
    user_follow_handler=None,        
    user_unfollow_handler=None,     
    message_new_handler=None,
    message_update_handler=None,
    chat_new_handler=None
   )
```
- Send message
```python
Bot.send_message(chat_id, content, content_type) # according to api docs, returns Message object or raises nambaone.ClientException
```
- Create chat
```python
Bot.create_chat(user_id, name='', image='')      # according to api docs, returns Chat object or raises nambaone.ClientException
```
- Start typing
```python
Bot.typing_start(chat_id)                        # sends `typing` event to chat or raises nambaone.ClientException
```
- Stop typing
```python
Bot.typing_stop(chat_id)                         # sends `stoptyping` event to chat or raises nambaone.ClientException
```

#### Message object contains bot field therefore there are handfull shortcuts such as
```python
update.message.reply_text(plain_text)
update.message.reply_typing()
update.message.reply_typing_stop()
```

## Live usage

Live usage case can be found in [Django Echo Bot](https://github.com/erjanmx/django-namba-one-bot)
