"""
Simple Voice Authentication using Resemblyzer (Python 3.13 compatible)
"""

import os
import json
import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path
from datetime import datetime
from resemblyzer import VoiceEncoder, preprocess_wav
from colorama import init, Fore, Style

init(autoreset=True)

class VoiceAuthSystem:
    def __init__(self, audio_db_path="audio_db", threshold=0.75):
        self.audio_db_path = Path(audio_db_path)
        self.audio_db_path.mkdir(exist_ok=True)
        self.threshold = threshold
        self.sample_rate = 16000
        self.users_file = self.audio_db_path / "users.json"
        
        print(f"{Fore.CYAN}🔊 Initializing Voice Authentication System...")
        self.encoder = VoiceEncoder()
        print(f"{Fore.GREEN}✅ Model loaded successfully!\n")
        
        self.users = self._load_users()
    
    def _load_users(self):
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def record_audio(self, duration=2, filename=None):
        print(f"{Fore.YELLOW}🎤 Recording for {duration} seconds...")
        print(f"{Fore.CYAN}   Speak clearly into your microphone!")
        
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32'
        )
        sd.wait()
        
        print(f"{Fore.GREEN}✅ Recording complete!")
        
        if filename is None:
            filename = f"temp/recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        os.makedirs(os.path. dirname(filename), exist_ok=True)
        sf.write(filename, audio, self.sample_rate)
        
        return filename
    
    def get_embedding(self, audio_path):
        """Extract voice embedding from audio file"""
        wav = preprocess_wav(audio_path)
        embedding = self.encoder.embed_utterance(wav)
        return embedding
    
    def register_user(self, username, num_samples=3):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}👤 Registering User: {Fore.WHITE}{username}")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        if username in self.users:
            overwrite = input(f"{Fore.YELLOW}User '{username}' already exists. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print(f"{Fore.RED}❌ Registration cancelled.")
                return False
        
        user_folder = self.audio_db_path / username
        user_folder. mkdir(exist_ok=True)
        
        audio_files = []
        embeddings = []
        
        print(f"{Fore.YELLOW}📝 We'll record {num_samples} voice samples for better accuracy.\n")
        
        for i in range(num_samples):
            print(f"{Fore.MAGENTA}Sample {i+1}/{num_samples}")
            input(f"{Fore.WHITE}   Press Enter when ready to record...")
            
            audio_file = user_folder / f"sample_{i+1}.wav"
            self.record_audio(duration=2, filename=str(audio_file))
            
            # Get embedding
            embedding = self. get_embedding(str(audio_file))
            embeddings.append(embedding. tolist())
            audio_files.append(str(audio_file))
            print()
        
        # Save user info with embeddings
        self.users[username] = {
            "audio_files": audio_files,
            "embeddings": embeddings,
            "registered_date": datetime.now().isoformat(),
            "num_samples": num_samples
        }
        self._save_users()
        
        print(f"{Fore. GREEN}✅ Successfully registered '{username}'!\n")
        return True
    
    def verify_user(self, username, test_audio=None):
        if username not in self.users:
            print(f"{Fore.RED}❌ User '{username}' not found!")
            return False, 0.0
        
        if test_audio is None:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.CYAN}🔐 Verifying Identity: {Fore.WHITE}{username}")
            print(f"{Fore. CYAN}{'='*60}\n")
            
            input(f"{Fore.WHITE}Press Enter to record your voice...")
            test_audio = self.record_audio(duration=2, filename="temp/verify_temp.wav")
        
        print(f"\n{Fore.YELLOW}🔍 Analyzing voice patterns...")
        
        # Get test embedding
        test_embedding = self.get_embedding(test_audio)
        
        # Compare with stored embeddings
        stored_embeddings = [np.array(e) for e in self.users[username]["embeddings"]]
        similarities = [np.dot(test_embedding, stored_emb) for stored_emb in stored_embeddings]
        
        avg_similarity = np.mean(similarities)
        is_verified = avg_similarity > self.threshold
        
        return is_verified, avg_similarity
    
    def authenticate(self, username):
        is_verified, score = self.verify_user(username)
        
        print(f"\n{Fore. CYAN}{'='*60}")
        print(f"{Fore.CYAN}🎯 Authentication Result")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.WHITE}User: {Fore.YELLOW}{username}")
        print(f"{Fore.WHITE}Similarity Score: {Fore.YELLOW}{score:.4f}")
        print(f"{Fore.WHITE}Threshold: {Fore.YELLOW}{self.threshold}")
        
        if is_verified:
            print(f"\n{Fore.GREEN}✅ AUTHENTICATION SUCCESSFUL!")
            print(f"{Fore. GREEN}   Welcome back, {username}!  🎉")
        else:
            print(f"\n{Fore.RED}❌ AUTHENTICATION FAILED!")
            print(f"{Fore.RED}   Voice does not match.")
        
        print(f"{Fore.CYAN}{'='*60}\n")
        return is_verified
    
    def list_users(self):
        if not self.users:
            print(f"{Fore. YELLOW}📭 No users registered yet.")
            return
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}👥 Registered Users")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        for i, (username, info) in enumerate(self.users.items(), 1):
            reg_date = datetime.fromisoformat(info['registered_date']).strftime('%Y-%m-%d %H:%M')
            print(f"{Fore.WHITE}{i}. {Fore. YELLOW}{username}")
            print(f"   📅 Registered: {reg_date}")
            print(f"   🎵 Voice samples:  {info['num_samples']}\n")


def main_menu():
    system = VoiceAuthSystem(threshold=0.75)
    
    while True: 
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🎤 VOICE AUTHENTICATION SYSTEM")
        print(f"{Fore.CYAN}{'='*60}\n")
        print(f"{Fore.WHITE}1. 👤 Register New User")
        print(f"{Fore.WHITE}2. 🔐 Authenticate User")
        print(f"{Fore.WHITE}3. 👥 List All Users")
        print(f"{Fore.WHITE}4. 🚪 Exit")
        print(f"{Fore. CYAN}{'='*60}\n")
        
        choice = input(f"{Fore.YELLOW}Select option (1-4): {Fore.WHITE}")
        
        if choice == '1': 
            username = input(f"\n{Fore.CYAN}Enter username: {Fore.WHITE}")
            system.register_user(username, num_samples=2)
        
        elif choice == '2':
            username = input(f"\n{Fore. CYAN}Enter username: {Fore.WHITE}")
            system. authenticate(username)
        
        elif choice == '3':
            system.list_users()
        
        elif choice == '4': 
            print(f"\n{Fore.GREEN}👋 Goodbye!")
            break


if __name__ == "__main__":
    main_menu()
