#Parser
import json

def parse_json(string, user):
    obj = json.loads(string)
    ret_val = ''
    if obj['response'] == 'error':
        ret_val = '\n'
        ret_val += '*****\tERROR\t*****\n'
        ret_val += obj['sender'] + ': '
        ret_val += obj['content']
        ret_val += '\n'
        return ret_val
    elif (obj['response'] == 'message') and (user != obj['sender']):
        ret_val += obj['sender'] + ': '
        ret_val += obj['content']
        return ret_val
    elif obj['response'] == 'history':
        ret_val = '\n'
        for jobj in obj['content']:
            ret_val += parse_json(jobj)
        ret_val += '\n'
        return ret_val
    elif obj['response'] == 'info':
        ret_val = '\n'
        ret_val += '*****\tINFO\t*****\n'
        ret_val += obj['sender'] + ': '
        ret_val += obj['content']
        ret_val += '\n'
        return ret_val
    else:
        return '\nInvalid Response: "' + obj['response'] + '"\n'
