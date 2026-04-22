from collections import defaultdict

# store memory per session (temporary)
memory_store = defaultdict(list)

session_state = {}

def set_speaking(session_id, value):
    session_state[session_id] = value

def is_speaking(session_id):
    return session_state.get(session_id, False)

def add_to_memory(session_id, role, content):
    memory_store[session_id].append({
        "role": role,
        "content": content
    })

def get_memory(session_id):
    return memory_store[session_id]

def clear_memory(session_id):
    memory_store[session_id] = []