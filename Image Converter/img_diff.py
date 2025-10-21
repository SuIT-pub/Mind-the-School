import cv2
import numpy as np
import os
import glob
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading

def process_image_difference(base_image, target_image_path, face_position=None, threshold_value=1):
    """
    Process the difference between base image and target image.
    face_position: (cx, cy, rx, ry) tuple from face detection, or None if no face
    threshold_value: threshold for difference detection (0-255, lower = more sensitive)
    Returns the difference result as a 4-channel BGRA image.
    """
    # load target image with alpha channel support
    image2 = cv2.imread(target_image_path, cv2.IMREAD_UNCHANGED)
    
    if image2 is None:
        log_print(f"Warning: Could not load image {target_image_path}")
        return None

    # ensure both images have the same dimensions
    if base_image.shape[:2] != image2.shape[:2]:
        log_print(f"Warning: Images have different dimensions. Resizing {target_image_path} to match base image.")
        image2 = cv2.resize(image2, (base_image.shape[1], base_image.shape[0]))

    # handle alpha channels - convert to 3-channel if needed
    if len(base_image.shape) == 3 and base_image.shape[2] == 4:
        # base_image has alpha channel, use only RGB channels
        image1_rgb = base_image[:, :, :3]
        image1_alpha = base_image[:, :, 3]
    else:
        image1_rgb = base_image
        image1_alpha = None

    if len(image2.shape) == 3 and image2.shape[2] == 4:
        # image2 has alpha channel, use only RGB channels
        image2_rgb = image2[:, :, :3]
        image2_alpha = image2[:, :, 3]
    else:
        image2_rgb = image2
        image2_alpha = None

    # compute absolute difference on RGB channels only
    difference = cv2.absdiff(image2_rgb, image1_rgb)

    # convert to grayscale for thresholding
    gray_diff = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

    # create a mask for areas with substantial content in both images
    content_mask = np.ones_like(gray_diff, dtype=np.uint8) * 255

    if image1_alpha is not None and image2_alpha is not None:
        # only consider differences in areas where both images have substantial content
        # use a higher threshold to avoid edge artifacts from anti-aliasing
        alpha_threshold = 200  # very high threshold to focus on solid content
        both_solid = (image1_alpha > alpha_threshold) & (image2_alpha > alpha_threshold)
        content_mask = both_solid.astype(np.uint8) * 255
    elif image1_alpha is not None:
        alpha_threshold = 200
        content_mask = (image1_alpha > alpha_threshold).astype(np.uint8) * 255
    elif image2_alpha is not None:
        alpha_threshold = 200
        content_mask = (image2_alpha > alpha_threshold).astype(np.uint8) * 255

    # apply content mask to the difference image
    masked_diff = cv2.bitwise_and(gray_diff, content_mask)

    # create a threshold to identify significant differences
    # adjust threshold value as needed (0-255, lower = more sensitive)
    _, mask = cv2.threshold(masked_diff, threshold_value, 255, cv2.THRESH_BINARY)

    # apply morphological operations to remove edge artifacts and small noise
    # use opening to remove small noise and closing to fill gaps
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # remove small noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # fill small gaps


    # apply additional erosion to remove edge artifacts
    kernel_erode = np.ones((2,2), np.uint8)
    mask = cv2.erode(mask, kernel_erode, iterations=1)

    # restrict differences to an oval around the detected face
    if face_position is not None:
        cx, cy, rx, ry = face_position
        face_mask = np.zeros_like(mask, dtype=np.uint8)
        cv2.ellipse(face_mask, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
        mask = cv2.bitwise_and(mask, face_mask)
        log_print(f"Applied face mask at position ({cx}, {cy}) with radius ({rx}, {ry})")
    else:
        log_print("No face position provided, processing entire image")

    # create 4-channel image (BGRA) for transparency
    result = np.zeros((base_image.shape[0], base_image.shape[1], 4), dtype=np.uint8)

    # copy the new image RGB channels to the result
    result[:, :, :3] = image2_rgb

    # create final alpha channel
    final_alpha = mask.copy()

    # make the entire lower half transparent (cut off everything below the middle)
    height = result.shape[0]
    middle_y = height // 4
    final_alpha[middle_y:, :] = 0  # make lower half transparent

    # also make the result image transparent in the lower half
    result[middle_y:, :, :3] = 0  # clear RGB channels in lower half

    result[:, :, 3] = final_alpha

    return result

base_path = os.path.dirname(os.path.abspath(__file__))

# Create log folder and set up logging
log_folder = os.path.join(base_path, "logs")
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, f"diff_processing_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def log_print(message):
    """Print message to console and write to log file."""
    print(message)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

class ProgressWindow:
    """A simple progress window that shows processing status."""
    
    def __init__(self, total_images):
        self.total_images = total_images
        self.current_image = 0
        self.current_base = ""
        self.current_target = ""
        self.root = None
        self.is_running = False
        
        # Create progress window
        self.root = tk.Toplevel()
        self.root.title("Processing Images...")
        self.root.geometry("500x200")
        self.root.resizable(False, False)
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Processing Images", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Status labels
        self.status_label = ttk.Label(main_frame, text="Initializing...", font=("Arial", 10))
        self.status_label.pack(pady=(0, 5))
        
        self.detail_label = ttk.Label(main_frame, text="", font=("Arial", 9), foreground="gray")
        self.detail_label.pack(pady=(0, 10))
        
        # Progress text
        self.progress_text = ttk.Label(main_frame, text="0 / 0 images processed", font=("Arial", 10))
        self.progress_text.pack()
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.is_running = True
    
    def update_progress(self, current_image, current_base="", current_target=""):
        """Update the progress display."""
        if not self.is_running or not self.root:
            return
            
        try:
            self.current_image = current_image
            self.current_base = current_base
            self.current_target = current_target
            
            # Calculate percentage
            percentage = (current_image / self.total_images) * 100 if self.total_images > 0 else 0
            
            # Update progress bar
            self.progress_var.set(percentage)
            
            # Update status text
            if current_base and current_target:
                self.status_label.config(text=f"Processing: {os.path.basename(current_base)}")
                self.detail_label.config(text=f"Target: {os.path.basename(current_target)}")
            elif current_base:
                self.status_label.config(text=f"Processing base: {os.path.basename(current_base)}")
                self.detail_label.config(text="Detecting face...")
            else:
                self.status_label.config(text="Processing images...")
                self.detail_label.config(text="")
            
            # Update progress text
            self.progress_text.config(text=f"{current_image} / {self.total_images} images processed")
            
            # Update the window
            self.root.update_idletasks()
        except tk.TclError:
            # Window was closed
            self.is_running = False
    
    def close(self):
        """Close the progress window."""
        if self.root and self.is_running:
            try:
                self.is_running = False
                self.root.destroy()
            except tk.TclError:
                pass

def detect_face_in_image(image):
    """
    Detect face in an image and return face position parameters.
    Returns (cx, cy, rx, ry) if face found, None otherwise.
    """
    try:
        # Convert to grayscale for face detection
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Load face cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        
        if len(faces) > 0:
            # Choose the largest detected face
            x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
            # Expand the region to include forehead/hair and cheeks
            expand_w = int(w * 0.08)
            expand_h = int(h * 0.13)
            cx = x + w // 2
            cy = y + h // 2
            rx = (w // 2) + expand_w
            ry = (h // 2) + expand_h
            return (cx, cy, rx, ry)
        else:
            return None
    except Exception as e:
        log_print(f"Face detection error: {e}")
        return None

def manual_face_selection(image, image_name):
    """
    Open a window for manual face selection on the image.
    Returns (cx, cy, rx, ry) if user selects a face, None if cancelled.
    """
    face_position = None
    
    # Create main window
    root = tk.Toplevel()
    root.title(f"Manual Face Selection - {image_name}")
    root.geometry("800x600")
    root.grab_set()  # Make window modal
    
    # Convert OpenCV image to PIL Image
    if len(image.shape) == 3:
        # BGR to RGB conversion
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image_rgb = image
    
    pil_image = Image.fromarray(image_rgb)
    
    # Resize image to fit window while maintaining aspect ratio
    display_width = 700
    display_height = 500
    pil_image.thumbnail((display_width, display_height), Image.Resampling.LANCZOS)
    
    # Convert to PhotoImage for tkinter
    photo = ImageTk.PhotoImage(pil_image)
    
    # Create main frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Instructions
    instructions = ttk.Label(main_frame, 
                           text="Click and drag to draw an oval around the face. Right-click to confirm or press 'Skip' to cancel.",
                           font=("Arial", 10))
    instructions.pack(pady=(0, 10))
    
    # Create canvas for image
    canvas = tk.Canvas(main_frame, width=display_width, height=display_height, bg='white')
    canvas.pack(pady=(0, 10))
    
    # Display image
    canvas.create_image(display_width//2, display_height//2, image=photo)
    
    # Variables for drawing
    start_x = start_y = 0
    oval_id = None
    is_drawing = False
    
    # Calculate scale factors for coordinate conversion
    scale_x = image.shape[1] / pil_image.width
    scale_y = image.shape[0] / pil_image.height
    
    def start_draw(event):
        nonlocal start_x, start_y, is_drawing
        start_x = event.x
        start_y = event.y
        is_drawing = True
    
    def draw_oval(event):
        nonlocal oval_id
        if is_drawing and oval_id:
            canvas.delete(oval_id)
        
        if is_drawing:
            # Draw oval from start point to current mouse position
            oval_id = canvas.create_oval(start_x, start_y, event.x, event.y, 
                                       outline='red', width=2, fill='', dash=(5, 5))
    
    def stop_draw(event):
        nonlocal is_drawing, face_position
        
        if is_drawing:
            is_drawing = False
            
            # Calculate oval parameters
            x1, y1 = start_x, start_y
            x2, y2 = event.x, event.y
            
            # Ensure x1 < x2 and y1 < y2
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            
            # Calculate center and radius
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            rx = (x2 - x1) // 2
            ry = (y2 - y1) // 2
            
            # Convert to original image coordinates
            cx_orig = int(cx * scale_x)
            cy_orig = int(cy * scale_y)
            rx_orig = int(rx * scale_x)
            ry_orig = int(ry * scale_y)
            
            face_position = (cx_orig, cy_orig, rx_orig, ry_orig)
            
            # Draw final oval
            canvas.delete(oval_id)
            canvas.create_oval(x1, y1, x2, y2, outline='green', width=3, fill='', dash=(5, 5))
            
            # Show confirmation
            confirm_label = ttk.Label(main_frame, text="Face position set! Right-click to confirm or draw again to adjust.", 
                                    foreground='green', font=("Arial", 10, "bold"))
            confirm_label.pack(pady=(5, 0))
    
    def confirm_selection(event=None):
        nonlocal face_position
        if face_position:
            root.grab_release()
            root.quit()
            root.destroy()
        else:
            messagebox.showwarning("No Selection", "Please draw an oval around the face first.")
    
    def skip_selection():
        nonlocal face_position
        face_position = None
        root.grab_release()
        root.quit()
        root.destroy()
    
    # Bind mouse events
    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", draw_oval)
    canvas.bind("<ButtonRelease-1>", stop_draw)
    canvas.bind("<Button-3>", confirm_selection)  # Right-click to confirm
    
    # Button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=(10, 0))
    
    ttk.Button(button_frame, text="Confirm Selection", command=confirm_selection).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(button_frame, text="Skip This Image", command=skip_selection).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(button_frame, text="Clear & Redraw", command=lambda: canvas.delete("all") or canvas.create_image(display_width//2, display_height//2, image=photo)).pack(side=tk.LEFT)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Start the GUI
    try:
        root.mainloop()
    except Exception as e:
        log_print(f"Error in manual face selection GUI: {e}")
        face_position = None
    
    return face_position

def get_image_name_without_extension(filepath):
    """Extract the base name without extension from a file path."""
    return os.path.splitext(os.path.basename(filepath))[0]

def find_matching_images(base_name, images_folder):
    """Find all images in the images folder that start with the base name."""
    matching_images = []
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.tif']
    
    for extension in image_extensions:
        # Search for both lowercase and uppercase extensions
        pattern_lower = os.path.join(images_folder, f"{base_name} *{extension}")
        pattern_upper = os.path.join(images_folder, f"{base_name} *{extension.upper()}")
        
        matching_images.extend(glob.glob(pattern_lower))
        matching_images.extend(glob.glob(pattern_upper))
    
    return matching_images

def create_gui_selection(base_image_files):
    """
    Create a GUI window to select which base images to process.
    Returns a tuple of (selected_base_image_paths, threshold_value).
    """
    selected_images = []
    threshold_value = 1
    
    # Create main window
    root = tk.Tk()
    root.title("Select Base Images to Process")
    root.geometry("600x500")
    root.resizable(True, True)
    
    # Create main frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Configure grid weights
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)
    
    # Title label
    title_label = ttk.Label(main_frame, text="Select Base Images to Process:", font=("Arial", 12, "bold"))
    title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
    
    # Threshold setting frame
    threshold_frame = ttk.LabelFrame(main_frame, text="Difference Detection Sensitivity", padding="5")
    threshold_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    threshold_frame.columnconfigure(1, weight=1)
    
    # Threshold label and slider
    ttk.Label(threshold_frame, text="Threshold:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
    threshold_var = tk.IntVar(value=1)
    threshold_scale = ttk.Scale(threshold_frame, from_=0, to=50, variable=threshold_var, orient=tk.HORIZONTAL)
    threshold_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
    threshold_label = ttk.Label(threshold_frame, text="1")
    threshold_label.grid(row=0, column=2, sticky=tk.W)
    
    # Update threshold label when slider changes
    def update_threshold_label(*args):
        threshold_label.config(text=str(int(threshold_var.get())))
    threshold_var.trace('w', update_threshold_label)
    
    # Threshold description
    ttk.Label(threshold_frame, text="Lower values = more sensitive (detects smaller differences)", 
              font=("Arial", 8), foreground="gray").grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
    
    # Create frame for checkboxes with scrollbar
    checkbox_frame = ttk.Frame(main_frame)
    checkbox_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
    checkbox_frame.columnconfigure(0, weight=1)
    
    # Create canvas and scrollbar
    canvas = tk.Canvas(checkbox_frame)
    scrollbar = ttk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Store checkboxes
    checkboxes = {}
    
    # Create checkboxes for each base image
    for i, base_file in enumerate(base_image_files):
        var = tk.BooleanVar(value=True)  # Checked by default
        checkbox = ttk.Checkbutton(
            scrollable_frame, 
            text=os.path.basename(base_file),
            variable=var
        )
        checkbox.grid(row=i, column=0, sticky=tk.W, pady=2)
        checkboxes[base_file] = var
    
    # Pack canvas and scrollbar
    canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    # Button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=3, column=0, pady=(10, 0))
    
    def select_all():
        """Select all checkboxes."""
        for var in checkboxes.values():
            var.set(True)
    
    def deselect_all():
        """Deselect all checkboxes."""
        for var in checkboxes.values():
            var.set(False)
    
    def start_processing():
        """Start processing with selected images."""
        nonlocal selected_images, threshold_value
        selected_images = [base_file for base_file, var in checkboxes.items() if var.get()]
        threshold_value = int(threshold_var.get())
        
        if not selected_images:
            messagebox.showwarning("No Selection", "Please select at least one base image to process.")
            return
        
        root.quit()
        root.destroy()
    
    def cancel_processing():
        """Cancel processing."""
        nonlocal selected_images
        selected_images = []
        root.quit()
        root.destroy()
    
    # Buttons
    ttk.Button(button_frame, text="Select All", command=select_all).grid(row=0, column=0, padx=(0, 5))
    ttk.Button(button_frame, text="Deselect All", command=deselect_all).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="Start Processing", command=start_processing).grid(row=0, column=2, padx=5)
    ttk.Button(button_frame, text="Cancel", command=cancel_processing).grid(row=0, column=3, padx=(5, 0))
    
    # Bind mousewheel to canvas
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Start the GUI
    try:
        root.mainloop()
    except Exception as e:
        log_print(f"Error in GUI selection: {e}")
        selected_images = []
        threshold_value = 1
    
    return selected_images, threshold_value

# Main execution
if __name__ == "__main__":
    # Log the start of processing
    log_print(f"Starting image difference processing...")
    log_print(f"Log folder: {log_folder}")
    
    # Get all base images from the base folder
    base_folder = os.path.join(base_path, "base")
    if not os.path.exists(base_folder):
        log_print(f"Error: Base folder '{base_folder}' does not exist")
        exit(1)
    
    # Get all image files in the base folder
    base_image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.tif']
    base_image_files = []
    
    for extension in base_image_extensions:
        base_image_files.extend(glob.glob(os.path.join(base_folder, extension)))
        base_image_files.extend(glob.glob(os.path.join(base_folder, extension.upper())))
    
    if not base_image_files:
        log_print(f"No base image files found in '{base_folder}' folder")
        exit(1)
    
    # Show GUI for base image selection
    log_print(f"Found {len(base_image_files)} base image(s). Opening selection window...")
    try:
        selected_base_images, threshold_value = create_gui_selection(base_image_files)
    except Exception as e:
        log_print(f"Error in GUI selection: {e}")
        log_print("Falling back to processing all images with default threshold...")
        selected_base_images = base_image_files
        threshold_value = 1
    
    if not selected_base_images:
        log_print("No base images selected. Exiting.")
        exit(0)
    
    log_print(f"Selected {len(selected_base_images)} base image(s) for processing:")
    for base_file in selected_base_images:
        log_print(f"  - {os.path.basename(base_file)}")
    log_print(f"Using threshold value: {threshold_value}")
    
    # Get all image files in the images folder
    images_folder = os.path.join(base_path, "images")
    if not os.path.exists(images_folder):
        log_print(f"Error: Images folder '{images_folder}' does not exist")
        exit(1)
    
    # Create output folder
    output_folder = os.path.join(base_path, "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        log_print(f"Created output folder: {output_folder}")
    else:
        log_print(f"Using existing output folder: {output_folder}")
    
    # Calculate total number of images to process
    total_images_to_process = 0
    for base_image_path in selected_base_images:
        base_name = get_image_name_without_extension(base_image_path)
        matching_images = find_matching_images(base_name, images_folder)
        total_images_to_process += len(matching_images)
    
    log_print(f"Total images to process: {total_images_to_process}")
    
    # Create progress window (only if we have images to process)
    progress_window = None
    if total_images_to_process > 0:
        try:
            progress_window = ProgressWindow(total_images_to_process)
        except Exception as e:
            log_print(f"Warning: Could not create progress window: {e}")
            progress_window = None
    
    total_processed = 0
    current_image_count = 0
    
    # Process each selected base image
    for base_image_path in selected_base_images:
        log_print(f"\n{'='*60}")
        log_print(f"Processing base image: {os.path.basename(base_image_path)}")
        log_print(f"{'='*60}")
        
        # Load base image
        base_image = cv2.imread(base_image_path, cv2.IMREAD_UNCHANGED)
        if base_image is None:
            log_print(f"Error: Could not load base image {base_image_path}")
            continue
        
        # Update progress - processing base image
        if progress_window:
            try:
                progress_window.update_progress(current_image_count, base_image_path)
            except Exception as e:
                log_print(f"Warning: Could not update progress: {e}")
        
        # Detect face in base image
        log_print("Detecting face in base image...")
        face_position = detect_face_in_image(base_image)
        
        if face_position is None:
            log_print("No face detected automatically - opening manual selection window...")
            try:
                face_position = manual_face_selection(base_image, os.path.basename(base_image_path))
            except Exception as e:
                log_print(f"Error in manual face selection: {e}")
                face_position = None
            
            if face_position is None:
                log_print("No face position selected - skipping this base image")
                continue
            else:
                cx, cy, rx, ry = face_position
                log_print(f"Manual face selection at position ({cx}, {cy}) with radius ({rx}, {ry})")
        else:
            cx, cy, rx, ry = face_position
            log_print(f"Face detected automatically at position ({cx}, {cy}) with radius ({rx}, {ry})")
        
        # Get the base name (without extension)
        base_name = get_image_name_without_extension(base_image_path)
        log_print(f"Looking for images starting with: '{base_name}'")
        
        # Find matching images in the images folder
        matching_images = find_matching_images(base_name, images_folder)
        
        if not matching_images:
            log_print(f"  No matching images found for '{base_name}'")
            continue
        
        log_print(f"  Found {len(matching_images)} matching image(s):")
        for img_file in matching_images:
            log_print(f"    - {os.path.basename(img_file)}")
        
        # Process each matching image
        processed_count = 0
        for image_path in matching_images:
            log_print(f"\n  Processing: {os.path.basename(base_image_path)} {os.path.basename(image_path)}")
            
            # Update progress - processing target image
            if progress_window:
                try:
                    progress_window.update_progress(current_image_count, base_image_path, image_path)
                except Exception as e:
                    log_print(f"Warning: Could not update progress: {e}")
            
            # Process the difference
            result = process_image_difference(base_image, image_path, face_position, threshold_value)
            
            if result is not None:
                # Create output filename (same name as original)
                output_filename = os.path.basename(image_path)
                output_path = os.path.join(output_folder, output_filename)
                
                # Save the difference image to output folder
                cv2.imwrite(output_path, result)
                processed_count += 1
                total_processed += 1
                log_print(f"    ✓ Successfully processed and saved to: {output_filename}")
            else:
                log_print(f"    ✗ Failed to process")
            
            current_image_count += 1
        
        log_print(f"\n  Base '{base_name}': {processed_count}/{len(matching_images)} images processed")
    
    # Close progress window
    if progress_window:
        try:
            progress_window.close()
        except Exception as e:
            log_print(f"Warning: Could not close progress window: {e}")
    
    log_print(f"\n{'='*60}")
    log_print(f"OVERALL SUMMARY")
    log_print(f"{'='*60}")
    log_print(f"Total images processed: {total_processed}/{total_images_to_process}")
    log_print(f"Difference images saved to: {output_folder}")
    log_print(f"Processing complete!")
    log_print(f"Log file saved to: {log_file}")
    log_print(f"Log folder: {log_folder}")