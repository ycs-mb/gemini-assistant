#!/usr/bin/env python3
import sys
from dotenv import dotenv_values

def main():
    env_vars = dotenv_values(".env")
    if env_vars:
        # Save API key in a different variable and remove it from env_vars if needed
        api_key = env_vars.get("API_KEY")
        if api_key:
            print(f"API_KEY saved separately: {api_key}")
        else:
            print("API_KEY not found in environment variables.")
        
        # Print the remaining environment variables
        for key, value in env_vars.items():
            print(f"{key}={value}")
    else:
        print("No environment variables found.")

if __name__ == "__main__":
    main()
