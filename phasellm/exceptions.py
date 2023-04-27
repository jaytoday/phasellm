"""
Exception classes and tests for prompts, LLMs, and workflows.
"""

def isAcceptableLLMResponse(response_given, acceptable_options):
    """
    Tests to confirm the response_given is in the list of acceptable_options. acceptable_options can also be a single string.

    Returns True if the response is 'acceptable', otherwise throws an LLMResponseException.
    """
    
    compare_to = None
    if isinstance(acceptable_options, str):
        compare_to = [acceptable_options]
    elif isinstance(acceptable_options, list):
        compare_to = acceptable_options

    if compare_to is None:
        raise Exception("testLLMResponse() only accepts a list or string object for acceptable_options.")

    if response_given not in acceptable_options:
        raise LLMResponseException(response_given, compare_to)

    return True

def isLLMCodeExecutable(llm_code):
    """
    Runs code and checks if any errors occur. Returns True if there are no errors.
    """
    try:
        exec(llm_code)
    except Exception as e:
        raise LLMCodeException(llm_code, e)
    
    return True

class LLMCodeException(Exception):
    """
    Exception to track excpetions with code generated by LLMs.
    """

    def __init__(self, code, exc):
        super().__init__("LLM Code Exception: code is raising an error.") 
        self.code = code 
        self.exception = exc
        self.exception_string = str(exc)

    def __repr__(self):
        return f"LLLM Code Exception: code is raising an error."

class LLMResponseException(Exception):
    """
    Exception to track acceptable responses from an LLM.
    """

    def __init__(self, response_given, acceptable_options):
        super().__init__("LLM Response Exception: response given is not in the list of acceptable options.") 
        self.response_given = response_given
        self.acceptable_options = acceptable_options 

    def __repr__(self):
        return f"LLM Response Exception: response given is not in the list of acceptable options."