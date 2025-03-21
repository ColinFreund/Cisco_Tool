import os
import sys
import logging
from app import app

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("cisco_manager.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 5000))
    
    # Start the server
    print(f"Starting Cisco Device Manager backend on port {port}")
    print(f"API available at http://localhost:{port}/api/")
    print(f"Press Ctrl+C to stop the server")
    
    app.run(host="0.0.0.0", port=port, debug=True)