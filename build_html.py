import os

src_dir = 'c:/creddemo/frontend'
dist_dir = 'c:/creddemo/frontend/dist'

if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

# Read header and footer
with open(os.path.join(src_dir, 'header.php'), 'r') as f:
    header = f.read()

with open(os.path.join(src_dir, 'footer.php'), 'r') as f:
    footer = f.read()
    footer = footer.replace('<?php echo date("Y"); ?>', '2026')

# Process files
files_to_process = ['index.php', 'chat.php', 'upload.php']

for file in files_to_process:
    with open(os.path.join(src_dir, file), 'r') as f:
        content = f.read()
        
    content = content.replace("<?php include 'header.php'; ?>", header)
    content = content.replace("<?php include 'footer.php'; ?>", footer)
    
    # Fix links
    content = content.replace('.php"', '.html"')
    
    new_file = file.replace('.php', '.html')
    with open(os.path.join(dist_dir, new_file), 'w') as f:
        f.write(content)

# Copy css
with open(os.path.join(src_dir, 'style.css'), 'r') as f:
    css = f.read()
with open(os.path.join(dist_dir, 'style.css'), 'w') as f:
    f.write(css)

print("HTML build complete!")
