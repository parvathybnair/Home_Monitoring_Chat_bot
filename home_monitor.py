"""
Home Monitoring Chatbot - Backend Logic
Provides AI-powered responses for home status queries
Includes Alexa-style smart home command execution
"""

import os
import sys
import re
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def safe_print(msg):
    """Print safely on Windows consoles that can't handle emojis"""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', errors='replace').decode('ascii'))

# Get environment variables
api_key = os.getenv("API_KEY", "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")
invoke_url = os.getenv("API_BASE_URL", "https://integrate.api.nvidia.com/v1/chat/completions")
model = os.getenv("MODEL", "google/gemma-4-31b-it")
temperature = float(os.getenv("TEMPERATURE", 1.00))
max_tokens = int(os.getenv("MAX_TOKENS", 256))

if not api_key:
    print("ERROR: API_KEY not found in .env file!")
    sys.exit(1)

# Home state simulation (in real scenario, this would connect to IoT devices)
home_state = {
    "doors": {
        "front": "closed",
        "back": "open",
        "garage": "closed"
    },
    "door_locks": {
        "front": "locked",
        "back": "unlocked",
        "garage": "locked"
    },
    "windows": {
        "living_room": "closed",
        "kitchen": "open",
        "bedroom": "closed"
    },
    "temperature": 25,
    "humidity": 45,
    "motion": False,
    "lights": {
        "living_room": "on",
        "kitchen": "off",
        "bedroom": "off"
    },
    "fans": {
        "living_room": "off",
        "kitchen": "off",
        "bedroom": "on"
    }
}


def get_home_status():
    """Generate formatted home status report"""
    status_report = f"""
=== HOME STATUS REPORT ===
Doors: {home_state['doors']}
Door Locks: {home_state['door_locks']}
Windows: {home_state['windows']}
Temperature: {home_state['temperature']}°C
Humidity: {home_state['humidity']}%
Motion detected: {home_state['motion']}
Lights: {home_state['lights']}
Fans: {home_state['fans']}
"""
    return status_report


def update_home_state(key, value):
    """Update home state (for simulating sensor changes)"""
    keys_to_update = key.split(".")
    current = home_state
    
    for k in keys_to_update[:-1]:
        if k in current:
            current = current[k]
    
    if keys_to_update[-1] in current:
        current[keys_to_update[-1]] = value
        
        # Auto-sync: when a door opens, unlock it. When it closes, lock it.
        if keys_to_update[0] == "doors":
            door_name = keys_to_update[-1]
            if door_name in home_state["door_locks"]:
                if value == "open":
                    home_state["door_locks"][door_name] = "unlocked"
                elif value == "closed":
                    home_state["door_locks"][door_name] = "locked"
        
        return True
    return False


# ============ ALEXA COMMAND SYSTEM ============

