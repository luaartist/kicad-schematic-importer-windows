import os
import math
from typing import List, Optional

def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text using a simple heuristic.
    On average, 1 token is about 4 characters in English text.
    """
    return math.ceil(len(text) / 4)

def is_string_literal_start(line: str) -> bool:
    """Check if line starts a multi-line string"""
    stripped = line.strip()
    return stripped.startswith(('"""', "'''", 'r"""', "r'''", 'f"""', "f'''"))

def is_data_structure_start(line: str) -> bool:
    """Check if line starts a data structure"""
    stripped = line.strip()
    return (
        stripped.startswith(('[', '{', '(')) or
        '=' in stripped and any(c in stripped for c in '[{(') or
        stripped.startswith('<script') or  # Handle embedded scripts
        stripped.startswith('{"') or  # Handle JSON data
        stripped.startswith("{'")  # Handle JSON data with single quotes
    )

def process_json_block(lines: List[str], start_idx: int, max_chars: int) -> tuple[List[str], int]:
    """Special handling for JSON/HTML blocks to split them into smaller chunks"""
    chunks = []
    current_chunk = []
    current_length = 0
    i = start_idx
    brace_level = 0
    max_chunk_size = max_chars // 2  # More aggressive limit for JSON data
    
    def save_current_chunk(force_split: bool = False) -> None:
        nonlocal current_chunk, current_length
        if current_chunk:
            # Add a continuation marker if we're forcing a split
            if force_split and brace_level > 0:
                current_chunk.append("# ... JSON continued in next chunk")
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_length = 0
            if force_split and brace_level > 0:
                current_chunk.append("# ... JSON continuation from previous chunk")
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        line_length = len(line) + 1  # +1 for newline
        
        # Track brace level to maintain JSON structure
        if not stripped.startswith('"') and not stripped.startswith("'"):
            brace_level += stripped.count('{') + stripped.count('[')
            brace_level -= stripped.count('}') + stripped.count(']')
        
        # Force split conditions
        force_split = False
        if current_length + line_length > max_chunk_size:
            force_split = True
        elif len(current_chunk) > 100:  # Also split if too many lines
            force_split = True
        
        if force_split:
            save_current_chunk(force_split=True)
        
        # Special handling for extremely long lines
        if line_length > max_chunk_size:
            # Split long line into smaller pieces
            remaining = line
            while remaining:
                chunk_size = max_chunk_size - 50  # Leave room for continuation marks
                if len(remaining) > chunk_size:
                    split_point = remaining.rfind(',', 0, chunk_size)
                    if split_point == -1:
                        split_point = chunk_size
                    chunks.append(remaining[:split_point] + " \\")
                    remaining = remaining[split_point:].lstrip()
                else:
                    chunks.append(remaining)
                    remaining = ""
        else:
            current_chunk.append(line)
            current_length += line_length
        
        i += 1
        
        # Break if we've reached the end of the JSON block
        if brace_level == 0 and stripped.endswith(('}', ']', '</script>')):
            break
    
    save_current_chunk()
    return chunks, i

def process_large_block(lines: List[str], start_idx: int, max_chars: int) -> tuple[List[str], int]:
    """
    Process an extremely large block of code by forcing splits at regular intervals.
    Returns the processed chunks and the new current index.
    """
    chunks = []
    current_chunk = []
    current_length = 0
    i = start_idx
    
    while i < len(lines):
        line = lines[i]
        line_length = len(line) + 1  # +1 for newline
        stripped = line.strip()
        
        # Special handling for JSON/HTML blocks
        if is_data_structure_start(stripped):
            # Save any existing content
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0
            
            # Process the JSON block with a header
            json_chunks, new_idx = process_json_block(lines, i, max_chars)
            for j, json_chunk in enumerate(json_chunks):
                chunk_header = f"# JSON block part {j+1}/{len(json_chunks)}\n"
                chunks.append(chunk_header + json_chunk)
            
            # Update position and skip to next line
            i = new_idx + 1
            continue
        
        # Force split if chunk is getting too large
        if current_length + line_length > max_chars or len(current_chunk) > 50:
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0
        
        current_chunk.append(line)
        current_length += line_length
        i += 1
        
        # Break at a good boundary if we've processed enough
        if (i - start_idx) > 50:
            if (
                not stripped or  # Empty line
                stripped.startswith('#') or  # Comment
                stripped.endswith((':', '}', ']', ')', ',')) or  # End of block
                i >= len(lines)  # End of file
            ):
                break
    
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    
    return chunks, i

