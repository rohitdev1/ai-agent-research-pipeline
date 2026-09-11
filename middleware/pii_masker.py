import re
import time
from typing import Generator

def stream_anonymized_pipeline(user_input: str) -> Generator[str, None, None]:
    """
    Middleware proxy that strips sensitive emails before hitting an external API,
    and replaces them dynamically during the real-time token stream.
    """
    # 1. Setup our secure data mapping container
    pii_vault = {}
    
    # 2. Strict regular expression matching standard email structures
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    found_emails = re.findall(email_pattern, user_input)
    
    # 3. Anonymization: Mask emails with deterministic tokens
    anonymized_input = user_input
    for index, email in enumerate(found_emails):
        placeholder = f"[EMAIL_{index}]"
        pii_vault[placeholder] = email  # Store mapping internally
        anonymized_input = anonymized_input.replace(email, placeholder)
        
    print(f"🔒 [SECURITY PROXY] Outbound text safely anonymized: '{anonymized_input}'\n")

    # 4. Simulated LLM Response Stream (Simulating incoming token chunks)
    mock_llm_chunks = [
        "Processing ", "your ", "request... ", 
        "Updates ", "will ", "be ", "dispatched ", "directly ", 
        "to ", "[EMAIL_0]", " within ", "the ", "hour."
    ]
    
    # 5. De-anonymization: Reconstruct the stream live for the user frontend
    for chunk in mock_llm_chunks:
        unmasked_chunk = chunk
        
        # Check if the current incoming fragment contains any vault placeholders
        for placeholder, real_email in pii_vault.items():
            if placeholder in unmasked_chunk:
                unmasked_chunk = unmasked_chunk.replace(placeholder, real_email)
                
        # Simulate slight network streaming delay
        time.sleep(0.1)
        yield unmasked_chunk

if __name__ == "__main__":
    sample_input = "System alert: Please route updates to testuser@domain.com immediately."
    print(f"📥 [FRONTEND LOG] Incoming user query: '{sample_input}'\n")
    
    print("🌊 [FRONTEND STREAM LOG] Displaying inbound token feed:")
    for token_chunk in stream_anonymized_pipeline(sample_input):
        print(token_chunk, end="", flush=True)
    print("\n")
