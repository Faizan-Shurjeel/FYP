"""
Quick Voice Authentication Test
"""

from voice_auth import VoiceAuthSystem
from colorama import Fore

print(f"{Fore.CYAN}{'='*60}")
print(f"{Fore.CYAN}🚀 QUICK VOICE AUTH TEST")
print(f"{Fore.CYAN}{'='*60}\n")

# Initialize system
system = VoiceAuthSystem(threshold=0.25)

# Get username
username = input(f"{Fore.YELLOW}Enter your name: {Fore.WHITE}")

# Register
print(f"\n{Fore.GREEN}Step 1: Registration")
system.register_user(username, num_samples=2)

# Authenticate
print(f"\n{Fore.GREEN}Step 2: Authentication")
system.authenticate(username)

print(f"\n{Fore. CYAN}✅ Test complete!")