def parse_smart_commands(user_input):
    """
    Parse user input for smart home control commands.
    Only triggers for explicit action commands, NOT for questions/queries.
    Returns a list of commands to execute via Alexa.
    Each command: {'device': str, 'action': str, 'key': str, 'value': str, 'alexa_cmd': str}
    """
    user_lower = user_input.lower().strip()
    commands = []

    # --- QUESTION DETECTION ---
    # If the user is asking a question, do NOT parse for commands.
    # Let the AI handle it instead.
    question_starters = [
        "is ", "are ", "what ", "what's ", "whats ",
        "how ", "which ", "where ", "when ", "why ",
        "do ", "does ", "did ", "can ", "could ",
        "tell ", "show ", "check ", "status",
        "any ", "has ", "have ",
    ]
    is_question = (
        user_lower.endswith("?")
        or any(user_lower.startswith(q) for q in question_starters)
    )
    
    if is_question:
        return []  # No commands — let AI answer the question

    # --- ROOM NAMES ---
    rooms = {
        "living_room": ["living room", "living", "hall"],
        "kitchen": ["kitchen"],
        "bedroom": ["bedroom", "bed room"],
    }

    def find_rooms(text):
        """Find which rooms are mentioned in the text"""
        found = []
        for room_key, aliases in rooms.items():
            for alias in aliases:
                if alias in text:
                    found.append(room_key)
                    break
        return found

    # Check if "all" is mentioned
    is_all = "all" in user_lower

    # --- DOOR COMMANDS ---
    if any(word in user_lower for word in ["door", "doors"]):
        door_names = {
            "front": ["front door", "front"],
            "back": ["back door", "back", "rear door", "rear"],
            "garage": ["garage door", "garage"],
        }

        if any(word in user_lower for word in ["close", "shut"]):
            if is_all or ("doors" in user_lower and not any(d in user_lower for d_list in door_names.values() for d in d_list)):
                # Close all doors
                for door in ["front", "back", "garage"]:
                    commands.append({
                        "device": f"{door} door",
                        "action": "close",
                        "key": f"doors.{door}",
                        "value": "closed",
                        "alexa_cmd": f"Alexa, close the {door} door"
                    })
            else:
                for door, aliases in door_names.items():
                    if any(a in user_lower for a in aliases):
                        commands.append({
                            "device": f"{door} door",
                            "action": "close",
                            "key": f"doors.{door}",
                            "value": "closed",
                            "alexa_cmd": f"Alexa, close the {door} door"
                        })

        elif any(word in user_lower for word in ["open"]):
            if is_all or ("doors" in user_lower and not any(d in user_lower for d_list in door_names.values() for d in d_list)):
                for door in ["front", "back", "garage"]:
                    commands.append({
                        "device": f"{door} door",
                        "action": "open",
                        "key": f"doors.{door}",
                        "value": "open",
                        "alexa_cmd": f"Alexa, open the {door} door"
                    })
            else:
                for door, aliases in door_names.items():
                    if any(a in user_lower for a in aliases):
                        commands.append({
                            "device": f"{door} door",
                            "action": "open",
                            "key": f"doors.{door}",
                            "value": "open",
                            "alexa_cmd": f"Alexa, open the {door} door"
                        })

        # Lock/Unlock
        if any(word in user_lower for word in ["lock"]):
            is_unlock = "unlock" in user_lower
            lock_val = "unlocked" if is_unlock else "locked"
            lock_action = "unlock" if is_unlock else "lock"

            if is_all or ("doors" in user_lower and not any(d in user_lower for d_list in door_names.values() for d in d_list)):
                for door in ["front", "back", "garage"]:
                    commands.append({
                        "device": f"{door} door lock",
                        "action": lock_action,
                        "key": f"door_locks.{door}",
                        "value": lock_val,
                        "alexa_cmd": f"Alexa, {lock_action} the {door} door"
                    })
            else:
                for door, aliases in door_names.items():
                    if any(a in user_lower for a in aliases):
                        commands.append({
                            "device": f"{door} door lock",
                            "action": lock_action,
                            "key": f"door_locks.{door}",
                            "value": lock_val,
                            "alexa_cmd": f"Alexa, {lock_action} the {door} door"
                        })

    # --- WINDOW COMMANDS ---
    if any(word in user_lower for word in ["window", "windows"]):
        target_rooms = find_rooms(user_lower)

        if any(word in user_lower for word in ["close", "shut"]):
            if is_all or (not target_rooms):
                for room in ["living_room", "kitchen", "bedroom"]:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} window",
                        "action": "close",
                        "key": f"windows.{room}",
                        "value": "closed",
                        "alexa_cmd": f"Alexa, close the {room.replace('_', ' ')} window"
                    })
            else:
                for room in target_rooms:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} window",
                        "action": "close",
                        "key": f"windows.{room}",
                        "value": "closed",
                        "alexa_cmd": f"Alexa, close the {room.replace('_', ' ')} window"
                    })

        elif any(word in user_lower for word in ["open"]):
            if is_all or (not target_rooms):
                for room in ["living_room", "kitchen", "bedroom"]:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} window",
                        "action": "open",
                        "key": f"windows.{room}",
                        "value": "open",
                        "alexa_cmd": f"Alexa, open the {room.replace('_', ' ')} window"
                    })
            else:
                for room in target_rooms:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} window",
                        "action": "open",
                        "key": f"windows.{room}",
                        "value": "open",
                        "alexa_cmd": f"Alexa, open the {room.replace('_', ' ')} window"
                    })

    # --- LIGHT COMMANDS ---
    if any(word in user_lower for word in ["light", "lights"]):
        target_rooms = find_rooms(user_lower)

        if any(word in user_lower for word in ["turn on", "switch on", "on"]):
            if is_all or (not target_rooms):
                for room in ["living_room", "kitchen", "bedroom"]:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} light",
                        "action": "turn on",
                        "key": f"lights.{room}",
                        "value": "on",
                        "alexa_cmd": f"Alexa, turn on the {room.replace('_', ' ')} light"
                    })
            else:
                for room in target_rooms:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} light",
                        "action": "turn on",
                        "key": f"lights.{room}",
                        "value": "on",
                        "alexa_cmd": f"Alexa, turn on the {room.replace('_', ' ')} light"
                    })

        elif any(word in user_lower for word in ["turn off", "switch off", "off"]):
            if is_all or (not target_rooms):
                for room in ["living_room", "kitchen", "bedroom"]:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} light",
                        "action": "turn off",
                        "key": f"lights.{room}",
                        "value": "off",
                        "alexa_cmd": f"Alexa, turn off the {room.replace('_', ' ')} light"
                    })
            else:
                for room in target_rooms:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} light",
                        "action": "turn off",
                        "key": f"lights.{room}",
                        "value": "off",
                        "alexa_cmd": f"Alexa, turn off the {room.replace('_', ' ')} light"
                    })

    # --- FAN COMMANDS ---
    if any(word in user_lower for word in ["fan", "fans"]):
        target_rooms = find_rooms(user_lower)

        if any(word in user_lower for word in ["turn on", "switch on", "on"]):
            if is_all or (not target_rooms):
                for room in ["living_room", "kitchen", "bedroom"]:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} fan",
                        "action": "turn on",
                        "key": f"fans.{room}",
                        "value": "on",
                        "alexa_cmd": f"Alexa, turn on the {room.replace('_', ' ')} fan"
                    })
            else:
                for room in target_rooms:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} fan",
                        "action": "turn on",
                        "key": f"fans.{room}",
                        "value": "on",
                        "alexa_cmd": f"Alexa, turn on the {room.replace('_', ' ')} fan"
                    })

        elif any(word in user_lower for word in ["turn off", "switch off", "off"]):
            if is_all or (not target_rooms):
                for room in ["living_room", "kitchen", "bedroom"]:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} fan",
                        "action": "turn off",
                        "key": f"fans.{room}",
                        "value": "off",
                        "alexa_cmd": f"Alexa, turn off the {room.replace('_', ' ')} fan"
                    })
            else:
                for room in target_rooms:
                    commands.append({
                        "device": f"{room.replace('_', ' ')} fan",
                        "action": "turn off",
                        "key": f"fans.{room}",
                        "value": "off",
                        "alexa_cmd": f"Alexa, turn off the {room.replace('_', ' ')} fan"
                    })

    return commands


