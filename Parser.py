#Parser
import json

def parse_json(string, username):
    obj = json.loads(string)
    ret_val = ''
    if obj['response'] == 'error':
        ret_val = '\n'
        ret_val += '*****\tERROR\t*****\n'
        ret_val += obj['sender'] + ': '
        ret_val += obj['content']
        ret_val += '\n'
        return ret_val
    elif obj['response'] == 'message':
        ret_val += '\n'
        ret_val += obj['sender'] + ': '
        ret_val += obj['content']
        ret_val += '\n'
        if obj['sender'] == username:
            return ''
        return ret_val
    elif obj['response'] == 'history':
        #print obj['content'][0]
        ret_val = '\n*******************************'
        ret_val += '\nPreviously on ' + obj['sender'] + "'s server:\n"
        for jobj in obj['content']:
            ret_val += parse_json(jobj, '')
        ret_val += '*******************************\n'
        return ret_val
    elif obj['response'] == 'info':
        ret_val = '\n'
        ret_val += '*****\tINFO\t*****\n'
        ret_val += obj['sender'] + ': '
        ret_val += obj['content']
        ret_val += '\n'
        return ret_val
    else:
        return '\n\nInvalid Response: "' + obj['response'] + '"\n\n'
