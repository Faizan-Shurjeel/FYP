"""
Complete Voice Authentication System using SpeechBrain
Author: Created for Faizan-Shurjeel
"""

import os
import json
import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path
from datetime import datetime
from speechbrain.inference.speaker import SpeakerRecognition
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

class VoiceAuthSystem:
    def __init__(self, audio_db_path="audio_db", threshold=0.25):
        """
        Initialize Voice Authentication System
        
        Args: 
            audio_db_path:  Path to store user voice samples
            threshold: Similarity threshold for verification (lower = stricter)
        """
        self.audio_db_path = Path(audio_db_path)
        self.audio_db_path.mkdir(exist_ok=True)
        self.threshold = threshold
        self. sample_rate = 16000
        self.users_file = self.audio_db_path / "users.json"
        
        print(f"{Fore.CYAN}🔊 Initializing Voice Authentication System...")
        print(f"{Fore.YELLOW}📥 Loading pre-trained model (first time will download ~400MB)...")
        
        # Load SpeechBrain pre-trained model
        self.verifier = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="models/spkrec-ecapa-voxceleb"
        )
        
        print(f"{Fore.GREEN}✅ Model loaded successfully!\n")
        
        # Load existing users
        self.users = self._load_users()
    
    def _load_users(self):
        """Load registered users from JSON file"""
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_users(self):
        """Save registered users to JSON file"""
        with open(self.users_file, 'w') as f:
            json. dump(self.users, f, indent=4)
    
    def record_audio(self, duration=3, filename=None):
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            filename: Output filename (optional)
        
        Returns:
            Path to saved audio file
        """
        print(f"{Fore.YELLOW}🎤 Recording for {duration} seconds...")
        print(f"{Fore.CYAN}   Speak clearly into your microphone!")
        
        # Record audio
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32'
        )
        sd.wait()
        
        print(f"{Fore.GREEN}✅ Recording complete!")
        
        # Save to file
        if filename is None:
            filename = f"temp/recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        os.makedirs(os.path. dirname(filename), exist_ok=True)
        sf.write(filename, audio, self.sample_rate)
        
        return filename
    
    def register_user(self, username, num_samples=3):
        """
        Register a new user with multiple voice samples
        
        Args: 
            username: User's name
            num_samples:  Number of voice samples to record (more = better accuracy)
        
        Returns:
            bool: Success status
        """
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}👤 Registering User: {Fore.WHITE}{username}")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        if username in self.users:
            overwrite = input(f"{Fore.YELLOW}⚠️  User '{username}' already exists. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print(f"{Fore.RED}❌ Registration cancelled.")
                return False
        
        user_folder = self.audio_db_path / username
        user_folder. mkdir(exist_ok=True)
        
        audio_files = []
        
        print(f"{Fore.YELLOW}📝 We'll record {num_samples} voice samples for better accuracy.")
        print(f"{Fore.CYAN}💡 Tip:  Speak different sentences each time for best results!\n")
        
        for i in range(num_samples):
            print(f"{Fore.MAGENTA}Sample {i+1}/{num_samples}")
            input(f"{Fore.WHITE}   Press Enter when ready to record...")
            
            audio_file = user_folder / f"sample_{i+1}.wav"
            self.record_audio(duration=3, filename=str(audio_file))
            audio_files.append(str(audio_file))
            print()
        
        # Save user info
        self.users[username] = {
            "audio_files": audio_files,
            "registered_date": datetime.now().isoformat(),
            "num_samples": num_samples
        }
        self._save_users()
        
        print(f"{Fore.GREEN}✅ Successfully registered '{username}'!")
        print(f"{Fore.GREEN}   {num_samples} voice samples saved.\n")
        
        return True
    
    def verify_user(self, username, test_audio=None):
        """
        Verify if the recorded voice matches the registered user
        
        Args:
            username: User to verify against
            test_audio: Path to test audio (if None, will record)
        
        Returns: 
            tuple: (is_verified, similarity_score)
        """
        if username not in self.users:
            print(f"{Fore.RED}❌ User '{username}' not found in database!")
            return False, 0.0
        
        # Record test audio if not provided
        if test_audio is None:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.CYAN}🔐 Verifying Identity:  {Fore.WHITE}{username}")
            print(f"{Fore.CYAN}{'='*60}\n")
            
            input(f"{Fore.WHITE}Press Enter to record your voice for verification...")
            test_audio = self.record_audio(duration=3, filename="temp/verify_temp.wav")
        
        # Compare with all registered samples
        registered_files = self.users[username]["audio_files"]
        scores = []
        
        print(f"\n{Fore.YELLOW}🔍 Analyzing voice patterns...")
        
        for reg_file in registered_files: 
            score, prediction = self.verifier.verify_files(test_audio, reg_file)
            scores.append(score. item())
        
        # Use average score
        avg_score = np.mean(scores)
        is_verified = avg_score > self.threshold
        
        return is_verified, avg_score
    
    def authenticate(self, username):
        """
        Complete authentication flow for a user
        
        Args: 
            username: User to authenticate
        
        Returns: 
            bool: Authentication success
        """
        is_verified, score = self.verify_user(username)
        
        print(f"\n{Fore. CYAN}{'='*60}")
        print(f"{Fore.CYAN}🎯 Authentication Result")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.WHITE}User: {Fore.YELLOW}{username}")
        print(f"{Fore.WHITE}Similarity Score: {Fore.YELLOW}{score:.4f}")
        print(f"{Fore.WHITE}Threshold: {Fore.YELLOW}{self.threshold}")
        
        if is_verified:
            print(f"\n{Fore.GREEN}✅ AUTHENTICATION SUCCESSFUL!")
            print(f"{Fore.GREEN}   Welcome back, {username}!  🎉")
        else:
            print(f"\n{Fore.RED}❌ AUTHENTICATION FAILED!")
            print(f"{Fore. RED}   Voice does not match registered user.")
        
        print(f"{Fore.CYAN}{'='*60}\n")
        
        return is_verified
    
    def list_users(self):
        """List all registered users"""
        if not self.users:
            print(f"{Fore. YELLOW}📭 No users registered yet.")
            return
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore. CYAN}👥 Registered Users")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        for i, (username, info) in enumerate(self.users. items(), 1):
            reg_date = datetime.fromisoformat(info['registered_date']).strftime('%Y-%m-%d %H:%M')
            print(f"{Fore.WHITE}{i}. {Fore. YELLOW}{username}")
            print(f"   📅 Registered: {reg_date}")
            print(f"   🎵 Voice samples: {info['num_samples']}\n")
    
    def delete_user(self, username):
        """Delete a registered user"""
        if username not in self.users:
            print(f"{Fore.RED}❌ User '{username}' not found!")
            return False
        
        # Delete audio files
        user_folder = self.audio_db_path / username
        if user_folder.exists():
            for file in user_folder.glob("*.wav"):
                file.unlink()
            user_folder.rmdir()
        
        # Remove from database
        del self.users[username]
        self._save_users()
        
        print(f"{Fore.GREEN}✅ User '{username}' deleted successfully!")
        return True


def main_menu():
    """Interactive menu for voice authentication system"""
    system = VoiceAuthSystem(threshold=0.25)
    
    while True:
        print(f"\n{Fore. CYAN}{'='*60}")
        print(f"{Fore. CYAN}🎤 VOICE AUTHENTICATION SYSTEM")
        print(f"{Fore. CYAN}{'='*60}\n")
        print(f"{Fore.WHITE}1. 👤 Register New User")
        print(f"{Fore.WHITE}2. 🔐 Authenticate User")
        print(f"{Fore.WHITE}3. 👥 List All Users")
        print(f"{Fore.WHITE}4. 🗑️  Delete User")
        print(f"{Fore.WHITE}5. ⚙️  Change Threshold")
        print(f"{Fore.WHITE}6. 🚪 Exit")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        choice = input(f"{Fore. YELLOW}Select option (1-6): {Fore.WHITE}")
        
        if choice == '1': 
            username = input(f"\n{Fore.CYAN}Enter username to register: {Fore.WHITE}")
            num_samples = input(f"{Fore.CYAN}Number of voice samples (default 3): {Fore.WHITE}") or "3"
            system.register_user(username, int(num_samples))
        
        elif choice == '2': 
            username = input(f"\n{Fore.CYAN}Enter username to authenticate: {Fore. WHITE}")
            system.authenticate(username)
        
        elif choice == '3': 
            system.list_users()
        
        elif choice == '4':
            username = input(f"\n{Fore.CYAN}Enter username to delete: {Fore.WHITE}")
            confirm = input(f"{Fore. RED}Are you sure?  This cannot be undone! (yes/no): {Fore.WHITE}")
            if confirm.lower() == 'yes':
                system.delete_user(username)
        
        elif choice == '5':
            new_threshold = input(f"\n{Fore.CYAN}Enter new threshold (current: {system.threshold}): {Fore.WHITE}")
            try:
                system.threshold = float(new_threshold)
                print(f"{Fore.GREEN}✅ Threshold updated to {system.threshold}")
            except ValueError:
                print(f"{Fore.RED}❌ Invalid threshold value!")
        
        elif choice == '6':
            print(f"\n{Fore.GREEN}👋 Goodbye!")
            break
        
        else:
            print(f"{Fore.RED}❌ Invalid option!  Please select 1-6.")


if __name__ == "__main__": 
    main_menu()