def execute_alexa_commands(commands):
    """
    Execute smart home commands via Alexa integration.
    In a real setup, this would call the Alexa Smart Home API.
    Currently simulates by updating the local home state.
    
    Returns a list of executed command results.
    """
    results = []
    
    for cmd in commands:
        # Validation: can't lock a door that is open
        if cmd["key"].startswith("door_locks.") and cmd["value"] == "locked":
            door_name = cmd["key"].split(".")[-1]
            if home_state["doors"].get(door_name) == "open":
                results.append({
                    "device": cmd["device"],
                    "action": cmd["action"],
                    "alexa_cmd": cmd["alexa_cmd"],
                    "success": False,
                    "status": "❌ Door is open",
                    "blocked_reason": f"Please close the {door_name} door first before locking it."
                })
                safe_print(f"[ALEXA] Cannot lock {door_name} door - it's still open!")
                continue
        
        success = update_home_state(cmd["key"], cmd["value"])
        results.append({
            "device": cmd["device"],
            "action": cmd["action"],
            "alexa_cmd": cmd["alexa_cmd"],
            "success": success,
            "status": "✅ Done" if success else "❌ Failed"
        })
        if success:
            safe_print(f"[ALEXA] {cmd['alexa_cmd']}")
        else:
            safe_print(f"[ALEXA] Failed: {cmd['alexa_cmd']}")
    
    return results


