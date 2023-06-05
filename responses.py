import random


commands = ["hello", "roll", "help"]

def get_response(message) -> str:
    msg = message.lower()

    if msg == 'hello':
        return 'Hello'
    
    if msg == 'roll':
        return str(random.randint(1, 6))
    
    if msg == 'help':
        return 'Commands: ', commands
    
    if msg.startswith('del') or msg.startswith('delete'):
        return 'Under development'
    
    if msg.startswith('p '):
        p_msg = msg[2:]
        print(p_msg)
    
    return 'Error reading msg. use >help for help'


