#Parser
import json

def parse_json(string):
    obj = json.loads(string)
    ret_val = ''
    if obj['response'] == 'error':
        ret_val = '\n\n'
        ret_val += '*****\tERROR\t*****\n'
        ret_val += obj['sender'] + ': '
        ret_val += obj['content']
        ret_val += '\n\n'
        return ret_val
    elif obj['response'] == 'message':
        ret_val += '\n'
        ret_val += obj['sender'] + ': '
        ret_val += obj['content']
        ret_val += '\n'
        return ret_val
    elif obj['response'] == 'history':
        ret_val = '\n\n'
        for jobj in obj['content']:
            print jobj
            ret_val += parse_json(json.dumps(jobj)) + '\n'
        ret_val += '\n\n'
        return ret_val
    elif obj['response'] == 'info':
        ret_val = '\n\n'
        ret_val += '*****\tINFO\t*****\n'
        ret_val += obj['sender'] + ': '
        ret_val += obj['content']
        ret_val += '\n\n'
        return ret_val
    else:
        return '\n\nInvalid Response: "' + obj['response'] + '"\n\n'
