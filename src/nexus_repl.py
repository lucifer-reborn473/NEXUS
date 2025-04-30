#!/usr/bin/env python3
import sys
import traceback
import readline
import os
from lexer import lex
from parser import parse, VarBind
from evaluator import e
from scope import SymbolTable

class NexusREPL:
    def __init__(self):
        self.global_scope = SymbolTable()
        
        # Set up readline for history
        self.history_file = os.path.expanduser("~/.nexus_history")
        try:
            readline.read_history_file(self.history_file)
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
        
        # Define built-in commands
        self.commands = {
            "help": self.show_help,
            "exit": self.exit_repl,
            "reset": self.reset_environment
        }
        
        # Initialize tab completion
        self.setup_completer()
    
    def show_help(self, *args):
        """Display help information about REPL commands"""
        print("\nNexus REPL Commands:")
        print("  help         - Show this help message")
        print("  exit         - Exit the REPL")
        print("  reset        - Reset the environment (clear all variables)")
        print("\nExample Nexus Code:")
        print("  var x = 10;")
        print("  fn add(a, b) { a + b; };")
        print("  displayl add(5, 7);")
        return None
    
    def exit_repl(self, *args):
        """Exit the REPL"""
        print("Exiting Nexus REPL")
        readline.write_history_file(self.history_file)
        sys.exit(0)
    
    def reset_environment(self, *args):
        """Reset the environment"""
        self.global_scope = SymbolTable()
        print("Environment reset - all variables and functions cleared")
        return None
    
    def setup_completer(self):
        keywords = ["var", "fixed", "fn", "if", "else", "while", "for", "displayl", "display"]
        
        def completer(text, state):
            options = [i for i in keywords if i.startswith(text)]
            options.extend([i for i in self.global_scope.table.keys() if i.startswith(text)])
            if state < len(options):
                return options[state]
            return None
        
        readline.set_completer(completer)
        
        # Check which readline variant is being used and bind appropriately
        if 'libedit' in readline.__doc__:
            # macOS uses libedit
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            # GNU readline
            readline.parse_and_bind("tab: complete")
    
    def evaluate(self, code):
        """Evaluate a piece of Nexus code"""
        try:
            # Check for built-in commands first
            command = code.strip()
            if command in self.commands:
                return self.commands[command]()
            
            # Check for obviously incomplete input before parsing
            if not self.is_balanced(code):
                return None  # Signal incomplete input
            
            # If the code appears complete with balanced braces and ends properly
            if self.is_balanced(code) and code.strip().endswith((";", "}")):
                try:
                    # Attempt to parse and evaluate
                    ast, self.global_scope = parse(code, self.global_scope)
                    result = e(ast, self.global_scope)
                    # Success - make sure we return a non-None value to reset prompt
                    return result if result is not None else ""
                except Exception as err:
                    # Only treat certain errors as incomplete input
                    err_msg = str(err).lower()
                    if any(pattern in err_msg for pattern in [
                        "unexpected end", "expected", "rightbracetoken",
                        "got none", "eof", "brace"
                    ]):
                        return None
                    raise  # Re-raise other errors
            
            # Try normal parsing for other cases
            ast, self.global_scope = parse(code, self.global_scope)
            result = e(ast, self.global_scope)
            return result
                
        except Exception as err:
            # Check for incomplete input errors
            err_msg = str(err)
            lower_err = err_msg.lower()
            
            # Catch various incomplete input patterns
            if any(pattern in lower_err for pattern in [
                "unexpected end", "expected", "rightbracetoken", 
                "got none", "eof", "brace"
            ]):
                return None  # Signal incomplete input
                
            # Regular error handling
            return f"Error: {err_msg}"
    
    def is_balanced(self, text):
        """Check if braces are balanced in the input text"""
        stack = []
        for char in text:
            if char == "{":
                stack.append(char)
            elif char == "}":
                if not stack or stack.pop() != "{":
                    return False
        return len(stack) == 0
    
    def run(self):
        """Run the Nexus REPL"""
        print("Nexus Language REPL v0.1")
        print("Type 'help' for assistance or 'exit' to quit")
        
        current_input = []
        prompt = "nexus> "
        
        while True:
            try:
                # Get user input
                line = input(prompt)
                
                # Skip empty lines at the beginning
                if not line.strip() and not current_input:
                    continue
                
                # Empty line with semicolon/brace at end of previous input might signal completion
                if not line.strip() and current_input and current_input[-1].strip().endswith((";", "}")):
                    full_code = "\n".join(current_input)
                    if self.is_balanced(full_code):
                        # Force evaluation of potentially complete input
                        try:
                            ast, self.global_scope = parse(full_code, self.global_scope)
                            result = e(ast, self.global_scope)
                            current_input = []
                            prompt = "nexus> "
                            if result is not None:
                                print(result)
                            continue
                        except:
                            # If it fails, just add the empty line and continue
                            pass
                
                # Add to current input buffer
                current_input.append(line)
                full_code = "\n".join(current_input)
                
                # Try to evaluate
                result = self.evaluate(full_code)
                
                if result is None:
                    # Incomplete input detected
                    prompt = "... "
                else:
                    # Add completed input to history
                    if full_code.strip():
                        readline.add_history(full_code)
                    
                    # Reset for new input
                    current_input = []
                    prompt = "nexus> "
                    
                    # Print result if not None
                    if result is not None and result != "":
                        print(result)
                
            except EOFError:
                print("\nExiting Nexus REPL")
                break
                
            except KeyboardInterrupt:
                print("\nOperation cancelled")
                current_input = []
                prompt = "nexus> "

if __name__ == "__main__":
    repl = NexusREPL()
    repl.run()
