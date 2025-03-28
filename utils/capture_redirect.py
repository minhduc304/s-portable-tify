import http.server
import socketserver
import threading
import webbrowser
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import urlparse, parse_qs
import queue

class SpotifyAuthHandler(http.server.SimpleHTTPRequestHandler):
    auth_queue = queue.Queue()
    
    def do_GET(self):
        # Parse the query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # Check if the path contains the authorization code
        if 'code' in query_params:
            SpotifyAuthHandler.auth_code = query_params['code'][0]
            
            # Send a response back to the user
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Authentication successful! You can close this window.')
        
        return

def start_local_server(port=8000):
    """Start a local server to capture the Spotify redirect"""
    handler = SpotifyAuthHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

def get_spotify_auth_code(client_id, client_secret, redirect_uri, scope):
    """
    Automatically obtain Spotify authorization code by starting a local server
    and opening the Spotify authorization URL in the default web browser
    """
    # Create the SpotifyOAuth object
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )
    
    # Start the local server in a separate thread
    server_thread = threading.Thread(target=start_local_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Get the authorization URL
    auth_url = auth_manager.get_authorize_url()
    
    # Open the authorization URL in the default web browser
    webbrowser.open(auth_url)
    
    # Wait for the auth code from the queue with a timeout
    try:
        auth_code = SpotifyAuthHandler.auth_queue.get(timeout=120)  # 2-minute timeout
        
        # Get the access token using the captured authorization code
        token_info = auth_manager.get_access_token(auth_code)
        
        return token_info
    except queue.Empty:
        print("Authentication timed out. Please try again.")
        return None