# ============ INSTANT LOCAL ANSWERS ============

def try_local_answer(user_input):
    """
    Try to answer common home status questions instantly without calling the AI API.
    Returns a response string if matched, or None to fall back to AI.
    """
    q = user_input.lower().strip().rstrip("?").strip()
    
    # --- DOOR STATUS ---
    if "door" in q:
        if "back" in q:
            status = home_state["doors"]["back"]
            lock = home_state["door_locks"]["back"]
            return f"The back door is currently {status} and {lock}."
        elif "front" in q:
            status = home_state["doors"]["front"]
            lock = home_state["door_locks"]["front"]
            return f"The front door is currently {status} and {lock}."
        elif "garage" in q:
            status = home_state["doors"]["garage"]
            lock = home_state["door_locks"]["garage"]
            return f"The garage door is currently {status} and {lock}."
        else:
            # All doors
            parts = []
            for door in ["front", "back", "garage"]:
                s = home_state["doors"][door]
                l = home_state["door_locks"][door]
                parts.append(f"{door} door is {s} and {l}")
            return f"Here's the door status: {', '.join(parts)}."
    
    # --- LOCK STATUS ---
    if "lock" in q:
        if "back" in q:
            return f"The back door is {home_state['door_locks']['back']}."
        elif "front" in q:
            return f"The front door is {home_state['door_locks']['front']}."
        elif "garage" in q:
            return f"The garage door is {home_state['door_locks']['garage']}."
        else:
            parts = [f"{d}: {v}" for d, v in home_state["door_locks"].items()]
            return f"Door lock status: {', '.join(parts)}."
    
    # --- WINDOW STATUS ---
    if "window" in q:
        if "kitchen" in q:
            return f"The kitchen window is currently {home_state['windows']['kitchen']}."
        elif "bedroom" in q:
            return f"The bedroom window is currently {home_state['windows']['bedroom']}."
        elif "living" in q or "hall" in q:
            return f"The living room window is currently {home_state['windows']['living_room']}."
        else:
            parts = [f"{k.replace('_', ' ')}: {v}" for k, v in home_state["windows"].items()]
            return f"Window status: {', '.join(parts)}."
    
    # --- LIGHT STATUS ---
    if "light" in q:
        if "kitchen" in q:
            return f"The kitchen light is {home_state['lights']['kitchen']}."
        elif "bedroom" in q:
            return f"The bedroom light is {home_state['lights']['bedroom']}."
        elif "living" in q or "hall" in q:
            return f"The living room light is {home_state['lights']['living_room']}."
        else:
            parts = [f"{k.replace('_', ' ')}: {v}" for k, v in home_state["lights"].items()]
            return f"Light status: {', '.join(parts)}."
    
    # --- FAN STATUS ---
    if "fan" in q:
        if "kitchen" in q:
            return f"The kitchen fan is {home_state['fans']['kitchen']}."
        elif "bedroom" in q:
            return f"The bedroom fan is {home_state['fans']['bedroom']}."
        elif "living" in q or "hall" in q:
            return f"The living room fan is {home_state['fans']['living_room']}."
        else:
            parts = [f"{k.replace('_', ' ')}: {v}" for k, v in home_state["fans"].items()]
            return f"Fan status: {', '.join(parts)}."
    
    # --- TEMPERATURE ---
    if "temperature" in q or "temp" in q or "hot" in q or "cold" in q:
        return f"The current temperature is {home_state['temperature']}°C."
    
    # --- HUMIDITY ---
    if "humidity" in q or "humid" in q:
        return f"The current humidity level is {home_state['humidity']}%."
    
    # --- MOTION ---
    if "motion" in q or "movement" in q or "someone" in q or "intruder" in q:
        detected = home_state["motion"]
        if detected:
            return "⚠️ Motion has been detected! Please check your security cameras."
        else:
            return "No motion detected. Everything looks calm."
    
    # --- FULL STATUS ---
    if "status" in q or "everything" in q or "full" in q or "all" in q or "home" in q or "house" in q:
        open_doors = [d for d, v in home_state["doors"].items() if v == "open"]
        unlocked = [d for d, v in home_state["door_locks"].items() if v == "unlocked"]
        open_windows = [w.replace("_", " ") for w, v in home_state["windows"].items() if v == "open"]
        lights_on = [l.replace("_", " ") for l, v in home_state["lights"].items() if v == "on"]
        fans_on = [f.replace("_", " ") for f, v in home_state["fans"].items() if v == "on"]
        
        parts = []
        parts.append(f"🌡️ Temperature: {home_state['temperature']}°C, Humidity: {home_state['humidity']}%.")
        if open_doors:
            parts.append(f"⚠️ Open doors: {', '.join(open_doors)}.")
        else:
            parts.append("✅ All doors are closed.")
        if unlocked:
            parts.append(f"🔓 Unlocked: {', '.join(unlocked)}.")
        if open_windows:
            parts.append(f"🪟 Open windows: {', '.join(open_windows)}.")
        else:
            parts.append("✅ All windows closed.")
        if lights_on:
            parts.append(f"💡 Lights on: {', '.join(lights_on)}.")
        if fans_on:
            parts.append(f"🌀 Fans on: {', '.join(fans_on)}.")
        parts.append(f"📡 Motion: {'Yes ⚠️' if home_state['motion'] else 'No'}.")
        return " ".join(parts)
    
    # ============ BASIC CONVERSATION / SMALL TALK ============

    # --- GREETINGS ---
    if any(w in q for w in ["hi", "hello", "hey", "good morning", "good evening", "good afternoon", "good night", "howdy", "hola", "sup", "yo", "hii", "hiii", "namaste"]):
        import random
        greetings = [
            "Hello! 👋 I'm HomeGuardAI, your smart home security assistant. Ask me about your home or control your devices!",
            "Hey there! 😊 HomeGuardAI at your service. How can I help with your home today?",
            "Hi! 👋 I'm HomeGuardAI — here to manage and protect your smart home. What can I do for you?",
            "Hello! Welcome back! 🛡️ HomeGuardAI is online. Need to check on anything?",
            "Hey! 😄 HomeGuardAI is ready. What do you need?",
        ]
        return random.choice(greetings)

    # --- FAREWELLS ---
    if any(w in q for w in ["bye", "goodbye", "see you", "see ya", "good night", "gotta go", "take care", "later", "cya"]):
        import random
        farewells = [
            "Goodbye! 👋 Stay safe, I'll keep watching over your home!",
            "See you later! 🏠 Your home is in good hands.",
            "Take care! I'll keep everything secure while you're away. 🔒",
            "Bye! 😊 Don't worry, I'll keep an eye on things!",
        ]
        return random.choice(farewells)

    # --- THANK YOU ---
    if any(w in q for w in ["thank", "thanks", "thx", "appreciate", "grateful", "tysm"]):
        import random
        thanks = [
            "You're welcome! 😊 Happy to help!",
            "Anytime! That's what I'm here for! 👍",
            "No problem at all! Let me know if you need anything else. 🏠",
            "Glad I could help! 😄",
            "My pleasure! Feel free to ask anything anytime!",
        ]
        return random.choice(thanks)

    # --- IDENTITY / WHO ARE YOU ---
    if any(phrase in q for phrase in ["who are you", "what are you", "what is your name", "your name", "whats your name", "what's your name", "introduce yourself", "tell me about yourself"]):
        return "I'm HomeGuardAI! 🛡️ Your intelligent home security assistant. I'm connected to your home's IoT devices and Alexa. I can monitor doors, windows, lights, fans, temperature, humidity, and motion sensors. I can also control your devices — just tell me what to do!"

    # --- HOW ARE YOU / FEELINGS ---
    if any(phrase in q for phrase in ["how are you", "how r u", "how do you do", "how are u", "how you doing", "how's it going", "hows it going", "you good", "are you okay", "you okay"]):
        import random
        feelings = [
            "I'm doing great, thanks for asking! 😊 Your home systems are all running smoothly. How can I help you?",
            "I'm wonderful! All sensors are active and I'm ready to assist! 🏠",
            "Doing well! 👍 Just keeping an eye on your home. What do you need?",
            "I'm excellent! Everything's under control here. What can I do for you? 😄",
        ]
        return random.choice(feelings)

    # --- WHAT CAN YOU DO / HELP ---
    if any(phrase in q for phrase in ["what can you do", "help me", "what do you do", "your features", "your capabilities", "how to use", "what should i ask", "what commands", "how does this work"]):
        return ("Here's what HomeGuardAI can do for you! 🛡️\n\n"
                "📊 **Check Status**: Ask about doors, windows, lights, fans, temperature, humidity, or motion\n"
                "🔧 **Control Devices**: Tell me to turn on/off lights or fans, open/close doors or windows, lock/unlock doors\n"
                "📋 **Full Report**: Say 'status' or 'how is my home' for a complete overview\n"
                "💬 **Chat**: I can have a friendly conversation too!\n\n"
                "Try saying: 'Turn on the bedroom light' or 'Is the front door locked?'")

    # --- JOKES ---
    if any(phrase in q for phrase in ["joke", "funny", "make me laugh", "tell me something funny", "humor"]):
        import random
        jokes = [
            "Why did the smart home break up with the dumb home? Because it couldn't handle the lack of connection! 😂🏠",
            "What did the light bulb say to the switch? 'You turn me on!' 💡😄",
            "Why was the thermostat so good at its job? Because it always kept its cool! 🌡️😂",
            "My door sensor told me a joke, but it was too open-ended. 🚪😄",
            "Why don't smart homes ever get lonely? Because they're always connected! 📡😂",
        ]
        return random.choice(jokes)

    # --- COMPLIMENTS ---
    if any(phrase in q for phrase in ["you are great", "you're great", "good job", "well done", "awesome", "amazing", "you rock", "love you", "you're the best", "nice work", "brilliant", "smart"]):
        import random
        compliments = [
            "Aww, thank you! 😊 You're pretty awesome yourself!",
            "That means a lot! I'm always here to help! 💪🏠",
            "You're making me blush (if I could)! 😄 Thanks!",
            "Thank you! I try my best to keep your home running smoothly! 🏠✨",
        ]
        return random.choice(compliments)

    # --- YES / NO / OK ---
    if q in ["yes", "yeah", "yep", "yup", "sure", "ok", "okay", "k", "alright", "right", "correct", "exactly"]:
        return "Got it! 👍 Let me know if there's anything else you need!"
    if q in ["no", "nah", "nope", "not really", "no thanks"]:
        return "Alright! I'm here whenever you need me. 😊"

    # --- APOLOGIES ---
    if any(phrase in q for phrase in ["sorry", "my bad", "apologies", "excuse me", "pardon"]):
        return "No worries at all! 😊 How can I help you?"

    # --- BORED ---
    if any(phrase in q for phrase in ["bored", "nothing to do", "entertain me"]):
        import random
        bored = [
            "How about checking your home status? Maybe something needs attention! 🏠",
            "Want me to tell you a joke? Or how about we check if all your doors are locked? 🔒",
            "You could try controlling your smart devices! Try 'turn on all lights' for a fun light show! 💡✨",
        ]
        return random.choice(bored)

    # --- TIME RELATED ---
    if any(phrase in q for phrase in ["what time", "what's the time", "whats the time", "current time", "what day"]):
        from datetime import datetime
        now = datetime.now()
        return f"It's currently {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}. ⏰"

    # --- WEATHER (redirect) ---
    if any(phrase in q for phrase in ["weather", "raining", "sunny", "cloudy", "forecast"]):
        return f"I don't have weather data, but inside your home it's {home_state['temperature']}°C with {home_state['humidity']}% humidity! 🌡️ For outdoor weather, try a weather app."

    # --- GOOD / BAD DAY ---
    if any(phrase in q for phrase in ["good day", "bad day", "having a rough day", "great day", "nice day"]):
        return "I hope your day gets even better! 😊 Let me know if I can help make things more comfortable at home! 🏠"

    # --- RANDOM CHITCHAT ---
    if any(phrase in q for phrase in ["what's up", "whats up", "wassup", "sup"]):
        import random
        chitchat = [
            "Not much! Just monitoring your home and keeping things secure. 🏠 What's up with you?",
            "Just keeping an eye on things! Everything looks good at home. 😊 Need anything?",
            "Hey! All systems are running smoothly. What can I do for you? 👍",
        ]
        return random.choice(chitchat)
    
    # No match — fall back to AI
    return None