def split_into_chunks(text: str, max_tokens: int = 800, max_lines: int = 200) -> List[str]:
    """
    Split text into chunks while trying to maintain code structure integrity.
    
    Args:
        text: The input text to split
        max_tokens: Maximum estimated tokens per chunk
    
    Returns:
        List of text chunks
    """
    # Convert max tokens to approximate char count (4 chars ≈ 1 token)
    max_chars = max_tokens * 4
    
    # Split text by newline to keep lines intact
    lines = text.splitlines()
    chunks = []
    current_chunk = []
    current_length = 0
    
    def save_chunk():
        if current_chunk:
            chunk_text = "\n".join(current_chunk)
            # Add a comment at the start of each chunk indicating its position
            chunk_number = len(chunks) + 1
            header = f"# Chunk {chunk_number}\n"
            chunks.append(header + chunk_text)
    
    in_class = False
    in_function = False
    indent_level = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        # Calculate the line's indent level
        stripped_line = line.lstrip()
        current_indent = len(line) - len(stripped_line)
        
        # Check for class/function definitions
        if stripped_line.startswith(('class ', 'def ')):
            if current_indent == 0:
                # If we're at root level, this is a good place to split
                if current_length > max_chars:
                    save_chunk()
                    current_chunk = []
                    current_length = 0
            indent_level = current_indent
            

        line_is_splittable = (
            not line.strip() or  # Empty line
            line.lstrip().startswith('#') or  # Comment line
            (indent_level == 0 and not in_class and not in_function) or  # Root level code
            is_data_structure_start(line) or  # Start of potentially large data structure
            len(current_chunk) >= max_lines  # Exceeded maximum lines per chunk
        )

        # Handle extremely large blocks differently
        if current_length > max_chars * 3 or len(current_chunk) >= max_lines:
            # Check if this is a JSON/data structure block first
            if any(is_data_structure_start(line.strip()) for line in current_chunk):
                # Process as JSON with current chunk as context
                all_lines = current_chunk + lines[i:]
                json_chunks, new_idx = process_json_block(all_lines, 0, max_chars)
                
                # Save with appropriate headers
                for j, json_chunk in enumerate(json_chunks):
                    chunk_header = f"# Large JSON block part {j+1}/{len(json_chunks)}\n"
                    chunks.append(chunk_header + json_chunk)
                
                # Reset state and update position
                current_chunk = []
                current_length = 0
                i = new_idx + 1
                continue
            
            # If not JSON, save current chunk and continue with normal processing
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0
            
        # Normal splitting conditions
        elif current_length + len(line) + 1 > max_chars:
            should_split = False
            
            # Split if we're extremely over the limit (2x)
            if current_length > max_chars * 2:
                should_split = True
            # Split if we're moderately over (1.5x) and have a splittable line
            elif current_length > max_chars * 1.5 and line_is_splittable:
                should_split = True
            # Split at root level
            elif indent_level == 0 and not in_class and not in_function:
                should_split = True
            
            if should_split:
                save_chunk()
                current_chunk = []
                current_length = 0
        
        # Add a warning comment if we're forced to split inside a function/class
        if len(current_chunk) == 0:
            if in_class or in_function:
                current_chunk.append(f"# Warning: Forced split inside {'class' if in_class else 'function'} due to size")
            if current_length > max_chars * 2:
                current_chunk.append("# Warning: Large code block detected - forced aggressive split")
        
        current_chunk.append(line)
        current_length += len(line) + 1  # +1 for newline
        i += 1
        
        # Update state
        if stripped_line.startswith('class '):
            in_class = True
        elif stripped_line.startswith('def '):
            in_function = True
        elif stripped_line and current_indent <= indent_level:
            in_class = False
            in_function = False
    
    # Save the last chunk
    save_chunk()
    
    return chunks

def split_file(filepath: str, max_tokens: int = 800, max_lines: int = 200, output_dir: Optional[str] = None) -> List[str]:
    """
    Split a file into multiple chunks and save them.
    
    Args:
        filepath: Path to the input file
        max_tokens: Maximum tokens per chunk
        output_dir: Directory to save the chunks (defaults to same directory as input)
    
    Returns:
        List of paths to the created chunk files
    """
    # Read the input file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the chunks
    chunks = split_into_chunks(content, max_tokens, max_lines)
    
    # Determine output directory
    if output_dir is None:
        output_dir = os.path.dirname(filepath)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filenames
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_files = []
    
    # Save each chunk to a file
    for i, chunk in enumerate(chunks, 1):
        output_path = os.path.join(output_dir, f"{base_name}_part{i}.py")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(chunk)
        output_files.append(output_path)
        
        # Print some stats about the chunk
        estimated_tokens = estimate_tokens(chunk)
        print(f"Created {output_path} (estimated tokens: {estimated_tokens})")
    
    return output_files

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python token_splitter.py <file_to_split>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    split_file(input_file)
