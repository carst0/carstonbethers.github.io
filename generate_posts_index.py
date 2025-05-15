import os
import json

def generate_posts_index():
    blog_dir = 'Blog_posts'
    posts = []
    
    for file in os.listdir(blog_dir):
        if file.endswith('.md') and file != 'STYLE_GUIDE.md':
            posts.append(file)
    
    # Sort posts alphabetically for consistent ordering
    posts.sort()
    
    # Write the index file
    with open('posts_index.json', 'w') as f:
        json.dump(posts, f, indent=2)
    
    print(f'Generated posts_index.json with {len(posts)} posts')

if __name__ == '__main__':
    generate_posts_index() 