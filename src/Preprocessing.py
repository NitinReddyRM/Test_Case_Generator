import re
import pandas as pd
import json
class Precessing:
    def __init__(self):
        pass
    def text_file_preprocessing(self,data):
        lines = data.splitlines()
        test_cases=[]
        current_case=""
        pattern=re.compile(r"^\d+\.\s*")
        for line in lines:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            if pattern.match(line):
                if current_case:
                    test_cases.append(current_case.strip())
                current_case = pattern.sub("", line)  # remove the "1. ", "2. ", etc.
            else:
                current_case += "" + line

        if current_case:
            test_cases.append(current_case.strip())
        return test_cases
    
    @staticmethod
    def extract_json_structure(text):
        # Try to match either a list or an object
        patterns = [
            r"\[\s*{.*?}\s*]",  # Matches a list of JSON objects
            r"{.*?}"            # Matches a single JSON object
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        return None
