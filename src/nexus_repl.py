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
        self.setup_completer()

    
    def show_help(self, *args):
        """Display help information about REPL commands"""
        print("\nNexus REPL Commands:")
        print("  help         - Show this help message")
        print("  exit         - Exit the REPL")
        print("  reset        - Reset the environment (clear all variables)")
        print("\nExample Nexus Code:")
        print("  var x = 10;")
        print("  fn add(a, b) { a + b; }")
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
        try:
            command = code.strip()
            if command in self.commands:
                return self.commands[command]()
           
            ast, self.global_scope = parse(code, self.global_scope) # returned scope is ignored
            
            result = e(ast, self.global_scope) # global scope

            return result
        except Exception as err:
            # Handle errors without crashing
            return f"Error: {str(err)}"

    
    def read_multiline_input(self):
        lines = []
        prompt = "nexus> "
        
        while True:
            try:
                line = input(prompt)
                lines.append(line)
                
                # Simple balanced braces check for multiline input
                if "{" in line and not self.is_balanced("".join(lines)):
                    prompt = "... "
                    continue
                
                # Check for semicolon to end statement
                if line.strip().endswith(";"):
                    break
                
                # If single line with no open braces, execute immediately
                if prompt == "nexus> " and "{" not in line:
                    break
                    
            except EOFError:
                print("")
                if not lines:
                    self.exit_repl()
                break
                
        return "\n".join(lines)
    
    def is_balanced(self, text):
        """Check if braces are balanced"""
        stack = []
        for char in text:
            if char == "{":
                stack.append(char)
            elif char == "}":
                if not stack or stack.pop() != "{":
                    return False
        return len(stack) == 0
    
    def run(self):
        print("Nexus Language REPL v0.1")
        print("Type 'help' for assistance or 'exit' to quit")
        
        while True:
            try:
                # Read input (possibly multiline)
                user_input = self.read_multiline_input()
                
                # Skip empty lines
                if not user_input.strip():
                    continue
                
                # Add to history
                readline.add_history(user_input)
                
                # Evaluate and print result
                result = self.evaluate(user_input)
                if result is not None:
                    print(result)
                    
            except KeyboardInterrupt:
                print("\nOperation cancelled")
                continue

if __name__ == "__main__":
    repl = NexusREPL()
    repl.run()
