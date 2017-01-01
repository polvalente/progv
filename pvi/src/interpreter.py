#Paulo Valente
#Interpreter for the ProgV test language

#The following comments outline what has been taken from the Programming Languages Course at Udacity

#Environment as a tuple: (parent, {string:value}), global == None
#lambda == function
#exception to simulate return

from sys import exit

class ProgvReturn(Exception):
    """"return" raises an Expection, so that we can break out of any statement and return to caller """
    def __init__(self, value):
        self.value = value
class UndefinedVariable(Exception):
    """Assignment to undefined variable"""
    def __init__(self):
        pass

def env_search(name, env):
    #search in current environment
    if name in env[1]:
        return (env[1])[name]
    #if environment is global, the name doesn't exist
    if env[0] == None:
        return None
    
    #if environment is not global, search for the name in its parent
    return env_search(name, env[0])

def env_update(name, value, env):
    if name in env[1]: 
        (env[1])[name] = value
    elif env[0] is not None: 
        env_update(name, value, env[0])
    else:
        #env is global and variable assigned doesn't exist
        raise UndefinedVariable

def eval_element(element, env):
    if element[0] == 'function':
        func_name = element[1]
        func_params = element[2]
        func_body = element[3]
        func_value = ("function",func_params, func_body, env)
        (env[1])[func_name] = func_value
    elif element[0] == 'stmt':
        eval_stmt(element[1], env)
    else:
        print "ERROR: eval_element: unknown element "+element

def eval_stmts(stmts, env):
    map(lambda s: eval_stmt(s, env), stmts)

def eval_stmt(stmt, env):
    stype = stmt[0]
    if stype == "if-then":
        conditional = stmt[1]
        then = stmt[2]
        if eval_exp(conditional, env):
            eval_stmts(then, env)
    elif stype == "while":
        conditional = stmt[1]
        body = stmt[2]
        while eval_exp(conditional,env): eval_stmts(body,env)
    elif stype == "if-then-else":
        conditional = stmt[1]
        then_branch = stmt[2]
        else_branch = stmt[3]
        if eval_exp(conditional,env):
            eval_stmts(then_branch,env)
        else:
            eval_stmts(else_branch,env)
    elif stype == "var":
        name = stmt[1]
        right_exp = stmt[2]
        (env[1])[name] = eval_exp(right_exp,env)
    elif stype == "assign":
        name = stmt[1]
        right_exp = stmt[2]
        env_update(name, eval_exp(right_exp,env), env)
    elif stype == "return":
        value = eval_exp(stmt[1],env)
        raise ProgvReturn(value)
    elif stype == "exp":
        eval_exp(stmt[1],env)
    else:
        print "ERROR: unknown statement type ", stype

def eval_exp(exp, env):
    etype = exp[0]

    if etype == "identifier":
        name = exp[1]
        value = env_search(name, env)
        if value == None:
            print "ERROR: unbound variable " + name
        else:
            return value
    elif etype == "number":
        return float(exp[1])
    elif etype == "string":
        return exp[1]
    elif etype == "true":
        return True
    elif etype == "false":
        return False
    elif etype == "function":
        params = exp[1]
        body = exp[2]
        return ("function", params, body, env)
    elif etype == "binop":
        #a op b
        a = eval_exp(exp[1], env)
        b = eval_exp(exp[3], env)
        op = exp[2]
        if op == "+": return a + b
        elif op == "-": return a - b
        elif op == "/": return a / b
        elif op == "*": return a * b
        elif op == "%": return a % b
        elif op == "==": return a == b
        elif op == "<=": return a <= b
        elif op == "<": return a < b
        elif op == ">=": return a >= b
        elif op == ">": return a > b
        elif op == "&&": return a and b
        elif op == "||": return a or b
        else:
            print "ERROR: unknown binary operation ", op
            exit(1)
    elif etype == "call":
        name = exp[1]
        args = exp[2]
        value = env_search(name, env)
        if name == "print":
            for arg in args:
                print eval_exp(arg,env),
            print
        elif value[0] == "function":
            params = value[1]
            body = value[2]
            env = value[3]
            if len(params) != len(args):
                print "ERROR: wrong number of arguments to " + name
            else:
                #new environment nested in the current one
                newenv = (env, {})
                def assign(arg, param):
                    newenv[1][param] = eval_exp(arg, env)
                map(lambda arg, param: assign(arg,param), args, params)
                try:
                    eval_stmts(body, newenv)
                    return None
                except ProgvReturn as r:
                    return r.value
        else:
            print "ERROR: call to non-function " + name
    else:
        print "ERROR: uknown expression type ", etype
    return None

def env_debug(env):
    print "Environment Debug:"
    for name in env[1]:
        print "env["+name+"] = ", env[1][name]

def interpret(ast):
    global_env = (None, {})
    for element in ast: 
        eval_element(element, global_env)
