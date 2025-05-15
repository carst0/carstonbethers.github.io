import http.server
import socketserver
import json
import os
from urllib.parse import unquote

class BlogHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Decode URL-encoded path
        decoded_path = unquote(self.path)
        print(f"Received request for: {decoded_path}")
        
        # Handle blog posts listing
        if decoded_path == '/list_posts':
            try:
                posts = []
                blog_dir = os.path.join(os.getcwd(), 'Blog_posts')
                print(f"Scanning directory: {blog_dir}")
                
                if not os.path.exists(blog_dir):
                    print(f"Error: Blog directory not found at {blog_dir}")
                    self.send_error(404, "Blog directory not found")
                    return
                
                for file in os.listdir(blog_dir):
                    if file.endswith('.md') and file != 'STYLE_GUIDE.md':
                        posts.append(file)
                
                print(f"Found {len(posts)} blog posts: {posts}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(posts).encode())
                return
            except Exception as e:
                print(f"Error handling /list_posts: {str(e)}")
                self.send_error(500, str(e))
                return

        # Handle blog post content requests
        if decoded_path.startswith('/Blog_posts/') and decoded_path.endswith('.md'):
            try:
                file_path = os.path.join(os.getcwd(), decoded_path.lstrip('/'))
                if not os.path.exists(file_path):
                    print(f"Blog post not found: {file_path}")
                    self.send_error(404, "Blog post not found")
                    return
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/markdown')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                return
            except Exception as e:
                print(f"Error serving blog post: {str(e)}")
                self.send_error(500, str(e))
                return

        # Handle direct file requests
        try:
            # Map the URL path to the local file system
            if decoded_path == '/':
                decoded_path = '/index.html'
            
            # Get the absolute path but verify it's within the root directory
            requested_path = os.path.abspath(os.path.join(os.getcwd(), decoded_path.lstrip('/')))
            root_dir = os.getcwd()
            
            if not requested_path.startswith(root_dir):
                print(f"Security error: Attempted to access file outside root: {requested_path}")
                self.send_error(403, "Access denied")
                return
            
            print(f"Attempting to serve: {requested_path}")
            
            # Set content type for markdown files
            if requested_path.endswith('.md'):
                with open(requested_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/markdown')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                return
            
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
            
        except Exception as e:
            print(f"Error serving {decoded_path}: {str(e)}")
            self.send_error(500, str(e))
            return

    def end_headers(self):
        # Add CORS headers for all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

PORT = 8000
Handler = BlogHandler

print(f"Starting server at http://localhost:{PORT}")
print(f"Serving files from: {os.getcwd()}")
print(f"Blog posts directory: {os.path.join(os.getcwd(), 'Blog_posts')}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server is running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close() 