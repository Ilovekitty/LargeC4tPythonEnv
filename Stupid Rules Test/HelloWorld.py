import re

def stupidRulesTxt(s):
    return re.sub(r"[A-Za-z]{3,}",
                  lambda mo: mo.group(0)[0].upper() +
                             mo.group(0)[1:].lower(),
                  s)
#<span>this <b class="stuff" ></b> </span>
def stupidRulesJS(s):
    return re.sub(r"(<div[.*]>)(.*)(</div>)",
            lambda mo: mo.group(0) + 
            stupidRulesTxt(mo.group(1)) 
            + mo.group(2),
            s)

def stupidRulesCS(s):
    return re.sub(r"(ErrorMessage\w*=\w*\")(.*)(\")",
                  lambda mo: mo.group(0) + 
                  stupidRulesTxt(mo.group(1))
                  + mo.group(2),
                  s)

# msg = "hey there i think this is going to be fun and i hope this works like a boss"
# print(msg)

# print()
# print(stupidRules(msg))

# print("hello world")
# print(str.capitalize("hello world"))
# print("hello you're world".title())

# print(stupidRules("heLLO of if you're world"))