from clients import webhook

def alert(msg: str):
    if webhook is not None:
        webhook.send(msg)