def chatbot_response(user_input):
    """
    Generate AI response based on user input and current home state.
    Also detects and executes smart home commands via Alexa.
    
    For commands: executes instantly and returns a pre-built confirmation (no AI call).
    For questions: calls the AI API for a natural language response.
    
    Returns:
        dict: {'response': str, 'commands': list, 'alexa_results': list}
    """
    # 1. Parse for smart home commands
    commands = parse_smart_commands(user_input)
    alexa_results = []
    
    # 2. Execute any commands found
    if commands:
        alexa_results = execute_alexa_commands(commands)
        
        # Build an instant confirmation response (no AI call needed for commands)
        successful = [r for r in alexa_results if r["success"]]
        failed = [r for r in alexa_results if not r["success"]]
        
        response_parts = []
        if successful:
            actions = ", ".join([f"{r['action']} the {r['device']}" for r in successful])
            response_parts.append(f"Done! I've sent the command to Alexa to {actions}.")
        if failed:
            for r in failed:
                if "blocked_reason" in r:
                    response_parts.append(f"⚠️ {r['blocked_reason']}")
                else:
                    response_parts.append(f"❌ Couldn't update: {r['device']}.")
        
        return {
            "response": " ".join(response_parts),
            "commands": [r["alexa_cmd"] for r in alexa_results],
            "alexa_results": alexa_results
        }
    
    # 3. Try instant local answer first (no API call needed for common questions)
    local = try_local_answer(user_input)
    if local:
        safe_print(f"[DEBUG] Local answer (instant): {local[:80]}...")
        return {
            "response": local,
            "commands": [],
            "alexa_results": []
        }
    
    # 4. Complex question — call the AI API
    system_prompt = f"""You are HomeGuardAI, a friendly and intelligent home security assistant connected to Alexa.
You can both chat naturally with humans AND answer questions about their home.

Current home status:

{get_home_status()}

Guidelines:
- Be warm, friendly, and conversational — like talking to a helpful friend
- Keep answers short and clear (1-3 sentences max)
- If asked about home status, give specific details from the data above
- If something is unusual or concerning (door open, motion detected), highlight it
- If asked general questions (small talk, jokes, opinions, etc.), respond naturally and warmly
- If asked about something outside your knowledge, politely redirect or say you're not sure
- Always maintain a helpful, positive tone with emojis where appropriate"""


    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 150,
        "temperature": temperature,
        "top_p": 0.95,
        "stream": False,
    }

    try:
        print(f"[DEBUG] Calling NVIDIA API with model: {model}")
        response = requests.post(invoke_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        bot_response = data['choices'][0]['message']['content']
        safe_print(f"[DEBUG] API Response received: {bot_response[:100]}...")
        
        return {
            "response": bot_response,
            "commands": [],
            "alexa_results": []
        }
    
    except Exception as e:
        print(f"[ERROR] AI service error: {type(e).__name__}: {e}")
        return {
            "response": f"Error connecting to AI service: {str(e)}",
            "commands": [],
            "alexa_results": []
        }


def run_chat_loop():
    """Run interactive chat loop"""
    print("\n" + "="*50)
    print("[HOME] HOME MONITORING CHATBOT")
    print("="*50)
    print("Ask me anything about your home status!")
    print("Type 'exit' to quit | 'status' to see full report\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if user_input.lower() == "status":
                print("\nBot:" + get_home_status())
                continue
            
            result = chatbot_response(user_input)
            if result["commands"]:
                safe_print(f"\nAlexa Commands Sent:")
                for cmd in result["commands"]:
                    safe_print(f"   -> {cmd}")
            safe_print(f"\nBot: {result['response']}\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == "__main__":
    run_chat_loop()
