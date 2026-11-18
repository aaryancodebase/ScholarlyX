import re
TOKEN_RE = re.compile(r"\(|\)|\bAND\b|\bOR\b|\bNOT\b|[^\s()]+", re.I)
PRECEDENCE = {"OR": 1, "AND": 2, "NOT": 3}

def _to_rpn(query):
    tokens = TOKEN_RE.findall(query); output=[]; stack=[]; expect_operand=True
    for raw in tokens:
        token=raw.upper()
        if token=="(": stack.append(token); expect_operand=True
        elif token==")":
            while stack and stack[-1]!="(": output.append(stack.pop())
            if not stack: raise ValueError("Mismatched parentheses.")
            stack.pop(); expect_operand=False
        elif token in PRECEDENCE:
            if token in ("AND","OR") and expect_operand: raise ValueError(f"Unexpected operator {token}.")
            while stack and stack[-1] in PRECEDENCE and (PRECEDENCE[stack[-1]]>PRECEDENCE[token] or (PRECEDENCE[stack[-1]]==PRECEDENCE[token] and token!="NOT")):
                output.append(stack.pop())
            stack.append(token); expect_operand=True
        else: output.append(raw.casefold()); expect_operand=False
    while stack:
        op=stack.pop()
        if op=="(": raise ValueError("Mismatched parentheses.")
        output.append(op)
    return output

def boolean_search(query, documents):
    postings={}
    for i,doc in enumerate(documents):
        for term in set(doc.split()): postings.setdefault(term,set()).add(i)
    universe=set(range(len(documents))); stack=[]
    for token in _to_rpn(query):
        if token=="NOT":
            if not stack: raise ValueError("NOT needs a term.")
            stack.append(universe-stack.pop())
        elif token in ("AND","OR"):
            if len(stack)<2: raise ValueError(f"{token} needs two operands.")
            right,left=stack.pop(),stack.pop()
            stack.append(left & right if token=="AND" else left | right)
        else: stack.append(postings.get(token,set()))
    if len(stack)!=1: raise ValueError("Invalid Boolean expression. Use terms with AND, OR, NOT and parentheses.")
    return sorted(stack[0])

def normalize_boolean_query(query, preprocessor):
    parts = TOKEN_RE.findall(query)
    normalized = []
    for part in parts:
        upper = part.upper()
        if upper in PRECEDENCE or part in ("(", ")"):
            normalized.append(upper if upper in PRECEDENCE else part)
        else:
            normalized.append(preprocessor.process(part) or part.casefold())
    return " ".join(normalized)
