from backend.feltfixinator_bridge import Bridge

if __name__ == "__main__":
    b = Bridge()
    print(b._ensure_llm_client())
