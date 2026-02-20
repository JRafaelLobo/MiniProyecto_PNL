import sys
import logging

# ❌ Bad (STDIO)
print("Processing request")

# ✅ Good (STDIO)
print("Processing request", file=sys.stderr)

# ✅ Good (STDIO)
logging.info("Processing request")
